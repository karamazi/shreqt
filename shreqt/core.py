from shreqt.layer_query import layer_factory
from shreqt.layer import Layer
from enum import Enum
from sqlalchemy_exasol.pyodbc import EXADialect_pyodbc
from shreqt.connection import ExasolConnection
from typing import List


class DBOnion:
    class DBType(Enum):
        EXASOL = 1

    def __init__(self, db_type: DBType):
        self.db_type = db_type
        # FIXME, inject engine-based components once we support >1 db.
        self.connection = ExasolConnection()
        self._dialect = EXADialect_pyodbc()
        self._layers: List[Layer] = []

        # self.connection.ping() # Should not be in constructor

    def push_layer(self, layer: Layer):
        self._layers.append(layer)
        elements = layer.to_list_push()
        queries = [layer_factory(e, self._dialect).push_query(e) for e in elements]
        self._run_queries(queries)

    def pop_layer(self):
        layer = self._layers.pop()
        elements = layer.to_list_pop()
        queries = [layer_factory(e, self._dialect).pop_query(e) for e in elements]
        self._run_queries(queries)

    def _run_queries(self, queries: List[str]):
        with self.connection.connect() as conn:
            for query in queries:
                conn.execute(query)
