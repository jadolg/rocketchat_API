from rocketchat_API.APISections.base import RocketChatBase


class RocketChatRoles(RocketChatBase):
    def roles_list(self, **kwargs):
        """Gets all the roles in the system."""
        return self.call_api_get("roles.list", kwargs=kwargs)

    def roles_create(self, name, **kwargs):
        """Create a new role in the system."""
        return self.call_api_post("roles.create", name=name, kwargs=kwargs)

    def roles_add_user_to_role(self, role_name, username, **kwargs):
        """Assign a role to a user. Optionally, you can set this role to a room."""
        return self.call_api_post(
            "roles.addUserToRole", roleName=role_name, username=username, kwargs=kwargs
        )

    def roles_remove_user_from_role(self, role_name, username, **kwargs):
        """Remove a role from a user. Optionally, you can unset this role for a specified scope."""
        return self.call_api_post(
            "roles.removeUserFromRole",
            roleName=role_name,
            username=username,
            kwargs=kwargs,
        )

    def roles_get_users_in_role(self, role, **kwargs):
        """Gets the users that belongs to a role. It supports the Offset and Count Only."""
        return self.call_api_get("roles.getUsersInRole", role=role, kwargs=kwargs)

    def roles_sync(self, updated_since):
        """Gets all the roles in the system which are updated after a given date."""
        return self.call_api_get("roles.sync", updatedSince=updated_since)
