import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


@pytest.fixture(scope="module")
def recipient_user(create_user):
    _recipient = create_user(name="user1")

    return _recipient.name


@pytest.fixture(scope="module")
def recipient_user3(create_user):
    _recipient = create_user(name="user3", email="anotherone@domain.com")

    return _recipient.name


@pytest.fixture(scope="module")
def recipient_user2(create_user):
    _recipient = create_user(name="user2", email="another@domain.com")

    return _recipient.name


def test_dm_create_multiple(logged_rocket, recipient_user3, recipient_user2):
    dm_create = logged_rocket.dm_create_multiple(
        [recipient_user3, recipient_user2]
    ).json()
    assert dm_create.get("success")
    room_id = dm_create.get("room").get("_id")
    dm_send = logged_rocket.chat_post_message(
        room_id=room_id, text="Das ist eine Testnachricht"
    ).json()
    assert dm_send.get("success")


def test_dm_create(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    assert dm_create.get("success")


def test_dm_send(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_send = logged_rocket.chat_post_message(room_id=room_id, text="test").json()
    assert dm_send.get("success")


def test_dm_send_no_text(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_send = logged_rocket.chat_post_message(room_id=room_id, text=None).json()
    assert dm_send.get("success")


def test_dm_list(logged_rocket, recipient_user):
    logged_rocket.dm_create(recipient_user)
    dm_list = logged_rocket.dm_list().json()
    assert dm_list.get("success")


def test_dm_close_open(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_close = logged_rocket.dm_close(room_id).json()
    assert dm_close.get("success")
    dm_open = logged_rocket.dm_open(room_id).json()
    assert dm_open.get("success")


def test_dm_set_topic(logged_rocket, recipient_user):
    topic = "this is my new topic"
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_set_topic = logged_rocket.dm_set_topic(room_id, topic).json()
    assert dm_set_topic.get("success")
    assert dm_set_topic.get("topic") == topic, "Topic set does not match topic returned"


def test_dm_list_everyone(logged_rocket):
    dm_list_everyone = logged_rocket.dm_list_everyone().json()
    assert dm_list_everyone.get("success")


def test_dm_history(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_history = logged_rocket.dm_history(room_id).json()
    assert dm_history.get("success")


def test_dm_members(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_members = logged_rocket.dm_members(room_id=room_id).json()
    assert dm_members.get("success")
    assert dm_members.get("members")[0].get("name") == "user1"


def test_dm_messages(logged_rocket, recipient_user):
    dm_message = logged_rocket.dm_messages(username=recipient_user).json()
    assert dm_message.get("success")
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_message = logged_rocket.dm_messages(room_id=room_id).json()
    assert dm_message.get("success")
    dm_message = logged_rocket.dm_messages(room_id=room_id, pinned=True).json()
    assert dm_message.get("success")
    assert dm_message.get("messages") == []

    with pytest.raises(RocketMissingParamException):
        logged_rocket.dm_messages()


def test_dm_messages_others(logged_rocket, recipient_user):
    # ToDo: Try changing the access configuration so endpoint can be successfully tested
    dm_create = logged_rocket.dm_create(recipient_user).json()
    room_id = dm_create.get("room").get("_id")
    dm_messages_others = logged_rocket.dm_messages_others(room_id).json()
    assert not dm_messages_others.get("success")


def test_dm_files(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    assert dm_create.get("success")

    dm_files = logged_rocket.dm_files(room_id=dm_create.get("room").get("_id")).json()
    assert dm_files.get("success")

    dm_files = logged_rocket.dm_files(user_name=recipient_user).json()
    assert dm_files.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.dm_files()


def test_dm_counters(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user).json()
    assert dm_create.get("success")

    dm_counters = logged_rocket.dm_counters(
        room_id=dm_create.get("room").get("_id")
    ).json()
    assert dm_counters.get("success")

    dm_counters = logged_rocket.dm_counters(
        room_id=dm_create.get("room").get("_id"),
        user_name=logged_rocket.me().json().get("_id"),
    ).json()
    assert dm_counters.get("success")
