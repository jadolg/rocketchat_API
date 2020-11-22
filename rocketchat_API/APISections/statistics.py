from rocketchat_API.APISections.base import RocketChatBase


class RocketChatStatistics(RocketChatBase):
    def statistics(self, **kwargs):
        """Retrieves the current statistics"""
        return self.call_api_get("statistics", kwargs=kwargs)

    def statistics_list(self, **kwargs):
        """Selectable statistics about the Rocket.Chat server."""
        return self.call_api_get("statistics.list", kwargs=kwargs)
