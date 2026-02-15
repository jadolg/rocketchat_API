import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketApiException,
    RocketBadStatusCodeException,
)
from rocketchat_API.rocketchat import RocketChat


@pytest.fixture(scope="session")
def rocket():
    _rocket = RocketChat()

    return _rocket


def get_tests_passowrd():
    return "yoZy4mN3B83SoKOD2PP1U8PoTUnBlukQ7ac6RlsgR$A"


@pytest.fixture(scope="session")
def create_user(rocket, name="user1", email="email@domain.com"):
    def _create_user(name=name, password=get_tests_passowrd(), email=email):
        # create empty object, because Mock not included to python2
        user = type("test", (object,), {})()

        user.name = name
        user.password = password
        user.email = email

        try:
            rocket.users_register(
                email=user.email,
                name=user.name,
                password=user.password,
                username=user.name,
            )
        except (RocketApiException, RocketBadStatusCodeException):
            pass

        return user

    return _create_user


@pytest.fixture(scope="session")
def user(create_user):
    _user = create_user()

    return _user


@pytest.fixture(scope="session")
def logged_rocket(user):
    _rocket = RocketChat(user.name, user.password)

    return _rocket


@pytest.fixture
def secondary_user(logged_rocket):
    try:
        testuser = logged_rocket.users_info(username="secondary")
    except (RocketApiException, RocketBadStatusCodeException) as exc_info:
        if "User not found." in str(exc_info):
            testuser = logged_rocket.users_create(
                "secondary@domain.com", "secondary", get_tests_passowrd(), "secondary"
            )
        else:
            raise

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    logged_rocket.users_delete(_testuser_id)


@pytest.fixture
def skip_if_no_license(logged_rocket):
    try:
        licenses_info = logged_rocket.licenses_info()
        if "license" in licenses_info and "license" in licenses_info.get("license"):
            return
    except (RocketApiException, RocketBadStatusCodeException):
        pytest.fail("License endpoint not available")
    pytest.skip("No license available")


@pytest.fixture
def livechat_inquiry(logged_rocket):
    """Create a livechat agent, visitor, and room to generate an inquiry."""
    # Save original routing method and set to Manual_Selection to prevent auto-assignment
    original_routing = logged_rocket.settings_get("Livechat_Routing_Method")
    original_routing_value = original_routing.get("value")
    logged_rocket.settings_update("Livechat_Routing_Method", "Manual_Selection")

    username = logged_rocket.me().get("username")
    agent = logged_rocket.livechat_create_user(user_type="agent", username=username)
    logged_rocket.users_set_status(message="working on it", status="online")

    token = str(uuid.uuid1())
    logged_rocket.livechat_register_visitor(token=token)
    livechat_room = logged_rocket.livechat_room(token=token)
    room_id = livechat_room.get("room").get("_id")

    inquiry = logged_rocket.livechat_inquiries_get_one(room_id=room_id)
    data = {
        "agent": agent,
        "agent_id": agent.get("user").get("_id"),
        "token": token,
        "room_id": room_id,
        "inquiry": inquiry.get("inquiry"),
        "inquiry_id": inquiry.get("inquiry", {}).get("_id"),
    }

    yield data

    logged_rocket.livechat_delete_user(
        user_type="agent", user_id=agent.get("user").get("_id")
    )
    # Restore original routing method
    logged_rocket.settings_update("Livechat_Routing_Method", original_routing_value)
