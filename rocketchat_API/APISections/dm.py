from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatDM(RocketChatBase):
    @paginated("ims")
    def dm_list(self, **kwargs):
        """List the private im chats for logged user."""
        return self.call_api_get("dm.list", kwargs=kwargs)

    @paginated("ims")
    def dm_list_everyone(self, **kwargs):
        """List all direct message the caller in the server."""
        return self.call_api_get("dm.list.everyone", kwargs=kwargs)

    @paginated("messages")
    def dm_history(self, room_id, **kwargs):
        """Retrieves the history for a private im chat."""
        return self.call_api_get("dm.history", roomId=room_id, kwargs=kwargs)

    def dm_create(self, username, **kwargs):
        """Create a direct message session with another user."""
        return self.call_api_post("dm.create", username=username, kwargs=kwargs)

    def dm_create_multiple(self, usernames, **kwargs):
        """Create a direct message session with one or more users."""
        return self.call_api_post(
            "dm.create", usernames=",".join(usernames), kwargs=kwargs
        )

    def dm_open(self, room_id, **kwargs):
        """Adds the direct message back to the user's list of direct messages."""
        return self.call_api_post("dm.open", roomId=room_id, kwargs=kwargs)

    def dm_close(self, room_id, **kwargs):
        """Removes the direct message from the user's list of direct messages."""
        return self.call_api_post("dm.close", roomId=room_id, kwargs=kwargs)

    def dm_members(self, room_id):
        """Retrieves members of a direct message."""
        return self.call_api_get("dm.members", roomId=room_id)

    @paginated("messages")
    def dm_messages(self, room_id=None, username=None, **kwargs):
        """Retrieves direct messages from the server."""
        if room_id:
            return self.call_api_get("dm.messages", roomId=room_id, kwargs=kwargs)

        if username:
            return self.call_api_get("dm.messages", username=username, kwargs=kwargs)

        raise RocketMissingParamException("roomId or username required")

    def dm_messages_others(self, room_id, **kwargs):
        """Retrieves the messages from any direct message in the server"""
        return self.call_api_get("dm.messages.others", roomId=room_id, kwargs=kwargs)

    def dm_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the direct message"""
        return self.call_api_post(
            "dm.setTopic", roomId=room_id, topic=topic, kwargs=kwargs
        )

    @paginated("files")
    def dm_files(self, room_id=None, user_name=None, **kwargs):
        """Retrieves the files from a direct message."""
        if room_id:
            return self.call_api_get("dm.files", roomId=room_id, kwargs=kwargs)
        if user_name:
            return self.call_api_get("dm.files", username=user_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or username required")

    def dm_counters(self, room_id, user_name=None):
        """Gets counters of direct messages."""
        if user_name:
            return self.call_api_get("dm.counters", roomId=room_id, username=user_name)
        return self.call_api_get("dm.counters", roomId=room_id)
