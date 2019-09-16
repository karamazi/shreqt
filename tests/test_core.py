from unittest.mock import patch, MagicMock


@patch("shreqt.core.layer_factory")
def test_onion_pushes_a_layer(layer_factory_mock, db_onion_exa, layer_with_all):
    conn_mock = MagicMock()
    cursor_mock = MagicMock()
    conn_mock.return_value.__enter__.return_value = cursor_mock
    db_onion_exa.connection.connect = conn_mock

    assert db_onion_exa._layers == []
    db_onion_exa.push_layer(layer_with_all)

    assert layer_factory_mock.call_count == 4
    assert layer_factory_mock.return_value.push_query.call_count == 4
    assert cursor_mock.execute.call_count == 4
    assert db_onion_exa._layers == [layer_with_all]


@patch("shreqt.core.layer_factory")
def test_onion_pops_a_layer(layer_factory_mock, db_onion_exa, layer_with_all):
    conn_mock = MagicMock()
    cursor_mock = MagicMock()
    conn_mock.return_value.__enter__.return_value = cursor_mock
    db_onion_exa.connection.connect = conn_mock

    db_onion_exa._layers = [layer_with_all]
    db_onion_exa.pop_layer()

    assert layer_factory_mock.call_count == 4
    assert layer_factory_mock.return_value.pop_query.call_count == 4
    assert cursor_mock.execute.call_count == 4
    assert db_onion_exa._layers == []


def test_onion_layer_applies_temporary_layer(db_onion_exa, layer_with_all):
    db_onion_exa._run_queries = MagicMock()
    assert len(db_onion_exa._layers) == 0

    with db_onion_exa.layer(layer_with_all):
        assert len(db_onion_exa._layers) == 1
        assert db_onion_exa._run_queries.call_count == 1

    assert len(db_onion_exa._layers) == 0
    assert db_onion_exa._run_queries.call_count == 2


def test_state_lock_calls_begin_and_rollback(db_onion_exa):
    conn_mock = MagicMock()
    cursor_mock = MagicMock()
    conn_mock.return_value.__enter__.return_value = cursor_mock
    db_onion_exa.connection.connect = conn_mock

    @db_onion_exa.freeze
    def some_test(conn):
        assert not conn.called
        return 1

    result = some_test()
    assert result == 1
    assert cursor_mock.rollback.call_count == 1
