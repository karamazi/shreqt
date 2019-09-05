import pytest
from shreqt.core import DBOnion
from shreqt.layer import Layer
from tests.resources import SimpleModel, SimpleView


@pytest.fixture
def db_onion_exa():
    return DBOnion(DBOnion.DBType.EXASOL)


@pytest.fixture
def layer_with_all():
    model = SimpleModel.sample()
    layer = Layer(schemas=["aa"], tables=[SimpleModel], views=[SimpleView], models=[model])
    return layer
