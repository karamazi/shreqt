import pytest

from shreqt.model import full_table_name, table_pk_fields, fields_dict
from tests.resources import SimpleModel, MultiKeyModel


@pytest.mark.parametrize(
    "table, expected",
    [
        [SimpleModel.sample(), "schema_one.simple_table"],
        [SimpleModel, "schema_one.simple_table"],
        [MultiKeyModel, "schema_two.multikey_table"],
    ],
)
def test_full_table_name_uses_object_or_class(table, expected):
    assert full_table_name(table) == expected


@pytest.mark.parametrize(
    "table, expected",
    [
        [SimpleModel.sample(), ["some_id"]],
        [SimpleModel, ["some_id"]],
        [MultiKeyModel, ["id_one", "id_two"]],
    ],
)
def test_table_pk_fields_uses_object_or_class(table, expected):
    assert table_pk_fields(table) == expected


@pytest.mark.parametrize(
    "model, expected",
    [
        [SimpleModel.sample(), {"some_id": "1", "some_col": "foo"}],
        [MultiKeyModel.sample(), {"id_one": "a", "id_two": "b", "not_id": "bar"}],
    ],
)
def test_fields_dic(model, expected):
    assert fields_dict(model) == expected
