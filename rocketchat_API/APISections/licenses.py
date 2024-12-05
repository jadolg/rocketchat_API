from warnings import deprecated

from rocketchat_API.APISections.base import RocketChatBase


class RocketChatLicenses(RocketChatBase):
    @deprecated("Use licenses_info instead")
    def licenses_get(self, **kwargs):
        """Retrieves a list of all registered licenses in the workspace."""
        return self.call_api_get("licenses.get", kwargs=kwargs)

    def licenses_info(self, **kwargs):
        """Retrieves a list of all registered licenses in the workspace."""
        return self.call_api_get("licenses.info", kwargs=kwargs)
