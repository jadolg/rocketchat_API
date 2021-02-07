def test_livechat_rooms(logged_rocket):
    livechat_rooms = logged_rocket.livechat_rooms().json()
    assert livechat_rooms.get("success")
    assert "rooms" in livechat_rooms
