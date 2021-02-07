def test_livechat_rooms(logged_rocket):
    livechat_rooms = logged_rocket.livechat_rooms().json()
    assert livechat_rooms.get("success")
    assert "rooms" in livechat_rooms


def test_livechat_inquiries_list(logged_rocket):
    livechat_inquiries_list = logged_rocket.livechat_inquiries_list().json()
    assert livechat_inquiries_list.get("success")
    assert "inquiries" in livechat_inquiries_list
