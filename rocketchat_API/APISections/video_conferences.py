from rocketchat_API.APISections.base import RocketChatBase


class RocketChatVideConferences(RocketChatBase):
    def update_jitsi_timeout(self, room_id, **kwargs):
        """Updates the timeout of Jitsi video conference in a channel."""
        return self.call_api_post(
            "video-conference/jitsi.update-timeout", roomId=room_id, kwargs=kwargs
        )
