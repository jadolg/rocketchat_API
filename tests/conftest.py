import pytest

from rocketchat_API.rocketchat import RocketChat


@pytest.fixture(scope="session")
def rocket():
    _rocket = RocketChat()

    return _rocket


@pytest.fixture(scope="session")
def create_user(rocket):
    def _create_user(name="user1", password="password", email="email@domain.com"):
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
