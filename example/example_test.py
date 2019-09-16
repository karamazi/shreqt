from example.example import get_gb_emails
from example.conftest import User
from shreqt import LayerBuilder

from example.conftest import db


def test_get_gb_emails_returns_one_user():
    expected = ["joe@gmail.com"]
    assert get_gb_emails() == expected


def test_get_gb_emails_can_handle_more_than_one_user():
    user_layer = LayerBuilder().with_model(User(email="kate@mail.gb", country="GB")).build()
    expected_two = ["joe@gmail.com", "kate@mail.gb"]
    with db.layer(user_layer):
        assert get_gb_emails() == expected_two

    # Additional user should now be removed.
    expected_one = ["joe@gmail.com"]
    assert get_gb_emails() == expected_one


def test_db_rollbacks_any_inserted_data_during_frozen_test():
    """
    This is a meta-test which demonstrates how db.freeze works on actual tests.
    """

    # Helper function
    def count_users(conn):
        return conn.execute("SELECT COUNT(*) as cnt FROM raw.users").fetchall()[0]["CNT"]

    # An actual test which inserts data to DB.
    @db.freeze
    def sub_test(conn):
        conn.execute("INSERT INTO raw.users VALUES ('rollback@test.aa', 'GB')")
        assert count_users(conn) == 3

    # Initial state
    with db.connection.connect() as conn:
        assert count_users(conn) == 2

    sub_test()

    # Post test. Any inserted data during test is removed.
    with db.connection.connect() as conn:
        assert count_users(conn) == 2
