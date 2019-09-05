from shreqt.model import ModelBase, ViewBase
from sqlalchemy import Column, String


class SimpleModel(ModelBase):
    __tablename__ = "simple_table"
    __table_args__ = {"schema": "schema_one"}

    some_id = Column(String(40), primary_key=True)
    some_col = Column(String(40))

    @staticmethod
    def sample():
        return SimpleModel(some_id="1", some_col="foo")


class MultiKeyModel(ModelBase):
    __tablename__ = "multikey_table"
    __table_args__ = {"schema": "schema_two"}

    id_one = Column(String(40), primary_key=True)
    id_two = Column(String(40), primary_key=True)
    not_id = Column(String(40))

    @staticmethod
    def sample():
        return MultiKeyModel(id_one="a", id_two="b", not_id="bar")


class SimpleView(ViewBase):
    name = "some_schema.test_view"

    @staticmethod
    def select():
        t = SimpleModel.__table__
        return t.select().where(t.c.some_id == "2")
