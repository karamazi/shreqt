from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.schema import CreateTable, DropTable
from shreqt.sqlalchemy_ext import CreateView, DropView
from shreqt.model import ModelBase, ViewBase, full_table_name, fields_dict, table_pk_fields
from typing import Type, Any, Union
from datetime import date, datetime
import abc
import sqlparse


class LayerQuery(abc.ABC):
    def __init__(self, dialect: Dialect):
        self.dialect = dialect

    @abc.abstractmethod
    def push_query(self, obj: Any) -> str:
        ...

    @abc.abstractmethod
    def pop_query(self, obj: Any) -> str:
        ...


class LayerQuerySchema(LayerQuery):
    def push_query(self, schema: str) -> str:
        return f"CREATE SCHEMA {schema}"

    def pop_query(self, schema: str) -> str:
        return f"DROP SCHEMA {schema} CASCADE"


class LayerQueryTable(LayerQuery):
    def push_query(self, table: Type[ModelBase]) -> str:
        return sqlparse.format(
            str(CreateTable(getattr(table, "__table__")).compile(dialect=self.dialect)),
            reident=True,
        )

    def pop_query(self, table: Type[ModelBase]) -> str:
        return sqlparse.format(
            str(DropTable(getattr(table, "__table__")).compile(dialect=self.dialect)),
            reindent=True,
        )


class LayerQueryView(LayerQuery):
    def push_query(self, view: Type[ViewBase]) -> str:
        return sqlparse.format(
            str(CreateView(view.name, view.select()).compile(dialect=self.dialect)), reident=True
        )

    def pop_query(self, view: Type[ViewBase]) -> str:
        return sqlparse.format(
            str(DropView(view.name).compile(dialect=self.dialect)), reindent=True
        )


class LayerQueryModel(LayerQuery):
    def push_query(self, model: ModelBase) -> str:
        full_table = full_table_name(model)
        fields = fields_dict(model)
        columns = list(fields.keys())
        values = map(LayerQueryModel.quote, [fields[c] for c in columns])
        columns_str = ", ".join(columns)
        values_str = ", ".join(values)
        return sqlparse.format(
            f"INSERT INTO {full_table} ({columns_str}) VALUES ({values_str})", reindent=True
        )

    def pop_query(self, model: ModelBase) -> str:
        full_table = full_table_name(model)
        fields = fields_dict(model)

        primary_fields_values = {k: fields[k] for k in table_pk_fields(model)}
        conditions = [
            f"{field} = {LayerQueryModel.quote(value)}"
            for field, value in primary_fields_values.items()
        ]
        conditions_str = " AND ".join(conditions)
        return sqlparse.format(f"DELETE FROM {full_table} WHERE {conditions_str}", reindent=True)

    @staticmethod
    def quote(value: Any) -> str:
        if value is None:
            return "NULL"
        if isinstance(value, str):
            return f"'{value}'"
        if isinstance(value, datetime):
            return value.strftime("'%Y-%m-%d %H:%M:%S'")
        if isinstance(value, date):
            return f"'{value.isoformat()}'"
        return str(value)


def layer_factory(
    element: Union[str, ModelBase, Type[ModelBase], Type[ViewBase]], dialect
) -> "LayerQuery":
    try:
        if isinstance(element, str):
            return LayerQuerySchema(dialect)

        if isinstance(element, ModelBase):
            return LayerQueryModel(dialect)

        if issubclass(element, ModelBase):
            return LayerQueryTable(dialect)

        if issubclass(element, ViewBase):
            return LayerQueryView(dialect)
    except TypeError:
        pass
    raise TypeError("Unable to instantiate Layer Query. Incorrect element type") from None
