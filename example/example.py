from shreqt.connection import ExasolConnection


def get_gb_emails():
    query = "SELECT email FROM utils.users_gb"
    with ExasolConnection().connect() as conn:
        rows = conn.execute(query).fetchall()
        return [row["EMAIL"] for row in rows]
