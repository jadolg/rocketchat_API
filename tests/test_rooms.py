import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketApiException,
)


def test_rooms_media(logged_rocket):
    rooms_media = logged_rocket.rooms_media(
        "GENERAL", file="tests/assets/avatar.png", description="hey there"
    )
    assert str(rooms_media.get("file").get("url")).endswith("avatar.png")


def test_rooms_get(logged_rocket):
    rooms_get = logged_rocket.rooms_get()
    assert "update" in rooms_get
    assert "remove" in rooms_get


def test_rooms_clean_history(logged_rocket):
    rooms_clean_history = logged_rocket.rooms_clean_history(
        room_id="GENERAL",
        latest="2016-09-30T13:42:25.304Z",
        oldest="2016-05-30T13:42:25.304Z",
    )
    assert rooms_clean_history.get("_id") == "GENERAL"
    assert "count" in rooms_clean_history


def test_rooms_favorite(logged_rocket):
    logged_rocket.rooms_favorite(room_id="GENERAL", favorite=True)
    logged_rocket.rooms_favorite(room_name="general", favorite=True)

    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.rooms_favorite(room_id="unexisting_channel", favorite=True)
    assert "error-room-not-found" in str(exc_info.value)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.rooms_favorite()


def test_rooms_info(logged_rocket):
    rooms_infoby_name = logged_rocket.rooms_info(room_name="general")
    assert rooms_infoby_name.get("room").get("_id") == "GENERAL"
    rooms_info_by_id = logged_rocket.rooms_info(room_id="GENERAL")
    assert rooms_info_by_id.get("room").get("_id") == "GENERAL"
    with pytest.raises(RocketMissingParamException):
        logged_rocket.rooms_info()


def test_rooms_create_discussion(logged_rocket):
    discussion_name = "this is a discussion"
    rooms_create_discussion = logged_rocket.rooms_create_discussion(
        prid="GENERAL",
        t_name=discussion_name,
    )
    assert "discussion" in rooms_create_discussion
    assert rooms_create_discussion.get("discussion").get("fname") == discussion_name


def test_rooms_admin_rooms(logged_rocket):
    iterated_rooms = list(logged_rocket.rooms_admin_rooms())
    assert len(iterated_rooms) > 0, "Should have at least one room"

    for room in iterated_rooms:
        assert "_id" in room
        assert "t" in room

    # Test with custom count parameter
    iterated_rooms_custom = list(logged_rocket.rooms_admin_rooms(count=1))
    assert len(iterated_rooms_custom) > 0

    rooms_with_filter = list(logged_rocket.rooms_admin_rooms(filter="general"))
    assert len(rooms_with_filter) == 1


def test_rooms_leave(logged_rocket, secondary_user):
    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.rooms_leave("GENERAL")
    assert exc_info.value.error_type == "error-you-are-last-owner"

    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    logged_rocket.channels_invite(
        room_id=channels_create.get("channel").get("_id"), user_id=secondary_user
    )

    logged_rocket.channels_add_owner(
        channels_create.get("channel").get("_id"), user_id=secondary_user
    )
    logged_rocket.rooms_leave(channels_create.get("channel").get("_id"))
