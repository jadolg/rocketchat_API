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
