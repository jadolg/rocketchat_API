import pytest
from semver import Version

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

        rocket.users_register(
            email=user.email, name=user.name, password=user.password, username=user.name
        )

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
    testuser = logged_rocket.users_info(username="secondary").json()
    if not testuser.get("success"):
        testuser = logged_rocket.users_create(
            "secondary@domain.com", "secondary", "password", "secondary"
        ).json()

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    logged_rocket.users_delete(_testuser_id)


@pytest.fixture
def skip_v7(logged_rocket):
    """Skip test if chat version is > 7.0.0"""
    version = logged_rocket.info().json().get("info").get("version")
    if version and Version.parse(version) > Version.parse("7.0.0"):
        pytest.skip("Endpoint not available in this version")


@pytest.fixture
def skip_if_no_license(logged_rocket):
    licenses_info = logged_rocket.licenses_info().json()
    if not licenses_info.get("success"):
        pytest.fail("License endpoint not available")
    if "license" in licenses_info and licenses_info.get("license").get("license").get("information").get("offline"):
        return
    pytest.skip("No license available")
