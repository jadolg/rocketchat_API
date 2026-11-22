import json

from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatMiscellaneous(RocketChatBase):
    # Miscellaneous information
    @paginated("result")
    def directory(self, query, **kwargs):
        """Search by users or channels on all server."""
        if isinstance(query, str):
            query = json.loads(query)

        return self.call_api_get("directory", kwargs={**query, **kwargs})

    def spotlight(self, query, **kwargs):
        """Searches for users or rooms that are visible to the user."""
        return self.call_api_get("spotlight", query=query, kwargs=kwargs)
