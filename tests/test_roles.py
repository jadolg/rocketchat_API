import uuid


def test_roles_list(logged_rocket):
    roles_list = logged_rocket.roles_list()
    assert len(roles_list.get("roles")) > 0


def test_roles_create(logged_rocket, skip_if_no_license):
    name = str(uuid.uuid1())
    roles_create = logged_rocket.roles_create(
        name=name, scope="Subscriptions", description="a test role"
    )
    assert roles_create.get("role").get("name") == name
    assert roles_create.get("role").get("scope") == "Subscriptions"
    assert roles_create.get("role").get("description") == "a test role"


def test_roles_add_remove_user_to_from_role(logged_rocket):
    me = logged_rocket.me()
    role_name = str(uuid.uuid1())
    role_id = logged_rocket.roles_create(name=role_name).get("role").get("_id")
    roles_add_user_to_role = logged_rocket.roles_add_user_to_role(
        role_id=role_id, username=me.get("username")
    )
    assert roles_add_user_to_role.get("role").get("name") == role_name
    assert roles_add_user_to_role.get("role").get("_id") == role_id

    roles_remove_user_from_role = logged_rocket.roles_remove_user_from_role(
        role_id=role_id, username=me.get("username")
    )
    assert "role" in roles_remove_user_from_role
    assert roles_remove_user_from_role.get("role").get("name") == role_name


def test_roles_get_users_in_role(logged_rocket):
    iterated_users = list(
        logged_rocket.roles_get_users_in_role(role="owner", roomId="GENERAL")
    )
    assert len(iterated_users) > 0, "Should have at least one owner"

    for user in iterated_users:
        assert "_id" in user
        assert "name" in user

    # Verify the admin/owner user is in the list
    assert any(user.get("name") == "user1" for user in iterated_users)


def test_roles_sync(logged_rocket):
    roles_sync = logged_rocket.roles_sync(updated_since="2017-11-25T15:08:17.248Z")
    assert len(roles_sync.get("roles")) > 0
