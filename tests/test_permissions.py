def test_permissions_list_all(logged_rocket):
    permissions_list_all = logged_rocket.permissions_list_all().json()
    assert permissions_list_all.get("success")
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all


def test_permissions_list_all_with_updatedSince(logged_rocket):
    permissions_list_all = logged_rocket.permissions_list_all(
        updatedSince="2017-11-25T15:08:17.248Z"
    ).json()
    assert permissions_list_all.get("success")
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all
