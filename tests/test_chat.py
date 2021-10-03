import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


def test_chat_post_notext_message(logged_rocket):
    chat_post_message = logged_rocket.chat_post_message(None, channel="GENERAL").json()
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == ""
    assert chat_post_message.get("success")


def test_chat_post_update_delete_message(logged_rocket):
    chat_post_message = logged_rocket.chat_post_message(
        "hello", channel="GENERAL"
    ).json()
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == "hello"
    assert chat_post_message.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.chat_post_message(text="text")

    msg_id = chat_post_message.get("message").get("_id")
    chat_get_message = logged_rocket.chat_get_message(msg_id=msg_id).json()
    assert chat_get_message.get("message").get("_id") == msg_id

    chat_update = logged_rocket.chat_update(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
        text="hello again",
    ).json()

    assert chat_update.get("message").get("msg") == "hello again"
    assert chat_update.get("success")

    chat_delete = logged_rocket.chat_delete(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
    ).json()
    assert chat_delete.get("success")


def test_chat_send_notext_message(logged_rocket):
    chat_send_message = logged_rocket.chat_send_message({"rid": "GENERAL"}).json()
    assert chat_send_message.get("message").get("rid") == "GENERAL"
    assert chat_send_message.get("message").get("msg") == ""
    assert chat_send_message.get("success")
    with pytest.raises(RocketMissingParamException):
        logged_rocket.chat_send_message({"msg": "General Kenobi"})


def test_chat_send_custom_id_delete_message(logged_rocket):
    chat_send_message = logged_rocket.chat_send_message(
        {"rid": "GENERAL", "msg": "Hello There", "_id": "42"}
    ).json()
    assert chat_send_message.get("message").get("rid") == "GENERAL"
    assert chat_send_message.get("message").get("msg") == "Hello There"
    assert chat_send_message.get("message").get("_id") == "42"
    assert chat_send_message.get("success")
    chat_delete = logged_rocket.chat_delete(
        room_id=chat_send_message.get("message").get("rid"),
        msg_id=chat_send_message.get("message").get("_id"),
    ).json()
    assert chat_delete.get("success")


def test_chat_post_react(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_react = logged_rocket.chat_react(msg_id=message_id).json()
    assert chat_react.get("success")


def test_post_pin_unpin(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_pin_message = logged_rocket.chat_pin_message(message_id).json()
    assert chat_pin_message.get("success")
    assert chat_pin_message.get("message").get("t") == "message_pinned"

    chat_unpin_message = logged_rocket.chat_unpin_message(message_id).json()
    assert chat_unpin_message.get("success")


def test_post_star_unstar_get_starred_messages(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )

    chat_get_starred_messages = logged_rocket.chat_get_starred_messages(
        room_id="GENERAL"
    ).json()
    assert chat_get_starred_messages.get("success")
    assert chat_get_starred_messages.get("count") == 0
    assert chat_get_starred_messages.get("messages") == []

    chat_star_message = logged_rocket.chat_star_message(message_id).json()
    assert chat_star_message.get("success")

    chat_get_starred_messages = logged_rocket.chat_get_starred_messages(
        room_id="GENERAL"
    ).json()
    assert chat_get_starred_messages.get("success")
    assert chat_get_starred_messages.get("count") == 1
    assert chat_get_starred_messages.get("messages") != []

    chat_unstar_message = logged_rocket.chat_unstar_message(message_id).json()
    assert chat_unstar_message.get("success")


def test_chat_search(logged_rocket):
    chat_search = logged_rocket.chat_search(
        room_id="GENERAL", search_text="hello"
    ).json()
    assert chat_search.get("success")


def test_chat_get_message_read_receipts(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_read_receipts = logged_rocket.chat_get_message_read_receipts(
        message_id=message_id
    ).json()
    assert chat_get_message_read_receipts.get("success")
    assert "receipts" in chat_get_message_read_receipts


def test_chat_report_message(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_report_message = logged_rocket.chat_report_message(
        message_id=message_id, description="this makes me angry"
    ).json()
    assert chat_get_message_report_message.get("success")


def test_chat_follow_message(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .json()
        .get("message")
        .get("_id")
    )
    chat_get_message_follow_message = logged_rocket.chat_follow_message(
        mid=message_id
    ).json()
    assert chat_get_message_follow_message.get("success")
