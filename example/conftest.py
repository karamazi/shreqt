from shreqt import ModelBase, ViewBase, DBOnion, LayerBuilder
from sqlalchemy import Column, String
import pytest

db: DBOnion = None


class User(ModelBase):
    __tablename__ = "users"
    __table_args__ = {"schema": "raw"}

    email = Column(String(100), primary_key=True)
    country = Column(String(2))


class UsersGb(ViewBase):
    name = "utils.users_gb"

    @staticmethod
    def select():
        t = User.__table__
        return t.select().where(t.c.country == "GB")


def pytest_sessionstart(session):
    global db
    db = DBOnion(DBOnion.DBType.EXASOL)

    builder = (
        LayerBuilder().with_schema("utils").with_schema("raw").with_table(User).with_view(UsersGb)
    )

    jon = User(email="joe@gmail.com", country="GB")
    pearchy = User(email="pearchy@gmail.com", country="AU")

    builder.with_model(jon).with_model(pearchy)

    db.push_layer(builder.build())


def pytest_sessionfinish(session, exitstatus):
    global db
    db.pop_layer()
