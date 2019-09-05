from shreqt.layer import LayerBuilder

from tests.resources import SimpleModel, MultiKeyModel, SimpleView


def test_layer_builder():
    builder = LayerBuilder()
    test_model = SimpleModel.sample()
    builder.with_model(test_model)
    builder.with_table(MultiKeyModel)
    builder.with_schema("third_schema")

    layer = builder.build()

    assert layer.models == [test_model]
    assert layer.tables == [SimpleModel, MultiKeyModel]
    assert sorted(layer.schemas) == sorted(["schema_one", "schema_two", "third_schema"])


def test_layer_builder_returns_self_on_with():
    builder = LayerBuilder()
    test_model = SimpleModel.sample()
    assert isinstance(builder.with_model(test_model), LayerBuilder)
    assert isinstance(builder.with_table(MultiKeyModel), LayerBuilder)
    assert isinstance(builder.with_view(SimpleView), LayerBuilder)
    assert isinstance(builder.with_schema("third_schema"), LayerBuilder)


def test_layer_push_pop_order(layer_with_all):
    model = layer_with_all.models[0]
    expected_push = ["aa", SimpleModel, SimpleView, model]
    assert layer_with_all.to_list_push() == expected_push

    expected_pop = [model, SimpleView, SimpleModel, "aa"]
    assert layer_with_all.to_list_pop() == expected_pop
