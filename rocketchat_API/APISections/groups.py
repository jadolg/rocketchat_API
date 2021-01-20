from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatGroups(RocketChatBase):
    def groups_list_all(self, **kwargs):
        """
        List all the private groups on the server.
        The calling user must have the 'view-room-administration' right
        """
        return self.call_api_get("groups.listAll", kwargs=kwargs)

    def groups_list(self, **kwargs):
        """List the private groups the caller is part of."""
        return self.call_api_get("groups.list", kwargs=kwargs)

    def groups_history(self, room_id, **kwargs):
        """Retrieves the messages from a private group."""
        return self.call_api_get("groups.history", roomId=room_id, kwargs=kwargs)

    def groups_add_moderator(self, room_id, user_id, **kwargs):
        """Gives the role of moderator for a user in the current groups."""
        return self.call_api_post(
            "groups.addModerator", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_remove_moderator(self, room_id, user_id, **kwargs):
        """Removes the role of moderator from a user in the current groups."""
        return self.call_api_post(
            "groups.removeModerator", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_moderators(self, room_id=None, group=None, **kwargs):
        """Lists all moderators of a group."""
        if room_id:
            return self.call_api_get("groups.moderators", roomId=room_id, kwargs=kwargs)
        if group:
            return self.call_api_get("groups.moderators", roomName=group, kwargs=kwargs)
        raise RocketMissingParamException("roomId or group required")

    def groups_add_owner(self, room_id, user_id, **kwargs):
        """Gives the role of owner for a user in the current Group."""
        return self.call_api_post(
            "groups.addOwner", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_remove_owner(self, room_id, user_id, **kwargs):
        """Removes the role of owner from a user in the current Group."""
        return self.call_api_post(
            "groups.removeOwner", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_archive(self, room_id, **kwargs):
        """Archives a private group, only if you’re part of the group."""
        return self.call_api_post("groups.archive", roomId=room_id, kwargs=kwargs)

    def groups_unarchive(self, room_id, **kwargs):
        """Unarchives a private group."""
        return self.call_api_post("groups.unarchive", roomId=room_id, kwargs=kwargs)

    def groups_close(self, room_id, **kwargs):
        """Removes the private group from the user’s list of groups, only if you’re part of the group."""
        return self.call_api_post("groups.close", roomId=room_id, kwargs=kwargs)

    def groups_create(self, name, **kwargs):
        """Creates a new private group, optionally including users, only if you’re part of the group."""
        return self.call_api_post("groups.create", name=name, kwargs=kwargs)

    def groups_get_integrations(self, room_id, **kwargs):
        """Retrieves the integrations which the group has"""
        return self.call_api_get(
            "groups.getIntegrations", roomId=room_id, kwargs=kwargs
        )

    def groups_info(self, room_id=None, room_name=None, **kwargs):
        """GRetrieves the information about the private group, only if you’re part of the group."""
        if room_id:
            return self.call_api_get("groups.info", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get("groups.info", roomName=room_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or roomName required")

    def groups_invite(self, room_id, user_id, **kwargs):
        """Adds a user to the private group."""
        return self.call_api_post(
            "groups.invite", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_kick(self, room_id, user_id, **kwargs):
        """Removes a user from the private group."""
        return self.call_api_post(
            "groups.kick", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_leave(self, room_id, **kwargs):
        """Causes the callee to be removed from the private group, if they’re part of it and are not the last owner."""
        return self.call_api_post("groups.leave", roomId=room_id, kwargs=kwargs)

    def groups_open(self, room_id, **kwargs):
        """Adds the private group back to the user’s list of private groups."""
        return self.call_api_post("groups.open", roomId=room_id, kwargs=kwargs)

    def groups_rename(self, room_id, name, **kwargs):
        """Changes the name of the private group."""
        return self.call_api_post(
            "groups.rename", roomId=room_id, name=name, kwargs=kwargs
        )

    def groups_set_description(self, room_id, description, **kwargs):
        """Sets the description for the private group."""
        return self.call_api_post(
            "groups.setDescription",
            roomId=room_id,
            description=description,
            kwargs=kwargs,
        )

    def groups_set_read_only(self, room_id, read_only, **kwargs):
        """Sets whether the group is read only or not."""
        return self.call_api_post(
            "groups.setReadOnly",
            roomId=room_id,
            readOnly=bool(read_only),
            kwargs=kwargs,
        )

    def groups_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the private group."""
        return self.call_api_post(
            "groups.setTopic", roomId=room_id, topic=topic, kwargs=kwargs
        )

    def groups_set_type(self, room_id, a_type, **kwargs):
        """Sets the type of room this group should be. The type of room this channel should be, either c or p."""
        return self.call_api_post(
            "groups.setType", roomId=room_id, type=a_type, kwargs=kwargs
        )

    def groups_set_custom_fields(
        self, custom_fields, room_id=None, room_name=None, **kwargs
    ):
        if room_id:
            return self.call_api_post(
                "groups.setCustomFields",
                roomId=room_id,
                customFields=custom_fields,
                kwargs=kwargs,
            )
        if room_name:
            return self.call_api_post(
                "groups.setCustomFields",
                roomName=room_name,
                customFields=custom_fields,
                kwargs=kwargs,
            )
        raise RocketMissingParamException("room_id or room_name required")

    def groups_delete(self, room_id=None, group=None, **kwargs):
        """Delete a private group."""
        if room_id:
            return self.call_api_post("groups.delete", roomId=room_id, kwargs=kwargs)
        if group:
            return self.call_api_post("groups.delete", roomName=group, kwargs=kwargs)
        raise RocketMissingParamException("roomId or group required")

    def groups_members(self, room_id=None, group=None, **kwargs):
        """Lists all group users."""
        if room_id:
            return self.call_api_get("groups.members", roomId=room_id, kwargs=kwargs)
        if group:
            return self.call_api_get("groups.members", roomName=group, kwargs=kwargs)
        raise RocketMissingParamException("roomId or group required")

    def groups_roles(self, room_id=None, room_name=None, **kwargs):
        """Lists all user’s roles in the private group."""
        if room_id:
            return self.call_api_get("groups.roles", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get("groups.roles", roomName=room_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or room_name required")

    def groups_files(self, room_id=None, room_name=None, **kwargs):
        """Retrieves the files from a private group."""
        if room_id:
            return self.call_api_get("groups.files", roomId=room_id, kwargs=kwargs)
        if room_name:
            return self.call_api_get("groups.files", roomName=room_name, kwargs=kwargs)
        raise RocketMissingParamException("roomId or room_name required")

    def groups_add_leader(self, room_id, user_id, **kwargs):
        """Gives the role of Leader for a user in the current group."""
        return self.call_api_post(
            "groups.addLeader", roomId=room_id, userId=user_id, kwargs=kwargs
        )

    def groups_remove_leader(self, room_id, user_id, **kwargs):
        """Removes the role of Leader for a user in the current group."""
        return self.call_api_post(
            "groups.removeLeader", roomId=room_id, userId=user_id, kwargs=kwargs
        )
