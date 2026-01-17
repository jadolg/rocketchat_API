import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketApiException,
)


@pytest.fixture(autouse=True)
def add_owner(logged_rocket, user):
    """Add test user as owner in GENERAL channel in every test in this module"""
    try:
        logged_rocket.channels_add_owner("GENERAL", username=user.name)
    except RocketApiException as e:
        if e.error_type != "error-user-already-owner":
            raise e


@pytest.fixture
def testuser_id(logged_rocket):
    try:
        testuser = logged_rocket.users_info(username="testuser1")
    except RocketApiException as e:
        if e.error == "User not found.":
            testuser = logged_rocket.users_create(
                "testuser1@domain.com", "testuser1", "password", "testuser1"
            )
        else:
            raise e

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    try:
        logged_rocket.users_delete(_testuser_id)
    except RocketApiException:
        pass


def test_channels_list(logged_rocket):
    iterated_channels = list(logged_rocket.channels_list())
    assert len(iterated_channels) > 0, "Should have at least one channel"

    for channel in iterated_channels:
        assert "_id" in channel
        assert "name" in channel

    iterated_channels_custom = list(logged_rocket.channels_list(count=1))
    assert len(iterated_channels_custom) > 0

    for channel in logged_rocket.channels_list():
        assert "_id" in channel


def test_channels_list_joined(logged_rocket):
    iterated_channels = list(logged_rocket.channels_list_joined())
    assert len(iterated_channels) > 0, "Should have at least one joined channel"

    for channel in iterated_channels:
        assert "_id" in channel
        assert "name" in channel

    iterated_channels_custom = list(logged_rocket.channels_list_joined(count=1))
    assert len(iterated_channels_custom) > 0

    for channel in logged_rocket.channels_list_joined():
        assert "_id" in channel


def test_channels_info(logged_rocket):
    channels_info = logged_rocket.channels_info(room_id="GENERAL")
    assert "channel" in channels_info
    assert channels_info.get("channel").get("_id") == "GENERAL"

    channel_name = channels_info.get("channel").get("name")
    channels_info = logged_rocket.channels_info(channel=channel_name)
    assert "channel" in channels_info
    assert channels_info.get("channel").get("_id") == "GENERAL"
    assert channels_info.get("channel").get("name") == channel_name

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_info()


def test_channels_history(logged_rocket):
    iterated_messages = list(logged_rocket.channels_history(room_id="GENERAL"))
    for message in iterated_messages:
        assert "_id" in message

    # Test with custom count parameter
    iterated_messages_custom = list(
        logged_rocket.channels_history(room_id="GENERAL", count=1)
    )
    for message in iterated_messages_custom:
        assert "_id" in message

    for message in logged_rocket.channels_history(room_id="GENERAL"):
        assert "_id" in message


def test_channels_add_all(logged_rocket):
    channels_add_all = logged_rocket.channels_add_all("GENERAL")
    assert "channel" in channels_add_all


def test_channels_add_and_remove_moderator(logged_rocket):
    me = logged_rocket.me()
    logged_rocket.channels_add_moderator("GENERAL", me.get("_id"))
    logged_rocket.channels_remove_moderator("GENERAL", me.get("_id"))


def test_channels_list_moderator(logged_rocket):
    channels_list_moderator = logged_rocket.channels_moderators(room_id="GENERAL")
    assert "moderators" in channels_list_moderator
    channel_name = (
        logged_rocket.channels_info(room_id="GENERAL").get("channel").get("name")
    )
    channels_list_moderator_by_name = logged_rocket.channels_moderators(
        channel=channel_name
    )
    assert "moderators" in channels_list_moderator_by_name
    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_moderators()


def test_channels_add_and_remove_owner(logged_rocket, testuser_id):
    logged_rocket.channels_invite("GENERAL", testuser_id)
    logged_rocket.channels_add_owner("GENERAL", user_id=testuser_id)
    logged_rocket.channels_remove_owner(room_id="GENERAL", user_id=testuser_id)
    logged_rocket.channels_kick(room_id="GENERAL", user_id=testuser_id)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_add_owner(room_id="GENERAL")


def test_channels_add_and_remove_leader(logged_rocket, testuser_id):
    channels_invite = logged_rocket.channels_invite("GENERAL", testuser_id)
    assert "channel" in channels_invite
    assert channels_invite.get("channel").get("_id") == "GENERAL"
    logged_rocket.channels_add_leader("GENERAL", user_id=testuser_id)

    logged_rocket.channels_remove_leader("GENERAL", user_id=testuser_id)


def test_channels_archive_unarchive(logged_rocket):
    logged_rocket.channels_archive("GENERAL")
    logged_rocket.channels_unarchive("GENERAL")


def test_channels_close_open(logged_rocket):
    logged_rocket.channels_close("GENERAL")
    logged_rocket.channels_open("GENERAL")


def test_channels_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    assert name == channels_create.get("channel").get("name")
    logged_rocket.channels_delete(channel=name)
    channels_create = logged_rocket.channels_create(name)
    room_id = channels_create.get("channel").get("_id")
    logged_rocket.channels_delete(room_id=room_id)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_delete()


def test_channels_get_integrations(logged_rocket):
    channels_get_integrations = logged_rocket.channels_get_integrations(
        room_id="GENERAL"
    )
    assert all(
        key in channels_get_integrations
        for key in ["integrations", "count", "offset", "total"]
    )


def test_channels_invite(logged_rocket, testuser_id):
    channels_invite = logged_rocket.channels_invite("GENERAL", testuser_id)
    assert "channel" in channels_invite
    assert channels_invite.get("channel").get("_id") == "GENERAL"


def test_channels_join(logged_rocket, testuser_id):
    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    logged_rocket.channels_invite(
        room_id=channels_create.get("channel").get("_id"), user_id=testuser_id
    )

    logged_rocket.channels_add_owner(
        channels_create.get("channel").get("_id"), user_id=testuser_id
    )

    join_code = str(uuid.uuid1())
    channels_set_join_code = logged_rocket.channels_set_join_code(
        channels_create.get("channel").get("_id"), join_code
    )
    assert "channel" in channels_set_join_code
    assert channels_set_join_code.get("channel").get("joinCodeRequired")

    channels_leave = logged_rocket.channels_leave(
        channels_create.get("channel").get("_id")
    )
    assert "channel" in channels_leave

    channels_join = logged_rocket.channels_join(
        channels_create.get("channel").get("_id"), join_code
    )
    assert "channel" in channels_join


def test_channels_kick(logged_rocket, testuser_id):
    channels_kick = logged_rocket.channels_kick("GENERAL", testuser_id)
    assert "channel" in channels_kick
    assert channels_kick.get("channel").get("_id") == "GENERAL"


def test_channels_leave(logged_rocket, testuser_id):
    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.channels_leave("GENERAL")
    assert "error-you-are-last-owner" == exc_info.value.error_type

    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    logged_rocket.channels_invite(
        room_id=channels_create.get("channel").get("_id"), user_id=testuser_id
    )

    logged_rocket.channels_add_owner(
        channels_create.get("channel").get("_id"), user_id=testuser_id
    )
    channels_leave = logged_rocket.channels_leave(
        channels_create.get("channel").get("_id")
    )
    assert "channel" in channels_leave


def test_channels_rename(logged_rocket):
    name = str(uuid.uuid1())
    name2 = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    channels_rename = logged_rocket.channels_rename(
        room_id=channels_create.get("channel").get("_id"), name=name2
    )
    assert channels_rename.get("channel").get("name") == name2


def test_channels_set_description(logged_rocket):
    description = str(uuid.uuid1())
    channels_set_description = logged_rocket.channels_set_description(
        "GENERAL", description
    )
    assert (
        channels_set_description.get("description") == description
    ), "Description does not match"


def test_channels_set_join_code(logged_rocket):
    join_code = str(uuid.uuid1())
    channels_set_join_code = logged_rocket.channels_set_join_code("GENERAL", join_code)
    assert "channel" in channels_set_join_code
    assert channels_set_join_code.get("channel").get("joinCodeRequired")


def test_channels_set_read_only(logged_rocket):
    logged_rocket.channels_set_read_only("GENERAL", True)
    logged_rocket.channels_set_read_only("GENERAL", False)


def test_channels_set_topic(logged_rocket):
    topic = str(uuid.uuid1())
    channels_set_topic = logged_rocket.channels_set_topic("GENERAL", topic)
    assert channels_set_topic.get("topic") == topic, "Topic does not match"


def test_channels_set_type(logged_rocket):
    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    channel_id = channels_create.get("channel").get("_id")

    channels_set_type = logged_rocket.channels_set_type(channel_id, "p")
    assert channels_set_type.get("channel").get("t"), "p"

    with pytest.raises(RocketApiException):
        logged_rocket.channels_set_type(channel_id, "c")


def test_channels_set_announcement(logged_rocket):
    announcement = str(uuid.uuid1())
    channels_set_announcement = logged_rocket.channels_set_announcement(
        "GENERAL", announcement
    )
    assert (
        channels_set_announcement.get("announcement") == announcement
    ), "Topic does not match"


def test_channels_set_custom_fields(logged_rocket):
    cf = {"key": "value"}
    channels_set_custom_fields = logged_rocket.channels_set_custom_fields("GENERAL", cf)
    assert cf == channels_set_custom_fields["channel"]["customFields"]


def test_channels_roles(logged_rocket):
    channels_roles = logged_rocket.channels_roles(room_id="GENERAL")
    assert channels_roles.get("roles") is not None
    channels_roles = logged_rocket.channels_roles(room_name="general")
    assert channels_roles.get("roles") is not None

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_roles()


def test_channels_counters(logged_rocket):
    channels_counters = logged_rocket.channels_counters(room_id="GENERAL")
    assert all(
        key in channels_counters
        for key in [
            "joined",
            "members",
            "unreads",
            "msgs",
            "userMentions",
        ]
    )
    channels_counters_by_name = logged_rocket.channels_counters(room_name="general")
    assert all(
        key in channels_counters_by_name
        for key in [
            "joined",
            "members",
            "unreads",
            "msgs",
            "userMentions",
        ]
    )
    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_counters()


def test_channels_online(logged_rocket):
    channels_online = logged_rocket.channels_online(_id="GENERAL")
    assert len(channels_online.get("online")) >= 1


def test_channels_set_default(logged_rocket):
    channels_set_default = logged_rocket.channels_set_default(
        room_id="GENERAL", default=False
    )
    assert channels_set_default.get("channel").get("default") is False
    channels_set_default = logged_rocket.channels_set_default(
        room_id="GENERAL", default=True
    )
    assert channels_set_default.get("channel").get("default")


def test_channels_members(logged_rocket):
    iterated_members = list(logged_rocket.channels_members(room_id="GENERAL"))
    iterated_members_channel = list(logged_rocket.channels_members(channel="general"))
    assert len(iterated_members) > 0, "Should have at least one member"
    assert len(iterated_members) == len(iterated_members_channel)

    for member in iterated_members:
        assert "_id" in member
        assert "username" in member

    # Test with custom count parameter
    iterated_members_custom = list(
        logged_rocket.channels_members(room_id="GENERAL", count=1)
    )
    assert len(iterated_members_custom) > 0

    for member in logged_rocket.channels_members(room_id="GENERAL"):
        assert "_id" in member

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_members()


def test_channels_files(logged_rocket):
    rooms_upload = logged_rocket.rooms_media(
        "GENERAL", file="tests/assets/avatar.png", msg="a test file"
    )
    assert "file" in rooms_upload

    iterated_files = list(logged_rocket.channels_files(room_id="GENERAL"))
    for file in iterated_files:
        assert "_id" in file

    iterated_files_room_name = list(logged_rocket.channels_files(room_name="general"))
    for file in iterated_files:
        assert "_id" in file

    assert len(iterated_files_room_name) == len(iterated_files)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.channels_files()


def test_channels_get_all_user_mentions_by_channel(logged_rocket):
    logged_rocket.chat_post_message(channel="GENERAL", text="Hello @user1")
    iterated_mentions = list(
        logged_rocket.channels_get_all_user_mentions_by_channel(room_id="GENERAL")
    )
    for mention in iterated_mentions:
        assert "_id" in mention
