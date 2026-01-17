import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketApiException,
)


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
    dm_create = logged_rocket.dm_create_multiple([recipient_user3, recipient_user2])
    room_id = dm_create.get("room").get("_id")
    logged_rocket.chat_post_message(room_id=room_id, text="Das ist eine Testnachricht")


def test_dm_create(logged_rocket, recipient_user):
    logged_rocket.dm_create(recipient_user)


def test_dm_send(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    logged_rocket.chat_post_message(room_id=room_id, text="test")


def test_dm_send_no_text(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    logged_rocket.chat_post_message(room_id=room_id, text=None)


def test_dm_list(logged_rocket, recipient_user):
    logged_rocket.dm_create(recipient_user)
    iterated_dms = list(logged_rocket.dm_list())
    assert len(iterated_dms) > 0, "Should have at least one DM"

    for dm in iterated_dms:
        assert "_id" in dm


def test_dm_close_open(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    logged_rocket.dm_close(room_id)
    logged_rocket.dm_open(room_id)


def test_dm_set_topic(logged_rocket, recipient_user):
    topic = "this is my new topic"
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    dm_set_topic = logged_rocket.dm_set_topic(room_id, topic)
    assert dm_set_topic.get("topic") == topic, "Topic set does not match topic returned"


def test_dm_history(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    iterated_messages = list(logged_rocket.dm_history(room_id=room_id))
    for message in iterated_messages:
        assert "_id" in message


def test_dm_members(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    dm_members = logged_rocket.dm_members(room_id=room_id)
    assert dm_members.get("members")[0].get("name") == "user1"


def test_dm_messages(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    iterated_messages = list(logged_rocket.dm_messages(room_id=room_id))
    for message in iterated_messages:
        assert "_id" in message

    iterated_messages_username = list(
        logged_rocket.dm_messages(username=recipient_user)
    )

    assert iterated_messages == iterated_messages_username

    with pytest.raises(RocketMissingParamException):
        logged_rocket.dm_messages()


def test_dm_messages_others(logged_rocket, recipient_user):
    # ToDo: Try changing the access configuration so endpoint can be successfully tested
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    with pytest.raises(RocketApiException):
        logged_rocket.dm_messages_others(room_id)


def test_dm_files(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)
    room_id = dm_create.get("room").get("_id")
    logged_rocket.rooms_media(
        room_id=room_id, file="tests/assets/avatar.png", msg="hey there"
    )
    iterated_files = list(logged_rocket.dm_files(room_id=room_id))
    for file in iterated_files:
        assert "_id" in file

    iterated_files_username = list(logged_rocket.dm_files(user_name=recipient_user))

    assert iterated_files == iterated_files_username

    with pytest.raises(RocketMissingParamException):
        logged_rocket.dm_files()


def test_dm_counters(logged_rocket, recipient_user):
    dm_create = logged_rocket.dm_create(recipient_user)

    dm_counters = logged_rocket.dm_counters(room_id=dm_create.get("room").get("_id"))
    assert all(
        key in dm_counters
        for key in ["joined", "members", "unreads", "msgs", "userMentions"]
    )

    dm_counters = logged_rocket.dm_counters(
        room_id=dm_create.get("room").get("_id"),
        user_name=logged_rocket.me().get("_id"),
    )
    assert all(
        key in dm_counters
        for key in ["joined", "members", "unreads", "msgs", "userMentions"]
    )


def test_dm_list_everyone(logged_rocket):
    iterated_dms = list(logged_rocket.dm_list_everyone())
    for dm in iterated_dms:
        assert "_id" in dm
