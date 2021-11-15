import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


@pytest.fixture
def testuser_id(logged_rocket):
    testuser = logged_rocket.users_info(username="testuser1").json()
    if not testuser.get("success"):
        testuser = logged_rocket.users_create(
            "testuser1@domain.com", "testuser1", "password", "testuser1"
        ).json()

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    logged_rocket.users_delete(_testuser_id)


@pytest.fixture
def test_group_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_group_id(test_group_name, logged_rocket):
    _test_group_id = (
        logged_rocket.groups_create(test_group_name).json().get("group").get("_id")
    )

    return _test_group_id


def test_groups_list_all(logged_rocket):
    groups_list = logged_rocket.groups_list_all().json()
    assert groups_list.get("success")
    assert "groups" in groups_list


def test_groups_list(logged_rocket):
    groups_list = logged_rocket.groups_list().json()
    assert groups_list.get("success")
    assert "groups" in groups_list


def test_groups_info(logged_rocket, test_group_name, test_group_id):
    groups_info_by_id = logged_rocket.groups_info(room_id=test_group_id).json()
    assert groups_info_by_id.get("success")
    assert "group" in groups_info_by_id
    assert groups_info_by_id.get("group").get("_id") == test_group_id

    groups_info_by_name = logged_rocket.groups_info(room_name=test_group_name).json()
    assert groups_info_by_name.get("success")
    assert "group" in groups_info_by_name
    assert groups_info_by_name.get("group").get("_id") == test_group_id

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_info()


def test_groups_history(logged_rocket, test_group_id):
    groups_history = logged_rocket.groups_history(room_id=test_group_id).json()
    assert groups_history.get("success")
    assert "messages" in groups_history


def test_groups_add_and_remove_moderator(logged_rocket, test_group_id):
    me = logged_rocket.me().json()
    groups_add_moderator = logged_rocket.groups_add_moderator(
        test_group_id, me.get("_id")
    ).json()
    assert groups_add_moderator.get("success")
    groups_remove_moderator = logged_rocket.groups_remove_moderator(
        test_group_id, me.get("_id")
    ).json()
    assert groups_remove_moderator.get("success")


def test_groups_add_and_remove_leader(logged_rocket, test_group_id):
    me = logged_rocket.me().json()
    groups_add_leader = logged_rocket.groups_add_leader(
        test_group_id, me.get("_id")
    ).json()
    assert groups_add_leader.get("success")
    groups_remove_leader = logged_rocket.groups_remove_leader(
        test_group_id, me.get("_id")
    ).json()
    assert groups_remove_leader.get("success")


def test_groups_list_moderator(logged_rocket, test_group_name, test_group_id):
    groups_list_moderator = logged_rocket.groups_moderators(
        room_id=test_group_id
    ).json()
    assert groups_list_moderator.get("success")
    groups_list_moderator_by_name = logged_rocket.groups_moderators(
        group=test_group_name
    ).json()
    assert groups_list_moderator_by_name.get("success")
    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_moderators()


def test_groups_add_and_remove_owner(logged_rocket, testuser_id, test_group_id):
    logged_rocket.groups_invite(test_group_id, testuser_id)
    groups_add_owner = logged_rocket.groups_add_owner(
        test_group_id, user_id=testuser_id
    ).json()
    assert groups_add_owner.get("success"), groups_add_owner.get("error")

    groups_remove_owner = logged_rocket.groups_remove_owner(
        test_group_id, user_id=testuser_id
    ).json()
    assert groups_remove_owner.get("success"), groups_remove_owner.get("error")


def test_groups_archive_unarchive(logged_rocket, test_group_id):
    groups_archive = logged_rocket.groups_archive(test_group_id).json()
    assert groups_archive.get("success")
    groups_unarchive = logged_rocket.groups_unarchive(test_group_id).json()
    assert groups_unarchive.get("success")


def test_groups_close_open(logged_rocket, test_group_id):
    groups_close = logged_rocket.groups_close(test_group_id).json()
    assert groups_close.get("success")
    groups_open = logged_rocket.groups_open(test_group_id).json()
    assert groups_open.get("success")


def test_groups_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    assert groups_create.get("success")
    assert name == groups_create.get("group").get("name")
    groups_delete = logged_rocket.groups_delete(group=name).json()
    assert groups_delete.get("success")
    groups_create = logged_rocket.groups_create(name).json()
    assert groups_create.get("success")
    room_id = groups_create.get("group").get("_id")
    groups_delete = logged_rocket.groups_delete(room_id=room_id).json()
    assert groups_delete.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_delete()


def test_groups_get_integrations(logged_rocket, test_group_id):
    groups_get_integrations = logged_rocket.groups_get_integrations(
        room_id=test_group_id
    ).json()
    assert groups_get_integrations.get("success")


def test_groups_invite(logged_rocket, testuser_id, test_group_id):
    groups_invite = logged_rocket.groups_invite(test_group_id, testuser_id).json()
    assert groups_invite.get("success")


def test_groups_kick(logged_rocket, testuser_id):
    id_group_created = (
        logged_rocket.groups_create(str(uuid.uuid1())).json().get("group").get("_id")
    )
    groups_invite = logged_rocket.groups_invite(id_group_created, testuser_id).json()
    assert groups_invite.get("success")
    groups_kick = logged_rocket.groups_kick(id_group_created, testuser_id).json()
    assert groups_kick.get("success")


def test_groups_leave(logged_rocket, test_group_id, testuser_id):
    groups_leave = logged_rocket.groups_leave(test_group_id).json()
    assert not groups_leave.get("success")
    assert groups_leave.get("errorType") == "error-you-are-last-owner"

    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    logged_rocket.groups_invite(
        room_id=groups_create.get("group").get("_id"), user_id=testuser_id
    )
    logged_rocket.groups_add_owner(
        groups_create.get("group").get("_id"), user_id=testuser_id
    ).json()
    groups_leave = logged_rocket.groups_leave(
        groups_create.get("group").get("_id")
    ).json()
    assert groups_leave.get("success")


def test_groups_rename(logged_rocket):
    name = str(uuid.uuid1())
    name2 = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    groups_rename = logged_rocket.groups_rename(
        room_id=groups_create.get("group").get("_id"), name=name2
    ).json()
    assert groups_rename.get("success")
    assert groups_rename.get("group").get("name") == name2


def test_groups_set_announcement(logged_rocket, test_group_id):
    announcement = str(uuid.uuid1())
    groups_set_announcement = logged_rocket.groups_set_announcement(
        test_group_id, announcement
    ).json()
    assert groups_set_announcement.get("success")
    assert (
        groups_set_announcement.get("announcement") == announcement
    ), "Announcement does not match"


def test_groups_set_description(logged_rocket, test_group_id):
    description = str(uuid.uuid1())
    groups_set_description = logged_rocket.groups_set_description(
        test_group_id, description
    ).json()
    assert groups_set_description.get("success")
    assert (
        groups_set_description.get("description") == description
    ), "Description does not match"


def test_groups_set_read_only(logged_rocket, test_group_id):
    groups_set_read_only = logged_rocket.groups_set_read_only(
        test_group_id, True
    ).json()
    assert groups_set_read_only.get("success")
    groups_set_read_only = logged_rocket.groups_set_read_only(
        test_group_id, False
    ).json()
    assert groups_set_read_only.get("success")


def test_groups_set_topic(logged_rocket, test_group_id):
    topic = str(uuid.uuid1())
    groups_set_topic = logged_rocket.groups_set_topic(test_group_id, topic).json()
    assert groups_set_topic.get("success")
    assert groups_set_topic.get("topic") == topic, "Topic does not match"


def test_groups_set_type(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    assert groups_create.get("success")

    groups_set_type = logged_rocket.groups_set_type(
        groups_create.get("group").get("_id"), "c"
    ).json()
    assert groups_set_type.get("success")
    assert groups_set_type.get("group").get("t"), "p"

    groups_set_type = logged_rocket.groups_set_type(
        groups_create.get("group").get("_id"), "p"
    ).json()
    # should fail because this is no more a group
    assert not groups_set_type.get("success")


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
    ).json()
    assert groups_set_custom_fields.get("success")
    assert (
        groups_set_custom_fields.get("group").get("customFields") == custom_fields
    ), "Custom fields do not match"

    groups_set_custom_fields = logged_rocket.groups_set_custom_fields(
        custom_fields, room_name=test_group_name
    ).json()
    assert groups_set_custom_fields.get("success")
    assert (
        groups_set_custom_fields.get("group").get("customFields") == custom_fields
    ), "Custom fields do not match"

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_set_custom_fields(custom_fields)


def test_groups_members(logged_rocket, test_group_name, test_group_id):
    groups_members = logged_rocket.groups_members(room_id=test_group_id).json()
    assert groups_members.get("success")
    groups_members = logged_rocket.groups_members(group=test_group_name).json()
    assert groups_members.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_members()


def test_groups_roles(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    assert groups_create.get("success")

    groups_roles = logged_rocket.groups_roles(
        room_id=groups_create.get("group").get("_id")
    ).json()
    assert groups_roles.get("success")
    assert groups_roles.get("roles") is not None

    groups_roles = logged_rocket.groups_roles(room_name=name).json()
    assert groups_roles.get("success")
    assert groups_roles.get("roles") is not None

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_roles()


def test_groups_files(logged_rocket):
    name = str(uuid.uuid1())
    groups_create = logged_rocket.groups_create(name).json()
    assert groups_create.get("success")

    groups_files = logged_rocket.groups_files(
        room_id=groups_create.get("group").get("_id")
    ).json()
    assert groups_files.get("success")

    groups_files = logged_rocket.groups_files(room_name=name).json()
    assert groups_files.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.groups_files()
