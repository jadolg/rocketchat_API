import uuid


def test_roles_list(logged_rocket):
    roles_list = logged_rocket.roles_list().json()
    assert roles_list.get("success")
    assert len(roles_list.get("roles")) > 0


def test_roles_create(logged_rocket, skip_if_no_license):
    name = str(uuid.uuid1())
    roles_create = logged_rocket.roles_create(
        name=name, scope="Subscriptions", description="a test role"
    ).json()
    assert roles_create.get("success")
    assert roles_create.get("role").get("name") == name
    assert roles_create.get("role").get("scope") == "Subscriptions"
    assert roles_create.get("role").get("description") == "a test role"


def test_roles_add_remove_user_to_from_role(logged_rocket):
    me = logged_rocket.me().json()
    roles_add_user_to_role = logged_rocket.roles_add_user_to_role(
        role_name="livechat-agent", username=me.get("username")
    ).json()
    assert roles_add_user_to_role.get("success")
    assert roles_add_user_to_role.get("role").get("name") == "livechat-agent"

    roles_remove_user_from_role = logged_rocket.roles_remove_user_from_role(
        role_name="livechat-agent", username=me.get("username")
    ).json()

    assert roles_remove_user_from_role.get("success")


def test_roles_get_users_in_role(logged_rocket):
    roles_get_users_in_role = logged_rocket.roles_get_users_in_role(
        role="owner", roomId="GENERAL"
    ).json()

    assert roles_get_users_in_role.get("success")
    assert roles_get_users_in_role.get("users")[0].get("name") == "user1"


def test_roles_sync(logged_rocket):
    roles_sync = logged_rocket.roles_sync(
        updated_since="2017-11-25T15:08:17.248Z"
    ).json()
    assert roles_sync.get("success")
    assert len(roles_sync.get("roles")) > 0
