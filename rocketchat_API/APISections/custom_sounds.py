import mimetypes

from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatCustomSounds(RocketChatBase):
    @paginated("sounds")
    def custom_sounds_list(self, **kwargs):
        """Retrieves all custom sounds."""
        return self.call_api_get("custom-sounds.list", kwargs=kwargs)

    def custom_sounds_get_one(self, sound_id, **kwargs):
        """Retrieves a single custom sound by its _id."""
        return self.call_api_get("custom-sounds.getOne", _id=sound_id, kwargs=kwargs)

    def custom_sounds_create(self, name, file, **kwargs):
        """Creates a custom sound from a local audio file."""
        content_type = mimetypes.guess_type(file)[0]
        with open(file, "rb") as f:
            return self.call_api_post(
                "custom-sounds.create",
                kwargs=kwargs,
                name=name,
                files={"sound": (file, f, content_type)},
            )

    def custom_sounds_delete(self, sound_id, **kwargs):
        """Deletes a custom sound by its _id."""
        return self.call_api_post("custom-sounds.delete", _id=sound_id, kwargs=kwargs)
