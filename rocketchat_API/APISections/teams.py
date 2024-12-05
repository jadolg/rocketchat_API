from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase

ID_OR_TEAM_NAME_REQUIRED = "team_id or team_name required"


class RocketChatTeams(RocketChatBase):
    def teams_create(self, name, team_type, **kwargs):
        """Creates a new team. Requires create-team permission."""
        return self.call_api_post(
            "teams.create", name=name, type=team_type, kwargs=kwargs
        )

    def teams_delete(self, team_id=None, team_name=None, **kwargs):
        """Delete a team."""
        if team_id:
            return self.call_api_post("teams.delete", teamId=team_id, kwargs=kwargs)
        if team_name:
            return self.call_api_post("teams.delete", teamName=team_name, kwargs=kwargs)
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_list_all(self, **kwargs):
        """
        List all the teams on the server.
        The calling user must have the 'view-all-teams' permission
        """
        return self.call_api_get("teams.listAll", kwargs=kwargs)

    def teams_info(self, team_id=None, team_name=None, **kwargs):
        """
        Gets a team's information.
        If the team is not public, the caller user must be a member of
        the team.
        """
        if team_id:
            return self.call_api_get("teams.info", teamId=team_id, kwargs=kwargs)
        if team_name:
            return self.call_api_get("teams.info", teamName=team_name, kwargs=kwargs)
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_members(
        self, team_id=None, team_name=None, name="", username="", **kwargs
    ):
        """Lists the members of a team."""
        if team_id:
            return self.call_api_get(
                "teams.members",
                teamId=team_id,
                name=name,
                username=username,
                kwargs=kwargs,
            )
        if team_name:
            return self.call_api_get(
                "teams.members",
                teamName=team_name,
                name=name,
                username=username,
                kwargs=kwargs,
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_add_members(self, team_id=None, team_name=None, members=None, **kwargs):
        """Adds members to the team."""
        if team_id:
            return self.call_api_post(
                "teams.addMembers", teamId=team_id, members=members, kwargs=kwargs
            )
        if team_name:
            return self.call_api_post(
                "teams.addMembers", teamName=team_name, members=members, kwargs=kwargs
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_remove_member(self, team_id=None, team_name=None, user_id=None, **kwargs):
        """Removes a member from a team. Requires edit-team-member permission."""
        if team_id:
            return self.call_api_post(
                "teams.removeMember", teamId=team_id, userId=user_id, kwargs=kwargs
            )
        if team_name:
            return self.call_api_post(
                "teams.removeMember", teamName=team_name, userId=user_id, kwargs=kwargs
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_update_member(self, team_id=None, team_name=None, member=None, **kwargs):
        """Updates a team member's roles. Requires edit-team-member permission."""
        if team_id:
            return self.call_api_post(
                "teams.updateMember", teamId=team_id, member=member, kwargs=kwargs
            )
        if team_name:
            return self.call_api_post(
                "teams.updateMember", teamName=team_name, member=member, kwargs=kwargs
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_list_rooms(
        self, team_id=None, team_name=None, room_type="", name="", **kwargs
    ):
        """List all rooms of the team."""
        if team_id:
            return self.call_api_get(
                "teams.listRooms",
                teamId=team_id,
                type=room_type,
                filter=name,
                kwargs=kwargs,
            )
        if team_name:
            return self.call_api_get(
                "teams.listRooms",
                teamName=team_name,
                type=room_type,
                filter=name,
                kwargs=kwargs,
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_add_rooms(self, team_id=None, team_name=None, rooms=None, **kwargs):
        """Adds rooms to the team. Requires add-team-channel permission."""
        if team_id:
            return self.call_api_post(
                "teams.addRooms",
                teamId=team_id,
                rooms=rooms,
                kwargs=kwargs,
            )
        if team_name:
            return self.call_api_post(
                "teams.addRooms",
                teamName=team_name,
                rooms=rooms,
                kwargs=kwargs,
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_remove_room(self, team_id=None, team_name=None, room_id=None, **kwargs):
        """Removes a room from a team. Requires remove-team-channel permission."""
        if team_id:
            return self.call_api_post(
                "teams.removeRoom",
                teamId=team_id,
                roomId=room_id,
                kwargs=kwargs,
            )
        if team_name:
            return self.call_api_post(
                "teams.removeRoom",
                teamName=team_name,
                roomId=room_id,
                kwargs=kwargs,
            )
        raise RocketMissingParamException(ID_OR_TEAM_NAME_REQUIRED)

    def teams_update_room(self, room_id, is_default, **kwargs):
        """Updates a room from a team. Requires edit-team-channel permission."""
        return self.call_api_post(
            "teams.updateRoom",
            roomId=room_id,
            isDefault=is_default,
            kwargs=kwargs,
        )
