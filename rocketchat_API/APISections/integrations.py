from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketUnsuportedIntegrationType,
)
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatIntegrations(RocketChatBase):
    # pylint: disable=too-many-arguments
    def integrations_create(
        self,
        integrations_type,
        name,
        enabled,
        username,
        channel,
        script_enabled,
        event=None,
        urls=None,
        **kwargs
    ):
        """Creates an integration."""
        if integrations_type == "webhook-outgoing":
            return self.call_api_post(
                "integrations.create",
                type=integrations_type,
                name=name,
                enabled=enabled,
                event=event,
                urls=urls,
                username=username,
                channel=channel,
                scriptEnabled=script_enabled,
                kwargs=kwargs,
            )
        elif integrations_type == "webhook-incoming":
            return self.call_api_post(
                "integrations.create",
                type=integrations_type,
                name=name,
                enabled=enabled,
                username=username,
                channel=channel,
                scriptEnabled=script_enabled,
                kwargs=kwargs,
            )
        else:
            raise RocketUnsuportedIntegrationType()

    def integrations_get(self, integration_id, **kwargs):
        """Retrieves an integration by id."""
        return self.call_api_get(
            "integrations.get", integrationId=integration_id, kwargs=kwargs
        )

    def integrations_history(self, integration_id, **kwargs):
        """Lists all history of the specified integration."""
        return self.call_api_get(
            "integrations.history", id=integration_id, kwargs=kwargs
        )

    def integrations_list(self, **kwargs):
        """Lists all of the integrations on the server."""
        return self.call_api_get("integrations.list", kwargs=kwargs)

    def integrations_remove(self, integrations_type, integration_id, **kwargs):
        """Removes an integration from the server."""
        return self.call_api_post(
            "integrations.remove",
            type=integrations_type,
            integrationId=integration_id,
            kwargs=kwargs,
        )

    def integrations_update(
        self,
        integrations_type,
        name,
        enabled,
        username,
        channel,
        script_enabled,
        integration_id,
        **kwargs
    ):
        """Updates an existing integration."""
        return self.call_api_put(
            "integrations.update",
            type=integrations_type,
            name=name,
            enabled=enabled,
            username=username,
            channel=channel,
            scriptEnabled=script_enabled,
            integrationId=integration_id,
            kwargs=kwargs,
        )
