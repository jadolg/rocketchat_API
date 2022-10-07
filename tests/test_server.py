from rocketchat_API.rocketchat import RocketChat


def test_info(logged_rocket):
    info = logged_rocket.info().json()
    assert "info" in info
    assert info.get("success")


def test_statistics(logged_rocket):
    statistics = logged_rocket.statistics().json()
    assert statistics.get("success")


def test_statistics_list(logged_rocket):
    statistics_list = logged_rocket.statistics_list().json()
    assert statistics_list.get("success")


def test_directory(logged_rocket):
    directory = logged_rocket.directory(
        query={"text": "rocket", "type": "users"}
    ).json()
    assert directory.get("success")


def test_spotlight(logged_rocket):
    spotlight = logged_rocket.spotlight(query="user1").json()
    assert spotlight.get("success")
    assert spotlight.get("users") is not None, "No users list found"
    assert spotlight.get("rooms") is not None, "No rooms list found"


def test_login_token(logged_rocket):
    user_id = logged_rocket.headers["X-User-Id"]
    auth_token = logged_rocket.headers["X-Auth-Token"]

    another_rocket = RocketChat(user_id=user_id, auth_token=auth_token)
    logged_user = another_rocket.me().json()

    assert logged_user.get("_id") == user_id
