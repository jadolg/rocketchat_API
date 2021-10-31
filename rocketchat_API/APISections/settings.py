from rocketchat_API.APISections.base import RocketChatBase


class RocketChatSettings(RocketChatBase):
    def settings_get(self, _id, **kwargs):
        """Gets the setting for the provided _id."""
        return self.call_api_get("settings/" + _id, kwargs=kwargs)

    def settings_update(self, _id, value, **kwargs):
        """Updates the setting for the provided _id."""
        return self.call_api_post("settings/" + _id, value=value, kwargs=kwargs)

    def settings(self, **kwargs):
        """List all private settings."""
        return self.call_api_get("settings", kwargs=kwargs)

    def settings_public(self, **kwargs):
        """List all private settings."""
        return self.call_api_get("settings.public", kwargs=kwargs)

    def settings_oauth(self, **kwargs):
        """List all OAuth services."""
        return self.call_api_get("settings.oauth", kwargs=kwargs)

    def settings_addcustomoauth(self, name, **kwargs):
        """Add a new custom OAuth service with the provided name."""
        return self.call_api_post("settings.addCustomOAuth", name=name, kwargs=kwargs)

    def service_configurations(self, **kwargs):
        """List all service configurations."""
        return self.call_api_get("service.configurations", kwargs=kwargs)
