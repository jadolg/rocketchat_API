import mimetypes

from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatCustomEmoji(RocketChatBase):
    @paginated("emojis")
    def custom_emoji_all(self, **kwargs):
        """List all custom emojis."""
        return self.call_api_get("emoji-custom.all", kwargs=kwargs)

    def custom_emoji_list(self, **kwargs):
        """Get a list of updated and removed emojis."""
        return self.call_api_get("emoji-custom.list", kwargs=kwargs)

    def custom_emoji_create(self, name, emoji_file, aliases=None, **kwargs):
        """
        Upload a custom emoji to the workspace. Make sure that you have configured the storage system. For details, refer to the Manage Custom Sounds and Emojis document.
        Permission required: manage-emoji
        """
        content_type = mimetypes.MimeTypes().guess_type(emoji_file)
        files = {
            "emoji": (
                emoji_file,
                open(emoji_file, "rb"),
                content_type[0],
            ),
        }
        return self.call_api_post(
            "emoji-custom.create",
            name=name,
            aliases=aliases,
            files=files,
            use_json=False,
            kwargs=kwargs,
        )

    def custom_emoji_delete(self, emoji_id, **kwargs):
        """Delete a custom emoji. Permission required: manage-emoji"""
        return self.call_api_post(
            "emoji-custom.delete", emojiId=emoji_id, kwargs=kwargs
        )

    def custom_emoji_update(
        self, emoji_id, name, emoji_file=None, aliases=None, **kwargs
    ):
        """Update a custom emoji. Permission required: manage-emoji"""
        files = None
        if emoji_file:
            content_type = mimetypes.MimeTypes().guess_type(emoji_file)
            files = {
                "emoji": (
                    emoji_file,
                    open(emoji_file, "rb"),
                    content_type[0],
                ),
            }
        return self.call_api_post(
            "emoji-custom.update",
            _id=emoji_id,
            name=name,
            aliases=aliases,
            files=files,
            use_json=False,
            kwargs=kwargs,
        )
