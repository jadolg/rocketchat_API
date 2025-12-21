def test_subscriptions_get(logged_rocket):
    subscriptions_get = logged_rocket.subscriptions_get()
    assert "update" in subscriptions_get


def test_subscriptions_get_one(logged_rocket):
    subscriptions_get_one = logged_rocket.subscriptions_get_one(room_id="GENERAL")
    assert "subscription" in subscriptions_get_one


def test_subscriptions_unread(logged_rocket):
    logged_rocket.subscriptions_unread(room_id="GENERAL")


def test_subscriptions_read(logged_rocket):
    logged_rocket.subscriptions_read(rid="GENERAL")
