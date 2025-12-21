import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketWrongStatusCodeException,
)


def test_rooms_upload(logged_rocket):
    rooms_upload = logged_rocket.rooms_upload(
        "GENERAL", file="tests/assets/avatar.png", description="hey there"
    )
    assert "message" in rooms_upload
    assert rooms_upload.get("message").get("file").get("format") == "png"
    assert rooms_upload.get("message").get("file").get("name") == "avatar.png"
    assert rooms_upload.get("message").get("file").get("type") == "image/png"


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

    with pytest.raises(RocketWrongStatusCodeException) as exc_info:
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
    rooms_simple = logged_rocket.rooms_admin_rooms()
    assert all(key in rooms_simple for key in ["rooms", "count", "offset", "total"])
    # Using a room type filter does not seem to work
    offset = actual_count = 0
    res = {}
    while res.get("total") is None or res.get("total") > offset:
        res = logged_rocket.rooms_admin_rooms(
            **{
                "types": [
                    "c",
                ],
                "offset": offset,
            }
        )
        offset += res.get("count")
        actual_count += len(list(filter(lambda x: "c" in x["t"], res.get("rooms"))))
    assert res.get("total") == actual_count

    rooms_with_filter = logged_rocket.rooms_admin_rooms(**{"filter": "general"})
    assert rooms_with_filter.get("rooms")[0].get("_id") == "GENERAL"


def test_rooms_leave(logged_rocket, secondary_user):
    with pytest.raises(RocketWrongStatusCodeException) as exc_info:
        logged_rocket.rooms_leave("GENERAL")
    assert "error-you-are-last-owner" in str(exc_info.value)

    name = str(uuid.uuid1())
    channels_create = logged_rocket.channels_create(name)
    logged_rocket.channels_invite(
        room_id=channels_create.get("channel").get("_id"), user_id=secondary_user
    )

    logged_rocket.channels_add_owner(
        channels_create.get("channel").get("_id"), user_id=secondary_user
    )
    logged_rocket.rooms_leave(channels_create.get("channel").get("_id"))
