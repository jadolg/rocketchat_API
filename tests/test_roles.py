import uuid


def test_roles_list(logged_rocket):
    roles_list = logged_rocket.roles_list().json()
    assert roles_list.get("success")
    assert len(roles_list.get("roles")) > 0


def test_roles_create(logged_rocket):
    name = str(uuid.uuid1())
    roles_create = logged_rocket.roles_create(name=name, scope="Subscriptions", description="a test role").json()
    assert roles_create.get("success")
    assert roles_create.get("role").get("name") == name
    assert roles_create.get("role").get("scope") == "Subscriptions"
    assert roles_create.get("role").get("description") == "a test role"
