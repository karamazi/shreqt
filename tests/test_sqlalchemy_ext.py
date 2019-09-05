from tests.resources import SimpleModel
from shreqt.sqlalchemy_ext import CreateView, DropView
from sqlalchemy_exasol.pyodbc import EXADialect_pyodbc


def test_create_view_generates_proper_sql():
    t = SimpleModel.__table__
    select = t.select().where(t.c.some_id == "1")
    expected = (
        "CREATE VIEW some.view AS \n"
        "SELECT schema_one.simple_table.some_id, schema_one.simple_table.some_col \n"
        "FROM schema_one.simple_table \n"
        "WHERE schema_one.simple_table.some_id = '1'"
    )
    actual = str(CreateView("some.view", select).compile(dialect=EXADialect_pyodbc()))
    assert actual == expected


def test_drop_view_generates_proper_sql():
    expected = "DROP VIEW some.view"
    actual = str(DropView("some.view").compile(dialect=EXADialect_pyodbc()))
    assert actual == expected
