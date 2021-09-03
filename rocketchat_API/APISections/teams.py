from rocketchat_API.APISections.base import RocketChatBase


class RocketChatTeams(RocketChatBase):
    def teams_create(self, name, team_type, **kwargs):
        """Creates a new team. Requires create-team permission."""
        return self.call_api_post(
            "teams.create", name=name, type=team_type, kwargs=kwargs
        )
