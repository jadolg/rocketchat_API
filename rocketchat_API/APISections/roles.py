from rocketchat_API.APISections.base import RocketChatBase


class RocketChatRoles(RocketChatBase):
    def roles_list(self, **kwargs):
        """Gets all the roles in the system."""
        return self.call_api_get("roles.list", kwargs=kwargs)

    def roles_create(self, name, **kwargs):
        """Create a new role in the system."""
        return self.call_api_post("roles.create", name=name, kwargs=kwargs)
