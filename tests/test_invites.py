def test_find_or_create_invite(logged_rocket):
    rid = "GENERAL"
    find_or_create_invite = logged_rocket.find_or_create_invite(
        rid=rid, days=7, max_uses=5
    ).json()
    assert find_or_create_invite.get("success")
    assert find_or_create_invite.get("days") == 7
    assert find_or_create_invite.get("maxUses") == 5


def test_list_invites(logged_rocket):
    list_invites = logged_rocket.list_invites().json()
    assert isinstance(list_invites, list)
