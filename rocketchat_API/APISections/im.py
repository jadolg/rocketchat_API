from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatIM(RocketChatBase):
    def im_list(self, **kwargs):
        """List the private im chats for logged user"""
        return self.call_api_get("im.list", kwargs=kwargs)

    def im_list_everyone(self, **kwargs):
        """List all direct message the caller in the server."""
        return self.call_api_get("im.list.everyone", kwargs=kwargs)

    def im_history(self, room_id, **kwargs):
        """Retrieves the history for a private im chat"""
        return self.call_api_get("im.history", roomId=room_id, kwargs=kwargs)

    def im_create(self, username, **kwargs):
        """Create a direct message session with another user."""
        return self.call_api_post("im.create", username=username, kwargs=kwargs)

    def im_open(self, room_id, **kwargs):
        """Adds the direct message back to the user’s list of direct messages."""
        return self.call_api_post("im.open", roomId=room_id, kwargs=kwargs)

    def im_close(self, room_id, **kwargs):
        """Removes the direct message from the user’s list of direct messages."""
        return self.call_api_post("im.close", roomId=room_id, kwargs=kwargs)

    def im_members(self, room_id, **kwargs):
        """Retrieves members of a direct message."""
        return self.call_api_get("im.members", roomId=room_id, args=kwargs)

    def im_messages(self, room_id=None, username=None, **kwargs):
        """Retrieves direct messages from the server by username"""
        if room_id:
            return self.call_api_get("im.messages", roomId=room_id, args=kwargs)

        if username:
            return self.call_api_get("im.messages", username=username, args=kwargs)

        raise RocketMissingParamException("roomId or username required")

    def im_messages_others(self, room_id, **kwargs):
        """Retrieves the messages from any direct message in the server"""
        return self.call_api_get("im.messages.others", roomId=room_id, kwargs=kwargs)

    def im_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the direct message"""
        return self.call_api_post(
            "im.setTopic", roomId=room_id, topic=topic, kwargs=kwargs
        )

    def im_files(self, room_id=None, user_name=None, **kwargs):
        """Retrieves the files from a direct message."""
        if room_id:
            return self.call_api_get("im.files", roomId=room_id, kwargs=kwargs)
        if user_name:
            return self.call_api_get("im.files", username=user_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or username required")

    def im_counters(self, room_id=None, user_name=None, **kwargs):
        """Gets counters of direct messages."""
        if room_id:
            return self.call_api_get("im.counters", roomId=room_id, kwargs=kwargs)
        if user_name:
            return self.call_api_get("im.counters", username=user_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or username required")
