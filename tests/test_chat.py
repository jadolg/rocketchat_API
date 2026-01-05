import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from tests.conftest import skip_if_no_license


def test_chat_post_notext_message(logged_rocket):
    chat_post_message = logged_rocket.chat_post_message(None, channel="GENERAL")
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == ""


def test_chat_post_update_delete_message(logged_rocket):
    chat_post_message = logged_rocket.chat_post_message(
        "hello",
        channel="GENERAL",
        attachments=[
            {"color": "#ff0000", "text": "there"},
        ],
    )
    assert chat_post_message.get("channel") == "GENERAL"
    assert chat_post_message.get("message").get("msg") == "hello"
    assert (
        chat_post_message.get("message").get("attachments")[0].get("color") == "#ff0000"
    )
    assert chat_post_message.get("message").get("attachments")[0].get("text") == "there"

    with pytest.raises(RocketMissingParamException):
        logged_rocket.chat_post_message(text="text")

    msg_id = chat_post_message.get("message").get("_id")
    chat_get_message = logged_rocket.chat_get_message(msg_id=msg_id)
    assert chat_get_message.get("message").get("_id") == msg_id

    chat_update = logged_rocket.chat_update(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
        text="hello again",
    )

    assert chat_update.get("message").get("msg") == "hello again"

    logged_rocket.chat_delete(
        room_id=chat_post_message.get("channel"),
        msg_id=chat_post_message.get("message").get("_id"),
    )


def test_chat_send_notext_message(logged_rocket):
    chat_send_message = logged_rocket.chat_send_message({"rid": "GENERAL"})
    assert chat_send_message.get("message").get("rid") == "GENERAL"
    assert chat_send_message.get("message").get("msg") == ""
    with pytest.raises(RocketMissingParamException):
        logged_rocket.chat_send_message({"msg": "General Kenobi"})


def test_chat_send_custom_id_delete_message(logged_rocket):
    chat_send_message = logged_rocket.chat_send_message(
        {"rid": "GENERAL", "msg": "Hello There", "_id": "42"}
    )
    assert chat_send_message.get("message").get("rid") == "GENERAL"
    assert chat_send_message.get("message").get("msg") == "Hello There"
    assert chat_send_message.get("message").get("_id") == "42"
    logged_rocket.chat_delete(
        room_id=chat_send_message.get("message").get("rid"),
        msg_id=chat_send_message.get("message").get("_id"),
    )


def test_chat_post_react(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )
    logged_rocket.chat_react(msg_id=message_id)


def test_post_pin_unpin(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )
    chat_pin_message = logged_rocket.chat_pin_message(message_id)
    assert chat_pin_message.get("message").get("t") == "message_pinned"

    logged_rocket.chat_unpin_message(message_id)


def test_post_star_unstar_get_starred_messages(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )

    starred_messages = list(logged_rocket.chat_get_starred_messages(room_id="GENERAL"))
    assert len(starred_messages) == 0

    logged_rocket.chat_star_message(message_id)

    starred_messages = list(logged_rocket.chat_get_starred_messages(room_id="GENERAL"))
    assert len(starred_messages) == 1

    logged_rocket.chat_unstar_message(message_id)


def test_chat_get_message_read_receipts(logged_rocket, skip_if_no_license):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )
    chat_get_message_read_receipts = logged_rocket.chat_get_message_read_receipts(
        message_id=message_id
    )
    assert "receipts" in chat_get_message_read_receipts


def test_chat_report_message(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )
    logged_rocket.chat_report_message(
        message_id=message_id, description="this makes me angry"
    )


def test_chat_follow_message(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message("hello", channel="GENERAL")
        .get("message")
        .get("_id")
    )
    logged_rocket.chat_follow_message(mid=message_id)


# TODO: Rollback the room_id change if https://github.com/RocketChat/Rocket.Chat/issues/35923 works out
def test_chat_get_thread_messages(logged_rocket):
    chat_post_message1 = logged_rocket.chat_post_message(
        "text1",
        channel="GENERAL",
    )
    msg1_id = chat_post_message1.get("message").get("_id")

    chat_post_message2 = logged_rocket.chat_post_message(
        "text2",
        room_id="GENERAL",
        tmid=msg1_id,
    )

    chat_post_message3 = logged_rocket.chat_post_message(
        "text3",
        room_id="GENERAL",
        tmid=msg1_id,
    )

    thread_messages = list(
        logged_rocket.chat_get_thread_messages(
            thread_msg_id=msg1_id,
        )
    )

    # check that correct number of messages is returned
    assert len(thread_messages) == 2

    # check that text of messages are correct and messages are returned in order
    assert thread_messages[0].get("msg") == chat_post_message2.get("message").get("msg")
    assert thread_messages[1].get("msg") == chat_post_message3.get("message").get("msg")


def test_chat_get_mentioned_messages(logged_rocket):
    chat_post_message_with_mention = logged_rocket.chat_post_message(
        "hello @user1",
        channel="GENERAL",
    )
    assert chat_post_message_with_mention.get("channel") == "GENERAL"
    assert "message" in chat_post_message_with_mention
    assert chat_post_message_with_mention.get("message").get("msg") == "hello @user1"

    mentioned_messages = list(
        logged_rocket.chat_get_mentioned_messages(room_id="GENERAL")
    )
    assert len(mentioned_messages) > 0
    assert mentioned_messages[0].get("msg") == "hello @user1"


def test_chat_search(logged_rocket):
    logged_rocket.chat_post_message("unique_search_term_test", channel="GENERAL")

    iterated_messages = list(
        logged_rocket.chat_search(
            room_id="GENERAL", search_text="unique_search_term_test"
        )
    )
    assert len(iterated_messages) > 0

    for message in iterated_messages:
        assert "_id" in message


def test_chat_get_starred_messages(logged_rocket):
    message_id = (
        logged_rocket.chat_post_message(room_id="GENERAL", text="star this message")
        .get("message")
        .get("_id")
    )
    logged_rocket.chat_star_message(msg_id=message_id)
    iterated_messages = list(logged_rocket.chat_get_starred_messages(room_id="GENERAL"))
    for message in iterated_messages:
        assert "_id" in message

    logged_rocket.chat_unstar_message(msg_id=message_id)
