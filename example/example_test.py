from example.example import get_gb_emails
from example.conftest import User
from shreqt import LayerBuilder


def test_get_gb_emails_returns_one_user():
    expected = ["joe@gmail.com"]
    assert get_gb_emails() == expected


def test_get_gb_emails_can_handle_more_than_one_user(db_instance):
    user_layer = LayerBuilder().with_model(User(email="kate@mail.gb", country="GB")).build()
    expected_two = ["joe@gmail.com", "kate@mail.gb"]
    with db_instance.layer(user_layer):
        assert get_gb_emails() == expected_two

    # Additional user should now be removed.
    expected_one = ["joe@gmail.com"]
    assert get_gb_emails() == expected_one
