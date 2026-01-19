import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketApiException


def test_livechat_rooms(logged_rocket):
    logged_rocket.livechat_rooms()


def test_livechat_inquiries_list(logged_rocket):
    logged_rocket.livechat_inquiries_list()


def test_livechat_inquiries_take(logged_rocket):
    # TODO: Find a way of creating an inquiry to be able to properly test this method
    with pytest.raises(RocketApiException) as exc_info:
        logged_rocket.livechat_inquiries_take(inquiry_id="NotARealThing")
    assert "error-not-found" == exc_info.value.error_type
    assert "Inquiry not found" in exc_info.value.error


def test_livechat_users(logged_rocket):
    iterated_users = list(logged_rocket.livechat_get_users(user_type="agent"))
    assert len(iterated_users) == 0

    username = logged_rocket.me().get("username")
    new_user = logged_rocket.livechat_create_user(user_type="agent", username=username)
    assert "user" in new_user
    assert new_user.get("user").get("username") == username

    iterated_users = list(logged_rocket.livechat_get_users(user_type="agent"))
    assert len(iterated_users) == 1

    livechat_get_user = logged_rocket.livechat_get_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    )
    assert livechat_get_user.get("user").get("username") == username

    logged_rocket.livechat_delete_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    )

    iterated_users = list(logged_rocket.livechat_get_users(user_type="agent"))
    assert len(iterated_users) == 0


def test_livechat_visitor_minimal(logged_rocket):
    token = str(uuid.uuid1())
    new_visitor = logged_rocket.livechat_register_visitor(token=token)
    assert "visitor" in new_visitor


def test_livechat_visitor_room_and_message(logged_rocket):
    token = str(uuid.uuid1())
    name = str(uuid.uuid1())
    new_visitor = logged_rocket.livechat_register_visitor(
        token=token, visitor={"username": name}
    )
    assert "visitor" in new_visitor

    get_visitor = logged_rocket.livechat_get_visitor(token=token)
    assert name == get_visitor.get("visitor").get("username")

    # We need to create a livechat agent and set the user online in order to be able to get a room
    username = logged_rocket.me().get("username")
    new_user = logged_rocket.livechat_create_user(user_type="agent", username=username)
    logged_rocket.users_set_status(message="working on it", status="online")

    livechat_room = logged_rocket.livechat_room(token=token)
    assert "room" in livechat_room

    livechat_message = logged_rocket.livechat_message(
        token=token,
        rid=livechat_room.get("room").get("_id"),
        msg="may the 4th be with you",
    )

    assert "message" in livechat_message
    assert livechat_message.get("message").get("msg") == "may the 4th be with you"

    livechat_messages_history = logged_rocket.livechat_messages_history(
        rid=livechat_room.get("room").get("_id"), token=token
    )
    assert "messages" in livechat_messages_history

    logged_rocket.livechat_delete_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    )


def test_livechat_get_users(logged_rocket):
    # Create an agent first
    username = logged_rocket.me().get("username")
    new_user = logged_rocket.livechat_create_user(user_type="agent", username=username)

    iterated_users = list(logged_rocket.livechat_get_users(user_type="agent"))
    assert len(iterated_users) > 0, "Should have at least one agent"

    for user in iterated_users:
        assert "_id" in user

    # Cleanup
    logged_rocket.livechat_delete_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    )
