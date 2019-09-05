from shreqt.layer_query import (
    LayerQuerySchema,
    LayerQueryTable,
    LayerQueryModel,
    LayerQueryView,
    layer_factory,
)
from tests.resources import SimpleModel, MultiKeyModel, SimpleView
from sqlalchemy_exasol.base import EXADialect
from textwrap import dedent
import pytest


def test_schema():
    q = LayerQuerySchema(None)
    expected = "CREATE SCHEMA test"
    assert q.push_query("test") == expected

    expected = "DROP SCHEMA test CASCADE"
    assert q.pop_query("test") == expected


def test_table():
    q = LayerQueryTable(EXADialect())

    expected = dedent(
        """
        CREATE TABLE schema_one.simple_table (
        \tsome_id VARCHAR(40) NOT NULL,
        \tsome_col VARCHAR(40),
        \tPRIMARY KEY (some_id)
        )\n
        """
    )
    actual = q.push_query(SimpleModel)
    assert actual == expected

    expected = "\nDROP TABLE schema_one.simple_table"
    assert q.pop_query(SimpleModel) == expected


def test_view():
    q = LayerQueryView(EXADialect())

    expected = (
        "CREATE VIEW some_schema.test_view AS\n"
        "SELECT schema_one.simple_table.some_id, schema_one.simple_table.some_col\n"
        "FROM schema_one.simple_table\n"
        "WHERE schema_one.simple_table.some_id = '2'"
    )

    actual = q.push_query(SimpleView)
    assert actual == expected

    expected = "DROP VIEW some_schema.test_view"
    assert q.pop_query(SimpleView) == expected


@pytest.mark.parametrize(
    "model, expected_push, expected_pop",
    [
        [
            SimpleModel.sample(),
            "INSERT INTO schema_one.simple_table (some_id, some_col)\nVALUES ('1', 'foo')",
            "DELETE\nFROM schema_one.simple_table\nWHERE some_id = '1'",
        ],
        [
            MultiKeyModel.sample(),
            (
                "INSERT INTO schema_two.multikey_table (id_one, id_two, not_id)\n"
                "VALUES ('a', 'b', 'bar')"
            ),
            (
                "DELETE\n"
                "FROM schema_two.multikey_table\n"
                "WHERE id_one = 'a'\n"
                "  AND id_two = 'b'"
            ),
        ],
    ],
)
def test_model(model, expected_push, expected_pop):
    q = LayerQueryModel(None)
    actual = q.push_query(model)
    assert actual == expected_push

    actual = q.pop_query(model)
    assert actual == expected_pop


@pytest.mark.parametrize("value, expected", [[1, "1"], ["1", "'1'"]])
def test_model_quote(value, expected):
    assert LayerQueryModel.quote(value) == expected


@pytest.mark.parametrize(
    "element, expected_type",
    [
        ["schema", LayerQuerySchema],
        [SimpleModel, LayerQueryTable],
        [SimpleModel(), LayerQueryModel],
        [SimpleView, LayerQueryView],
    ],
)
def test_layer_factory(element, expected_type):
    query = layer_factory(element, None)
    assert isinstance(query, expected_type)


@pytest.mark.parametrize("value", [None, 1])
def test_layer_factory_raises_type_error_on_unknown_element(value):
    with pytest.raises(TypeError, match="Unable to instantiate Layer Query. .*"):
        layer_factory(value, None)
