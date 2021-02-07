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
