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


@pytest.fixture(scope="session")
def create_user(rocket, name="user1", email="email@domain.com"):
    def _create_user(name=name, password="password", email=email):
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
                "secondary@domain.com", "secondary", "password", "secondary"
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
