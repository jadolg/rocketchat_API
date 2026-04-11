from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatCustomSounds(RocketChatBase):
    @paginated("sounds")
    def custom_sounds_list(self, **kwargs):
        """Retrieves all custom sounds."""
        return self.call_api_get("custom-sounds.list", kwargs=kwargs)

    def custom_sounds_get_one(self, sound_id, **kwargs):
        """Retrieves a single custom sound by its _id."""
        return self.call_api_get("custom-sounds.getOne", _id=sound_id, kwargs=kwargs)
