from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatChannels(RocketChatBase):
    def channels_list(self, **kwargs):
        """Retrieves all of the channels from the server."""
        return self.call_api_get("channels.list", kwargs=kwargs)

    def channels_list_joined(self, **kwargs):
        """Lists all of the channels the calling user has joined"""
        return self.call_api_get("channels.list.joined", kwargs=kwargs)

    def channels_info(self, room_id=None, channel=None, **kwargs):
        """Gets a channel’s information."""
        if room_id:
            return self.call_api_get("channels.info", roomId=room_id, kwargs=kwargs)
        if channel:
            return self.call_api_get("channels.info", roomName=channel, kwargs=kwargs)
        raise RocketMissingParamException("roomId or channel required")

    def channels_history(self, room_id, **kwargs):
        """Retrieves the messages from a channel."""
        return self.call_api_get("channels.history", roomId=room_id, kwargs=kwargs)

    def channels_add_all(self, room_id, **kwargs):
        """Adds all of the users of the Rocket.Chat server to the channel."""
        return self.call_api_post("channels.addAll", roomId=room_id, kwargs=kwargs)

    def channels_add_moderator(self, room_id, user_id, **kwargs):
        """Gives the role of moderator for a user in the current channel."""
        return self.call_api_post(
            "channels.addModerator", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def channels_remove_moderator(self, room_id, user_id, **kwargs):
        """Removes the role of moderator from a user in the current channel."""
        return self.call_api_post(
            "channels.removeModerator", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def channels_moderators(self, room_id=None, channel=None, **kwargs):
        """Lists all moderators of a channel."""
        if room_id:
            return self.call_api_get(
                "channels.moderators", roomId=room_id, kwargs=kwargs
            )
        if channel:
            return self.call_api_get(
                "channels.moderators", roomName=channel, kwargs=kwargs
            )
        raise RocketMissingParamException("roomId or channel required")

    def channels_add_owner(self, room_id, user_id=None, username=None, **kwargs):
        """Gives the role of owner for a user in the current channel."""
        if user_id:
            return self.call_api_post(
                "channels.addOwner", roomId=room_id, userId=user_id, kwargs=kwargs
            )
        if username:
            return self.call_api_post(
                "channels.addOwner", roomId=room_id, username=username, kwargs=kwargs
            )
        raise RocketMissingParamException("userID or username required")

    def channels_remove_owner(self, room_id, user_id, **kwargs):
        """Removes the role of owner from a user in the current channel."""
        return self.call_api_post(
            "channels.removeOwner", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def channels_archive(self, room_id, **kwargs):
        """Archives a channel."""
        return self.call_api_post("channels.archive", roomId=room_id, kwargs=kwargs)

    def channels_unarchive(self, room_id, **kwargs):
        """Unarchives a channel."""
        return self.call_api_post("channels.unarchive", roomId=room_id, kwargs=kwargs)

    def channels_close(self, room_id, **kwargs):
        """Removes the channel from the user’s list of channels."""
        return self.call_api_post("channels.close", roomId=room_id, kwargs=kwargs)

    def channels_open(self, room_id, **kwargs):
        """Adds the channel back to the user’s list of channels."""
        return self.call_api_post("channels.open", roomId=room_id, kwargs=kwargs)

    def channels_create(self, name, **kwargs):
        """Creates a new public channel, optionally including users."""
        return self.call_api_post("channels.create", name=name, kwargs=kwargs)

    def channels_get_integrations(self, room_id, **kwargs):
        """Retrieves the integrations which the channel has"""
        return self.call_api_get(
            "channels.getIntegrations", roomId=room_id, kwargs=kwargs
        )

    def channels_invite(self, room_id, user_id, **kwargs):
        """Adds a user to the channel."""
        return self.call_api_post(
            "channels.invite", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def channels_join(self, room_id, join_code, **kwargs):
        """Joins yourself to the channel."""
        return self.call_api_post(
            "channels.join", roomId=room_id, joinCode=join_code, kwargs=kwargs
        )

    def channels_kick(self, room_id, user_id, **kwargs):
        """Removes a user from the channel."""
        return self.call_api_post(
            "channels.kick", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def channels_leave(self, room_id, **kwargs):
        """Causes the callee to be removed from the channel."""
        return self.call_api_post("channels.leave", roomId=room_id, kwargs=kwargs)

    def channels_rename(self, room_id, name, **kwargs):
        """Changes the name of the channel."""
        return self.call_api_post(
            "channels.rename", roomId=room_id, name=name, kwargs=kwargs
        )

    def channels_set_description(self, room_id, description, **kwargs):
        """Sets the description for the channel."""
        return self.call_api_post(
            "channels.setDescription",
            roomId=room_id,
            description=description,
            kwargs=kwargs,
        )

    def channels_set_join_code(self, room_id, join_code, **kwargs):
        """Sets the code required to join the channel."""
        return self.call_api_post(
            "channels.setJoinCode", roomId=room_id, joinCode=join_code, kwargs=kwargs
        )

    def channels_set_read_only(self, room_id, read_only, **kwargs):
        """Sets whether the channel is read only or not."""
        return self.call_api_post(
            "channels.setReadOnly",
            roomId=room_id,
            readOnly=bool(read_only),
            kwargs=kwargs,
        )

    def channels_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the channel."""
        return self.call_api_post(
            "channels.setTopic", roomId=room_id, topic=topic, kwargs=kwargs
        )

    def channels_set_type(self, room_id, a_type, **kwargs):
        """Sets the type of room this channel should be. The type of room this channel should be, either c or p."""
        return self.call_api_post(
            "channels.setType", roomId=room_id, type=a_type, kwargs=kwargs
        )

    def channels_set_announcement(self, room_id, announce, **kwargs):
        """Sets the announcement for the channel."""
        return self.call_api_post(
            "channels.setAnnouncement",
            roomId=room_id,
            announcement=announce,
            kwargs=kwargs,
        )

    def channels_set_custom_fields(self, rid, custom_fields):
        """Sets the custom fields for the channel."""
        return self.call_api_post(
            "channels.setCustomFields", roomId=rid, customFields=custom_fields
        )

    def channels_delete(self, room_id=None, channel=None, **kwargs):
        """Delete a public channel."""
        if room_id:
            return self.call_api_post("channels.delete", roomId=room_id, kwargs=kwargs)
        if channel:
            return self.call_api_post(
                "channels.delete", roomName=channel, kwargs=kwargs
            )
        raise RocketMissingParamException("roomId or channel required")

    def channels_members(self, room_id=None, channel=None, **kwargs):
        """Lists all channel users."""
        if room_id:
            return self.call_api_get("channels.members", roomId=room_id, kwargs=kwargs)
        if channel:
            return self.call_api_get(
                "channels.members", roomName=channel, kwargs=kwargs
            )
        raise RocketMissingParamException("roomId or channel required")

    def channels_roles(self, room_id=None, room_name=None, **kwargs):
        """Lists all user’s roles in the channel."""
        if room_id:
            return self.call_api_get("channels.roles", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get(
                "channels.roles", roomName=room_name, kwargs=kwargs
            )
        raise RocketMissingParamException("roomId or room_name required")

    def channels_files(self, room_id=None, room_name=None, **kwargs):
        """Retrieves the files from a channel."""
        if room_id:
            return self.call_api_get("channels.files", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get(
                "channels.files", roomName=room_name, kwargs=kwargs
            )
        raise RocketMissingParamException("room_id or room_name required")

    def channels_get_all_user_mentions_by_channel(self, room_id, **kwargs):
        """Gets all the mentions of a channel."""
        return self.call_api_get(
            "channels.getAllUserMentionsByChannel", roomId=room_id, kwargs=kwargs
        )

    def channels_counters(self, room_id=None, room_name=None, **kwargs):
        """Gets counters for a channel."""
        if room_id:
            return self.call_api_get("channels.counters", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get(
                "channels.counters", roomName=room_name, kwargs=kwargs
            )
        raise RocketMissingParamException("room_id or room_name required")

    def channels_online(self, _id):
        """Lists all online users of a channel if the channel's id is provided, otherwise it gets all online users of
        all channels."""
        return self.call_api_get("channels.online", _id=_id)
