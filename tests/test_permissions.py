def test_permissions_list_all(logged_rocket):
    permissions_list_all = logged_rocket.permissions_list_all()
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all


def test_permissions_list_all_with_updated_since(logged_rocket):
    permissions_list_all = logged_rocket.permissions_list_all(
        updatedSince="2017-11-25T15:08:17.248Z"
    )
    assert "update" in permissions_list_all
    assert "remove" in permissions_list_all


def test_permissions_update(logged_rocket):
    def get_updated_roles(permission, permissions_update):
        for permission_update in permissions_update:
            if permission.get("_id", "A") == permission_update.get("_id", "B"):
                return permission_update.get("roles")

        # Permission not found
        raise ValueError

    def check_update(permissions, permissions_update):
        for permission in permissions:
            try:
                if permission.get("roles") != get_updated_roles(
                    permission, permissions_update
                ):
                    return False
            except ValueError:
                return False

        return True

    permissions = [
        {"_id": "access-permissions", "roles": ["admin", "bot"]},
        {"_id": "add-user-to-any-c-room", "roles": ["admin"]},
    ]
    permissions_update = logged_rocket.permissions_update(permissions=permissions)
    assert check_update(permissions, permissions_update.get("permissions", []))

    permissions_wrong_id = [
        {"_id": "wrong-id", "roles": ["admin", "bot"]},
    ]
    assert (
        check_update(permissions_wrong_id, permissions_update.get("permissions", []))
        is False
    )

    permissions_wrong_roles = [
        {"_id": "access-permissions", "roles": ["bot"]},
    ]
    assert (
        check_update(permissions_wrong_roles, permissions_update.get("permissions", []))
        is False
    )
