import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketAuthenticationException,
    RocketMissingParamException,
    RocketApiException,
)


def test_login(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)

    with pytest.raises(RocketAuthenticationException):
        logged_rocket.login(user.name, "bad_password")

    assert login.get("status") == "success"
    assert "authToken" in login.get("data")
    assert "userId" in login.get("data")


def test_login_email(logged_rocket, user):
    login = logged_rocket.login(user.email, user.password)

    with pytest.raises(RocketAuthenticationException):
        logged_rocket.login(user.name, "bad_password")

    assert "authToken" in login.get("data")
    assert "userId" in login.get("data")


def test_me(logged_rocket, user):
    me = logged_rocket.me()
    assert me.get("username") == user.name
    assert me.get("name") == user.name


def test_logout(logged_rocket, user):
    logged_rocket.login(user.name, user.password)
    logged_rocket.logout()


def test_users_info(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)
    user_id = login.get("data").get("userId")

    users_info_by_id = logged_rocket.users_info(user_id=user_id)
    assert users_info_by_id.get("user").get("_id") == user_id

    users_info_by_name = logged_rocket.users_info(username=user.name)
    assert users_info_by_name.get("user").get("name") == user.name

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_info()


def test_users_get_presence(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)
    users_get_presence = logged_rocket.users_get_presence(
        user_id=login.get("data").get("userId")
    )

    assert all(
        key in users_get_presence
        for key in ["connectionStatus", "presence", "lastLogin"]
    )

    users_get_presence_by_name = logged_rocket.users_get_presence(username=user.name)

    assert all(
        key in users_get_presence_by_name
        for key in ["connectionStatus", "presence", "lastLogin"]
    )

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_get_presence()


def test_users_get_avatar(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)

    with pytest.raises(RocketApiException):
        logged_rocket.users_get_avatar(user_id="no_user")

    logged_rocket.users_get_avatar(user_id=login.get("data").get("userId"))

    logged_rocket.users_get_avatar(username=user.name)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_get_avatar()


def test_users_reset_avatar(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)
    logged_rocket.users_reset_avatar(user_id=login.get("data").get("userId"))

    logged_rocket.users_reset_avatar(username=user.name)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_reset_avatar()


def test_users_create_token(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)
    # noinspection HardcodedPassword
    secret = "1234567890abcdef"
    users_create_token = logged_rocket.users_create_token(
        user_id=login.get("data").get("userId"), secret=secret
    )
    assert "authToken" in users_create_token.get("data")
    assert "userId" in users_create_token.get("data")


def test_users_create_update_delete(logged_rocket, user):
    name = str(uuid.uuid1())
    users_create = logged_rocket.users_create(
        email="{}@domain.com".format(name),
        name=name,
        password=user.password,
        username=name,
    )

    user_id = users_create.get("user").get("_id")
    users_update = logged_rocket.users_update(
        user_id,
        name="newname",
        password=user.password,
        username="newusername",
    )
    assert users_update.get("user").get("name") == "newname"
    assert users_update.get("user").get("username") == "newusername"

    logged_rocket.users_delete(user_id)


def test_users_set_active_status(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password)
    user_id = login.get("data").get("userId")
    user_set_status = logged_rocket.users_set_active_status(user_id, active_status=True)
    assert user_set_status.get("user").get("_id") == user_id


def test_users_set_avatar_from_file(logged_rocket):
    logged_rocket.users_set_avatar(avatar_url="tests/assets/avatar.svg")


def test_users_set_avatar_from_url(logged_rocket):
    # ToDo: Modify this test so it can run while offline
    logged_rocket.users_set_avatar(
        avatar_url="https://upload.wikimedia.org/wikipedia/commons/7/77/Wikipedia_svg_logo.svg"
    )


def test_users_forgot_password(logged_rocket):
    logged_rocket.users_forgot_password(email="email@domain.com")


def test_users_set_get_preferences(logged_rocket):
    users_set_preferences = logged_rocket.users_set_preferences(
        user_id=logged_rocket.me().get("_id"), data={"useEmojis": False}
    )
    assert "user" in users_set_preferences
    assert users_set_preferences.get("user").get("_id") == logged_rocket.me().get("_id")
    users_get_preferences = logged_rocket.users_get_preferences()
    assert "preferences" in users_get_preferences


def test_users_list(logged_rocket):
    iterated_users = list(logged_rocket.users_list())
    assert len(iterated_users) > 0, "Should have at least one user"

    for user in iterated_users:
        assert "_id" in user
        assert "username" in user

    iterated_users_custom = list(logged_rocket.users_list(count=1))
    assert len(iterated_users_custom) > 0
    assert len(iterated_users_custom) == len(iterated_users)

    for user in logged_rocket.users_list():
        assert "_id" in user


def test_users_set_status(logged_rocket):
    logged_rocket.users_set_status(message="working on it", status="online")
