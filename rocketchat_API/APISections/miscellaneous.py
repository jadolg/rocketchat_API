from rocketchat_API.APISections.base import RocketChatBase


class RocketChatMiscellaneous(RocketChatBase):
    # Miscellaneous information
    def info(self, **kwargs):
        """Information about the Rocket.Chat server."""
        return self.call_api_get("info", kwargs=kwargs)

    def directory(self, query, **kwargs):
        """Search by users or channels on all server."""
        if isinstance(query, dict):
            query = str(query).replace("'", '"')

        return self.call_api_get("directory", query=query, kwargs=kwargs)

    def spotlight(self, query, **kwargs):
        """Searches for users or rooms that are visible to the user."""
        return self.call_api_get("spotlight", query=query, kwargs=kwargs)
