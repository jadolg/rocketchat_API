import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketAuthenticationException,
    RocketMissingParamException,
)


@pytest.fixture
def delete_user2(logged_rocket):
    user2_exists = logged_rocket.users_info(username="user2").json().get("success")
    if user2_exists:
        user_id = (
            logged_rocket.users_info(username="user2").json().get("user").get("_id")
        )
        logged_rocket.users_delete(user_id)


def test_login(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()

    with pytest.raises(RocketAuthenticationException):
        logged_rocket.login(user.name, "bad_password")

    assert login.get("status") == "success"
    assert "authToken" in login.get("data")
    assert "userId" in login.get("data")


def test_login_email(logged_rocket, user):
    login = logged_rocket.login(user.email, user.password).json()

    with pytest.raises(RocketAuthenticationException):
        logged_rocket.login(user.name, "bad_password")

    assert login.get("status") == "success"
    assert "authToken" in login.get("data")
    assert "userId" in login.get("data")


def test_me(logged_rocket, user):
    me = logged_rocket.me().json()
    assert me.get("success")
    assert me.get("username") == user.name
    assert me.get("name") == user.name


def test_logout(logged_rocket, user):
    logged_rocket.login(user.name, user.password).json()
    logout = logged_rocket.logout().json()
    assert logout.get("status") == "success"


def test_users_info(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()
    user_id = login.get("data").get("userId")

    users_info_by_id = logged_rocket.users_info(user_id=user_id).json()
    assert users_info_by_id.get("success")
    assert users_info_by_id.get("user").get("_id") == user_id

    users_info_by_name = logged_rocket.users_info(username=user.name).json()
    assert users_info_by_name.get("success")
    assert users_info_by_name.get("user").get("name") == user.name

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_info()


def test_users_get_presence(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()
    users_get_presence = logged_rocket.users_get_presence(
        user_id=login.get("data").get("userId")
    ).json()
    assert users_get_presence.get("success")

    users_get_presence_by_name = logged_rocket.users_get_presence(
        username=user.name
    ).json()
    assert users_get_presence_by_name.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_get_presence()


def test_users_get_avatar(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()

    users_get_avatar = logged_rocket.users_get_avatar(user_id="no_user")
    assert users_get_avatar.status_code == 400

    users_get_avatar = logged_rocket.users_get_avatar(
        user_id=login.get("data").get("userId")
    )
    assert users_get_avatar.text

    users_get_avatar = logged_rocket.users_get_avatar(username=user.name)
    assert users_get_avatar.text

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_get_avatar()


def test_users_reset_avatar(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()
    users_reset_avatar = logged_rocket.users_reset_avatar(
        user_id=login.get("data").get("userId")
    ).json()
    assert users_reset_avatar.get("success")

    users_reset_avatar = logged_rocket.users_reset_avatar(username=user.name).json()
    assert users_reset_avatar.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_reset_avatar()


def test_users_create_token(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()
    users_create_token = logged_rocket.users_create_token(
        user_id=login.get("data").get("userId")
    ).json()
    assert users_create_token.get("success")
    assert "authToken" in users_create_token.get("data")
    assert "userId" in users_create_token.get("data")

    users_create_token = logged_rocket.users_create_token(
        username=login.get("data").get("me").get("name")
    ).json()
    assert users_create_token.get("success")
    assert "authToken" in users_create_token.get("data")
    assert "userId" in users_create_token.get("data")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.users_create_token()


def test_users_create_update_delete(logged_rocket, user):
    name = str(uuid.uuid1())
    users_create = logged_rocket.users_create(
        email="{}@domain.com".format(name),
        name=name,
        password=user.password,
        username=name,
    ).json()
    assert users_create.get("success"), users_create.get("error")

    user_id = users_create.get("user").get("_id")
    users_update = logged_rocket.users_update(
        user_id,
        name="newname",
        password=user.password,
        username="newusername",
    ).json()
    assert users_update.get("success"), "Can not update user"
    assert users_update.get("user").get("name") == "newname"
    assert users_update.get("user").get("username") == "newusername"

    users_delete = logged_rocket.users_delete(user_id).json()
    assert users_delete.get("success")


def test_users_set_active_status(logged_rocket, user):
    login = logged_rocket.login(user.name, user.password).json()
    user_id = login.get("data").get("userId")
    user_set_status = logged_rocket.users_set_active_status(
        user_id, active_status=True
    ).json()
    assert user_set_status.get("success"), user_set_status.get("error")


def test_users_set_avatar_from_file(logged_rocket):
    users_set_avatar = logged_rocket.users_set_avatar(
        avatar_url="tests/assets/avatar.svg"
    ).json()
    assert users_set_avatar.get("success"), users_set_avatar.get("error")


def test_users_set_avatar_from_url(logged_rocket):
    # ToDo: Modify this test so it can run while offline
    users_set_avatar = logged_rocket.users_set_avatar(
        avatar_url="https://upload.wikimedia.org/wikipedia/commons/7/77/Wikipedia_svg_logo.svg"
    ).json()
    assert users_set_avatar.get("success"), users_set_avatar.get("error")


def test_users_forgot_password(logged_rocket):
    users_forgot_password = logged_rocket.users_forgot_password(
        email="email@domain.com"
    ).json()
    assert users_forgot_password.get("success")


def test_users_set_get_preferences(logged_rocket):
    users_set_preferences = logged_rocket.users_set_preferences(
        user_id=logged_rocket.me().json().get("_id"), data={"useEmojis": False}
    ).json()
    assert users_set_preferences.get("success")
    users_get_preferences = logged_rocket.users_get_preferences().json()
    assert users_get_preferences.get("success")


def test_users_list(logged_rocket):
    users_list = logged_rocket.users_list().json()
    assert users_list.get("success")


def test_users_set_status(logged_rocket):
    users_set_status = logged_rocket.users_set_status(
        message="working on it", status="online"
    ).json()
    assert users_set_status.get("success")
