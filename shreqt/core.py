from shreqt.layer_query import layer_factory
from shreqt.layer import Layer
from enum import Enum
from sqlalchemy_exasol.pyodbc import EXADialect_pyodbc
from shreqt.connection import ExasolConnection
from typing import List
from contextlib import contextmanager


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

    def freeze(self, test_fun):
        def wrapper(*args, **kwargs):
            with self.connection.connect(autocommit=False) as conn:
                res = test_fun(conn, *args, **kwargs)
                conn.rollback()
                return res

        return wrapper

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

    @contextmanager
    def layer(self, layer: Layer):
        self.push_layer(layer)
        try:
            yield self
        finally:
            self.pop_layer()

    def _run_queries(self, queries: List[str]):
        with self.connection.connect(autocommit=False) as conn:
            try:
                for query in queries:
                    conn.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
