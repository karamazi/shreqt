from example.example import get_gb_emails


def test_get_gb_emails_returns_one_user():
    expected = ["joe@gmail.com"]
    assert get_gb_emails() == expected
