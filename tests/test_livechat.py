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
    assert "Inquiry already taken" == livechat_inquiries_take.get("reason")


def test_livechat_users(logged_rocket):
    livechat_users = logged_rocket.livechat_get_users(type="agent").json()
    assert livechat_users.get("success")
    assert "users" in livechat_users
    assert len(livechat_users.get("users")) == 0

    username = logged_rocket.me().json().get("username")
    new_user = logged_rocket.livechat_create_user(
        type="agent", username=username
    ).json()
    assert new_user.get("success")
    assert "user" in new_user
    assert new_user.get("user").get("username") == username

    livechat_users = logged_rocket.livechat_get_users(type="agent").json()
    assert len(livechat_users.get("users")) == 1

    livechat_get_user = logged_rocket.livechat_get_user(
        type="agent", id=new_user.get("user").get("_id")
    ).json()
    assert livechat_get_user.get("success")
    assert new_user.get("user").get("username") == username

    livechat_delete_user = logged_rocket.livechat_delete_user(
        type="agent", id=new_user.get("user").get("_id")
    ).json()
    assert livechat_delete_user.get("success")

    livechat_users = logged_rocket.livechat_get_users(type="agent").json()
    assert len(livechat_users.get("users")) == 0
