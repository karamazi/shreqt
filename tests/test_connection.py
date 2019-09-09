from shreqt.connection import ExasolConnection

from unittest.mock import patch, call


@patch("shreqt.connection.pyexasol")
@patch("shreqt.connection.environ")
def test_connect_is_called_with_env_credentials(env_mock, pyexasol_mock):
    with ExasolConnection().connect():
        assert pyexasol_mock.connect.call_count == 1
        assert "schema" not in pyexasol_mock.connect.call_args[1]

        assert call.get("SHREQT_DSN", "localhost:8999") in env_mock.method_calls
        assert call.get("SHREQT_USER", "sys") in env_mock.method_calls
        assert call.get("SHREQT_PASS", "exasol") in env_mock.method_calls
