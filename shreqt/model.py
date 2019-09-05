from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect
from typing import Union, Type
from abc import ABC, abstractmethod

ModelBase = declarative_base()


class ViewBase(ABC):
    name: str

    @staticmethod
    @abstractmethod
    def select():
        raise NotImplementedError("Not implemented")


def full_table_name(table: Union[ModelBase, Type[ModelBase]]):
    table_cls = type(table) if isinstance(table, ModelBase) else table
    table_info = inspect(table_cls).tables[0]
    schema = table_info.schema
    table = table_info.name
    return f"{schema}.{table}"


def table_pk_fields(table: Union[ModelBase, Type[ModelBase]]):
    table_cls = type(table) if isinstance(table, ModelBase) else table

    keys = inspect(table_cls).primary_key
    return [k.name for k in keys]


def fields_dict(model: ModelBase):
    return {f: v for f, v in model.__dict__.items() if f[0] != "_"}
