import logging

from rocketchat_API.APISections.base import RocketChatBase


class RocketChatLicenses(RocketChatBase):
    def licenses_get(self, **kwargs):
        """Retrieves a list of all registered licenses in the workspace."""
        logging.warning(
            "The method licenses.get is deprecated and will be removed in version 7 of Rocket.Chat"
        )
        return self.call_api_get("licenses.get", kwargs=kwargs)

    def licenses_info(self, **kwargs):
        """Retrieves a list of all registered licenses in the workspace."""
        return self.call_api_get("licenses.info", kwargs=kwargs)
