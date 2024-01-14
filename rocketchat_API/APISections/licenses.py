from rocketchat_API.APISections.base import RocketChatBase


class RocketChatLicenses(RocketChatBase):
    def licenses_get(self, **kwargs):
        """Retrieves a list of all registered licenses in the workspace."""
        return self.call_api_get("licenses.get", kwargs=kwargs)
