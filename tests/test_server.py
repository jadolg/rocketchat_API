from rocketchat_API.rocketchat import RocketChat


def test_info(logged_rocket):
    info = logged_rocket.info()
    assert "info" in info


def test_statistics(logged_rocket):
    statistics = logged_rocket.statistics()
    assert all(
        key in statistics
        # Good enough sample to verify that statistics are returned
        for key in [
            "wizard",
            "uniqueId",
            "installedAt",
            "deploymentFingerprintHash",
            "deploymentFingerprintVerified",
        ]
    )


def test_statistics_list(logged_rocket):
    statistics_list = list(logged_rocket.statistics_list())
    assert len(statistics_list) > 0


def test_directory(logged_rocket):
    results = list(logged_rocket.directory(query={"text": "rocket", "type": "users"}))
    for result in results:
        assert "_id" in result


def test_directory_with_string_query(logged_rocket):
    """Test directory method when query is passed as a string"""
    results = list(logged_rocket.directory(query='{"text": "rocket", "type": "users"}'))
    for result in results:
        assert "_id" in result


def test_spotlight(logged_rocket):
    spotlight = logged_rocket.spotlight(query="user1")
    assert spotlight.get("users") is not None, "No users list found"
    assert spotlight.get("rooms") is not None, "No rooms list found"


def test_login_token(logged_rocket):
    user_id = logged_rocket.headers["X-User-Id"]
    auth_token = logged_rocket.headers["X-Auth-Token"]

    another_rocket = RocketChat(user_id=user_id, auth_token=auth_token)
    logged_user = another_rocket.me()

    assert logged_user.get("_id") == user_id
