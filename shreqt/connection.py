import pyexasol
from contextlib import contextmanager
from os import environ


class ExasolConnection:
    @contextmanager
    def connect(self, schema=None, autocommit=True):
        # revlibs.connections doesnt support schema = None.
        # Ideally we'd want to fix revlibs and use them instead of this.

        params = dict(compression=True, autocommit=autocommit)
        if schema:
            params["schema"] = schema

        connection = pyexasol.connect(
            dsn=environ.get("SHREQT_DSN", "localhost:8999"),
            user=environ.get("SHREQT_USER", "sys"),
            password=environ.get("SHREQT_PASS", "exasol"),
            fetch_dict=True,
            fetch_mapper=pyexasol.exasol_mapper,
            **params,
        )
        try:
            yield connection
        finally:
            connection.close()
