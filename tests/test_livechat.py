import uuid


def test_livechat_rooms(logged_rocket):
    livechat_rooms = logged_rocket.livechat_rooms().json()
    assert livechat_rooms.get("success")
    assert "rooms" in livechat_rooms


def test_livechat_inquiries_list(logged_rocket):
    livechat_inquiries_list = logged_rocket.livechat_inquiries_list().json()
    assert livechat_inquiries_list.get("success")
    assert "inquiries" in livechat_inquiries_list


def test_livechat_inquiries_take(logged_rocket):
    # TODO: Find a way of creating an inquiry to be able to properly test this method
    livechat_inquiries_take = logged_rocket.livechat_inquiries_take(
        inquiry_id="NotARealThing"
    ).json()
    assert not livechat_inquiries_take.get("success")
    assert "Inquiry not found [error-not-found]" == livechat_inquiries_take.get("error")


def test_livechat_users(logged_rocket):
    livechat_users = logged_rocket.livechat_get_users(user_type="agent").json()
    assert livechat_users.get("success")
    assert "users" in livechat_users
    assert len(livechat_users.get("users")) == 0

    username = logged_rocket.me().json().get("username")
    new_user = logged_rocket.livechat_create_user(
        user_type="agent", username=username
    ).json()
    assert new_user.get("success")
    assert "user" in new_user
    assert new_user.get("user").get("username") == username

    livechat_users = logged_rocket.livechat_get_users(user_type="agent").json()
    assert len(livechat_users.get("users")) == 1

    livechat_get_user = logged_rocket.livechat_get_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    ).json()
    assert livechat_get_user.get("success")
    assert new_user.get("user").get("username") == username

    livechat_delete_user = logged_rocket.livechat_delete_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    ).json()
    assert livechat_delete_user.get("success")

    livechat_users = logged_rocket.livechat_get_users(user_type="agent").json()
    assert len(livechat_users.get("users")) == 0


def test_livechat_visitor_minimal(logged_rocket):
    token = str(uuid.uuid1())
    new_visitor = logged_rocket.livechat_register_visitor(token=token).json()
    assert new_visitor.get("success")
    assert "visitor" in new_visitor


def test_livechat_visitor_room_and_message(logged_rocket):
    token = str(uuid.uuid1())
    name = str(uuid.uuid1())
    new_visitor = logged_rocket.livechat_register_visitor(
        token=token, visitor={"username": name}
    ).json()
    assert new_visitor.get("success")
    assert "visitor" in new_visitor

    get_visitor = logged_rocket.livechat_get_visitor(token=token).json()
    assert get_visitor.get("success")
    assert name == get_visitor.get("visitor").get("username")

    # We need to create a livechat agent and set the user online in order to be able to get a room
    username = logged_rocket.me().json().get("username")
    new_user = logged_rocket.livechat_create_user(
        user_type="agent", username=username
    ).json()
    assert new_user.get("success")
    users_set_status = logged_rocket.users_set_status(
        message="working on it", status="online"
    ).json()
    assert users_set_status.get("success")

    livechat_room = logged_rocket.livechat_room(token=token).json()
    assert livechat_room.get("success")
    assert "room" in livechat_room

    livechat_message = logged_rocket.livechat_message(
        token=token,
        rid=livechat_room.get("room").get("_id"),
        msg="may the 4th be with you",
    ).json()

    assert livechat_message.get("success")
    assert "message" in livechat_message
    assert livechat_message.get("message").get("msg") == "may the 4th be with you"

    livechat_messages_history = logged_rocket.livechat_messages_history(
        rid=livechat_room.get("room").get("_id"), token=token
    ).json()
    assert livechat_messages_history.get("success")
    assert "messages" in livechat_messages_history

    livechat_delete_user = logged_rocket.livechat_delete_user(
        user_type="agent", user_id=new_user.get("user").get("_id")
    ).json()
    assert livechat_delete_user.get("success")
