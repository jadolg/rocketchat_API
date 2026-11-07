import base64
import hashlib
import hmac
import json
import struct
import time
import uuid
from types import SimpleNamespace

import pytest
import semver

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketApiException,
    RocketAuthenticationException,
    RocketMissingParamException,
)
from rocketchat_API.rocketchat import RocketChat
from tests.conftest import get_tests_passowrd


def totp_code(secret):
    key = base64.b32decode(secret.upper() + "=" * (-len(secret) % 8))
    digest = hmac.new(
        key, struct.pack(">Q", int(time.time()) // 30), hashlib.sha1
    ).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    return f"{value % 10**6:06d}"


@pytest.fixture
def temp_user(logged_rocket):
    username = f"tmp_{uuid.uuid4().hex[:10]}"
    created = logged_rocket.users_create(
        f"{username}@domain.com", username, get_tests_passowrd(), username
    )
    user_id = created.get("user").get("_id")
    session = RocketChat(username, get_tests_passowrd())
    yield SimpleNamespace(id=user_id, name=username, rocket=session)
    # The user may already have been removed by the test itself
    try:
        logged_rocket.users_delete(user_id)
    except RocketApiException:
        pass


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


def test_users_info_by_email(logged_rocket, skip_if_version_under):
    skip_if_version_under("8.4.0")
    email = f"{uuid.uuid4().hex}@domain.com"
    username = f"info_email_{uuid.uuid4().hex[:8]}"

    # No user has this email yet, so the lookup must fail.
    with pytest.raises(RocketApiException):
        logged_rocket.users_info(email=email)

    created = logged_rocket.users_create(
        email, username, get_tests_passowrd(), username
    )
    user_id = created.get("user").get("_id")
    try:
        users_info_by_email = logged_rocket.users_info(email=email)
        assert users_info_by_email.get("user").get("_id") == user_id
    finally:
        logged_rocket.users_delete(user_id)


def test_users_info_by_import_id(logged_rocket):
    # An importId can only be set while importing users (CSV, Slack, ...), which
    # is not exposed through the API, so the success path cannot be set up from
    # code. We only assert the parameter reaches the server: the API answering
    # with a "user not found" error (rather than the wrapper raising a
    # missing-param error) proves importId was sent as a query parameter.
    with pytest.raises(RocketApiException):
        logged_rocket.users_info(import_id="nonexistent")


def test_users_info_by_free_switch_extension(logged_rocket, skip_if_version_under):
    skip_if_version_under("8.5.0")
    # Assigning a freeSwitchExtension requires a configured FreeSwitch server
    # (VoIP_TeamCollab), which is part of the deployment rather than something we
    # can set up from code, so the success path cannot be exercised here. We only
    # assert the parameter reaches the server: the API answering with a "user not
    # found" error (rather than the wrapper raising a missing-param error) proves
    # freeSwitchExtension was sent as a query parameter.
    with pytest.raises(RocketApiException):
        logged_rocket.users_info(free_switch_extension="0000")


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
        avatar_url="https://files.akiel.dev/Wikipedia_svg_logo.svg"
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


def test_users_set_status(logged_rocket):
    logged_rocket.users_set_status(message="working on it", status="online")


def test_users_list_by_status(logged_rocket, user):
    listed = list(logged_rocket.users_list_by_status(status="active"))
    assert user.name in [u.get("username") for u in listed]


def test_users_get_username_suggestion(logged_rocket):
    assert logged_rocket.users_get_username_suggestion().get("result")


def test_users_get_avatar_suggestion(logged_rocket):
    assert "suggestions" in logged_rocket.users_get_avatar_suggestion()


def test_users_check_username_availability(logged_rocket, user):
    free = logged_rocket.users_check_username_availability(uuid.uuid4().hex[:12])
    assert free.get("result") is True

    taken = logged_rocket.users_check_username_availability("rocket.cat")
    assert taken.get("result") is False


def test_users_presence(logged_rocket):
    presence = logged_rocket.users_presence()
    assert presence.get("full") is True
    assert "rocket.cat" in [u.get("username") for u in presence.get("users")]

    by_ids = logged_rocket.users_presence(
        ids=["rocket.cat"], **{"from": "2000-01-01T00:00:00.000Z"}
    )
    assert [u.get("_id") for u in by_ids.get("users")] == ["rocket.cat"]


def test_users_autocomplete(logged_rocket, user):
    found = logged_rocket.users_autocomplete(json.dumps({"term": user.name}))
    assert user.name in [u.get("username") for u in found.get("items")]


def test_users_get_status(logged_rocket, user):
    user_id = logged_rocket.me().get("_id")

    by_id = logged_rocket.users_get_status(user_id=user_id)
    assert by_id.get("_id") == user_id
    assert "status" in by_id

    by_name = logged_rocket.users_get_status(username=user.name)
    assert by_name.get("_id") == user_id

    own = logged_rocket.users_get_status()
    assert own.get("_id") == user_id


def test_users_list_teams(logged_rocket):
    teams = logged_rocket.users_list_teams(logged_rocket.me().get("_id"))
    assert isinstance(teams.get("teams"), list)


def test_users_personal_access_tokens(logged_rocket):
    token_name = f"token_{uuid.uuid4().hex[:8]}"
    generated = logged_rocket.users_generate_personal_access_token(
        token_name, bypassTwoFactor=True
    )
    assert generated.get("token")

    listed = logged_rocket.users_get_personal_access_tokens()
    assert token_name in [t.get("name") for t in listed.get("tokens")]

    regenerated = logged_rocket.users_regenerate_personal_access_token(token_name)
    assert regenerated.get("token")
    assert regenerated.get("token") != generated.get("token")

    logged_rocket.users_remove_personal_access_token(token_name)
    listed = logged_rocket.users_get_personal_access_tokens()
    assert token_name not in [t.get("name") for t in listed.get("tokens")]


def test_users_request_data_download(temp_user):
    assert temp_user.rocket.users_request_data_download().get("requested") is True
    assert "requested" in temp_user.rocket.users_request_data_download(full_export=True)


def test_users_deactivate_idle(logged_rocket):
    assert logged_rocket.users_deactivate_idle(days_idle=36500).get("count") == 0


def test_users_send_confirmation_email(rocket, logged_rocket, user):
    # TODO: remove the 8.5 branch once Rocket.Chat 8.5 reaches EOL
    version = semver.Version.parse(
        rocket.info()["version"], optional_minor_and_patch=True
    )
    client = logged_rocket if version < semver.Version(8, 6, 0) else rocket
    client.users_send_confirmation_email(user.email)


def test_users_update_own_basic_info(temp_user):
    new_name = f"renamed_{uuid.uuid4().hex[:6]}"
    updated = temp_user.rocket.users_update_own_basic_info(data={"name": new_name})
    assert updated.get("user").get("name") == new_name
    assert temp_user.rocket.me().get("name") == new_name


def test_users_2fa_email(logged_rocket, temp_user):
    # Email 2FA can only be enabled with a verified email
    logged_rocket.users_update(temp_user.id, verified=True)

    temp_user.rocket.users_2fa_enable_email()
    temp_user.rocket.users_2fa_send_email_code(temp_user.name)

    # With 2FA on, protected endpoints reject requests without a code
    with pytest.raises(RocketApiException):
        temp_user.rocket.users_2fa_disable_email()


def test_users_2fa_send_email_code_and_disable(logged_rocket, temp_user):
    temp_user.rocket.users_2fa_disable_email()
    temp_user.rocket.users_2fa_send_email_code(temp_user.name)


def test_users_totp(temp_user, skip_if_version_under):
    skip_if_version_under("8.8.0")
    enabled = temp_user.rocket.users_enable_totp()
    secret = enabled.get("secret")
    assert secret

    assert temp_user.rocket.users_validate_totp(totp_code(secret)).get("codes")
    assert temp_user.rocket.users_totp_codes_remaining().get("remaining") is not None

    regenerated = temp_user.rocket.users_regenerate_totp_codes(totp_code(secret))
    assert regenerated.get("codes")

    temp_user.rocket.users_disable_totp(totp_code(secret))


def test_users_reset_totp(logged_rocket, temp_user):
    logged_rocket.users_reset_totp(userId=temp_user.id)
    logged_rocket.users_reset_totp(username=temp_user.name)
    temp_user.rocket.users_reset_totp()


def test_users_reset_e2e_key(logged_rocket, temp_user):
    logged_rocket.users_reset_e2e_key(userId=temp_user.id)
    logged_rocket.users_reset_e2e_key(username=temp_user.name)
    # Resetting another user's key logs them out
    session = RocketChat(temp_user.name, get_tests_passowrd())
    session.users_reset_e2e_key()


def test_users_logout_other_clients(temp_user):
    temp_user.rocket.users_logout_other_clients()


def test_users_remove_other_tokens(temp_user):
    temp_user.rocket.users_remove_other_tokens()


def test_users_logout(logged_rocket, temp_user):
    logged_rocket.users_logout(userId=temp_user.id)
    with pytest.raises(RocketApiException):
        temp_user.rocket.me()

    session = RocketChat(temp_user.name, get_tests_passowrd())
    session.users_logout()


def test_users_delete_own_account(logged_rocket, temp_user):
    logged_rocket.settings_update("Accounts_AllowDeleteOwnAccount", True)
    try:
        temp_user.rocket.users_delete_own_account(get_tests_passowrd())
    finally:
        logged_rocket.settings_update("Accounts_AllowDeleteOwnAccount", False)
    with pytest.raises(RocketApiException):
        logged_rocket.users_info(user_id=temp_user.id)
