import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketApiException,
)


@pytest.fixture
def testuser_id(logged_rocket):
    try:
        testuser = logged_rocket.users_info(username="testuser1")
    except RocketApiException as e:
        if e.error == "User not found":
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


@pytest.fixture
def test_group_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_group_id(test_group_name, logged_rocket):
    _test_group_id = (
        logged_rocket.groups_create(test_group_name).get("group").get("_id")
    )

    return _test_group_id


def test_groups_list_all(logged_rocket):
    iterated_groups = list(logged_rocket.groups_list_all())
    assert len(iterated_groups) > 0, "Should have at least one group"

    for group in iterated_groups:
        assert "_id" in group
        assert "name" in group

    iterated_groups_custom = list(logged_rocket.groups_list_all(count=1))
    assert len(iterated_groups_custom) > 0

    for group in logged_rocket.groups_list_all():
        assert "_id" in group


def test_groups_list(logged_rocket):
    iterated_groups = list(logged_rocket.groups_list())
    for group in iterated_groups:
        assert "_id" in group
        assert "name" in group


def test_groups_info(logged_rocket, test_group_name, test_group_id):
    groups_info_by_id = logged_rocket.groups_info(room_id=test_group_id)
    assert "group" in groups_info_by_id
    assert groups_info_by_id.get("group").get("_id") == test_group_id

    groups_info_by_name = logged_rocket.groups_info(room_name=test_group_name)
    assert "group" in groups_info_by_name
    assert groups_info_by_name.get("group").get("_id") == test_group_id

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_info()


def test_groups_history(logged_rocket, test_group_id):
    logged_rocket.chat_post_message(
        room_id=test_group_id, text="Testing groups_history"
    )

    # Test with positional argument
    for message in logged_rocket.groups_history(test_group_id):
        assert "_id" in message
        assert "msg" in message
        assert message.get("msg") == "Testing groups_history"

    # Test with keyword argument
    for message in logged_rocket.groups_history(room_id=test_group_id):
        assert "_id" in message
        assert "msg" in message
        assert message.get("msg") == "Testing groups_history"


def test_groups_add_and_remove_moderator(logged_rocket, test_group_id):
    me = logged_rocket.me()
    logged_rocket.groups_add_moderator(test_group_id, me.get("_id"))
    logged_rocket.groups_remove_moderator(test_group_id, me.get("_id"))


def test_groups_add_and_remove_leader(logged_rocket, test_group_id):
    me = logged_rocket.me()
    logged_rocket.groups_add_leader(test_group_id, me.get("_id"))
    logged_rocket.groups_remove_leader(test_group_id, me.get("_id"))


def test_groups_list_moderator(logged_rocket, test_group_name, test_group_id):
    me = logged_rocket.me()
    logged_rocket.groups_add_moderator(test_group_id, me.get("_id"))
    groups_list_moderator = logged_rocket.groups_moderators(room_id=test_group_id)
    assert "moderators" in groups_list_moderator
    assert groups_list_moderator.get("moderators")[0].get("_id") == me.get("_id")
    logged_rocket.groups_remove_moderator(test_group_id, me.get("_id"))
    groups_list_moderator_by_name = logged_rocket.groups_moderators(
        group=test_group_name
    )
    assert "moderators" in groups_list_moderator_by_name
    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_moderators()


def test_groups_add_and_remove_owner(logged_rocket, testuser_id, test_group_id):
    logged_rocket.groups_invite(test_group_id, testuser_id)
    logged_rocket.groups_add_owner(test_group_id, user_id=testuser_id)
    another_owner_id = logged_rocket.users_info(username="user1").get("user").get("_id")
    try:  # When running several times we don't clean this up so it's fine if it fails after
        logged_rocket.groups_add_owner(test_group_id, user_id=another_owner_id)
    except RocketApiException:
        pass
    logged_rocket.groups_remove_owner(test_group_id, user_id=testuser_id)


def test_groups_archive_unarchive(logged_rocket, test_group_id):
    logged_rocket.groups_archive(test_group_id)
    logged_rocket.groups_unarchive(test_group_id)


def test_groups_close_open(logged_rocket, test_group_id):
    logged_rocket.groups_close(test_group_id)
    logged_rocket.groups_open(test_group_id)


def test_groups_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name)
    assert name == groups_create.get("group").get("name")
    logged_rocket.groups_delete(group=name)
    groups_create = logged_rocket.groups_create(name)
    room_id = groups_create.get("group").get("_id")
    logged_rocket.groups_delete(room_id=room_id)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_delete()


def test_groups_get_integrations(logged_rocket, test_group_id):
    groups_get_integrations = logged_rocket.groups_get_integrations(
        room_id=test_group_id
    )
    assert "integrations" in groups_get_integrations


def test_groups_invite(logged_rocket, testuser_id, test_group_id):
    groups_invite = logged_rocket.groups_invite(test_group_id, testuser_id)
    assert "group" in groups_invite
    assert groups_invite.get("group").get("_id") == test_group_id


def test_groups_kick(logged_rocket, testuser_id):
    id_group_created = (
        logged_rocket.groups_create(str(uuid.uuid1())).get("group").get("_id")
    )
    groups_invite = logged_rocket.groups_invite(id_group_created, testuser_id)
    assert "group" in groups_invite
    assert groups_invite.get("group").get("_id") == id_group_created
    logged_rocket.groups_kick(id_group_created, testuser_id)


def test_groups_leave(logged_rocket, test_group_id, testuser_id):
    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.groups_leave(test_group_id)

    assert "error-you-are-last-owner" == str(exc_info.value.error_type)
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name)
    logged_rocket.groups_invite(
        room_id=groups_create.get("group").get("_id"), user_id=testuser_id
    )
    logged_rocket.groups_add_owner(
        groups_create.get("group").get("_id"), user_id=testuser_id
    )
    logged_rocket.groups_leave(groups_create.get("group").get("_id"))


def test_groups_rename(logged_rocket):
    name = str(uuid.uuid1())
    name2 = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name)
    groups_rename = logged_rocket.groups_rename(
        room_id=groups_create.get("group").get("_id"), name=name2
    )
    assert groups_rename.get("group").get("name") == name2


def test_groups_set_announcement(logged_rocket, test_group_id):
    announcement = str(uuid.uuid1())
    groups_set_announcement = logged_rocket.groups_set_announcement(
        test_group_id, announcement
    )
    assert (
        groups_set_announcement.get("announcement") == announcement
    ), "Announcement does not match"


def test_groups_set_description(logged_rocket, test_group_id):
    description = str(uuid.uuid1())
    groups_set_description = logged_rocket.groups_set_description(
        test_group_id, description
    )
    assert (
        groups_set_description.get("description") == description
    ), "Description does not match"


def test_groups_set_read_only(logged_rocket, test_group_id):
    logged_rocket.groups_set_read_only(test_group_id, True)
    logged_rocket.groups_set_read_only(test_group_id, False)


def test_groups_set_topic(logged_rocket, test_group_id):
    topic = str(uuid.uuid1())
    groups_set_topic = logged_rocket.groups_set_topic(test_group_id, topic)
    assert groups_set_topic.get("topic") == topic, "Topic does not match"


def test_groups_set_type(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name)

    groups_set_type = logged_rocket.groups_set_type(
        groups_create.get("group").get("_id"), "c"
    )
    assert groups_set_type.get("group").get("t"), "p"

    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.groups_set_type(groups_create.get("group").get("_id"), "p")
    assert exc_info.value.error_type == "error-room-not-found"


def test_groups_set_custom_fields(
    logged_rocket,
    test_group_id,
    test_group_name,
):
    field_name = str(uuid.uuid1())
    field_value = str(uuid.uuid1())
    custom_fields = {field_name: field_value}

    groups_set_custom_fields = logged_rocket.groups_set_custom_fields(
        custom_fields, room_id=test_group_id
    )
    assert (
        groups_set_custom_fields.get("group").get("customFields") == custom_fields
    ), "Custom fields do not match"

    groups_set_custom_fields = logged_rocket.groups_set_custom_fields(
        custom_fields, room_name=test_group_name
    )
    assert (
        groups_set_custom_fields.get("group").get("customFields") == custom_fields
    ), "Custom fields do not match"

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_set_custom_fields(custom_fields)


def test_groups_roles(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name)

    groups_roles = logged_rocket.groups_roles(
        room_id=groups_create.get("group").get("_id")
    )
    assert groups_roles.get("roles") is not None

    groups_roles = logged_rocket.groups_roles(room_name=name)
    assert groups_roles.get("roles") is not None

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_roles()


def test_groups_files(logged_rocket, test_group_name, test_group_id):
    rooms_upload = logged_rocket.rooms_media(
        room_id=test_group_id, file="tests/assets/avatar.png", description="hey there"
    )
    assert "file" in rooms_upload

    iterated_files = list(logged_rocket.groups_files(room_id=test_group_id))
    for file in iterated_files:
        assert "_id" in file

    iterated_files_name = list(logged_rocket.groups_files(room_name=test_group_name))
    assert iterated_files_name == iterated_files

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_files()


def test_groups_members(logged_rocket, test_group_name, test_group_id):
    iterated_members = list(logged_rocket.groups_members(room_id=test_group_id))
    iterated_members_room_name = list(
        logged_rocket.groups_members(group=test_group_name)
    )
    assert len(iterated_members) > 0, "Should have at least one member"
    assert iterated_members_room_name == iterated_members

    for member in iterated_members:
        assert "_id" in member
        assert "username" in member

    # Test with custom count parameter
    iterated_members_custom = list(
        logged_rocket.groups_members(room_id=test_group_id, count=1)
    )
    assert len(iterated_members_custom) > 0

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_members()
