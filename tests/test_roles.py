def test_roles_list(logged_rocket):
    roles_list = logged_rocket.roles_list().json()
    assert roles_list.get("success")
    assert len(roles_list.get("roles")) > 0
