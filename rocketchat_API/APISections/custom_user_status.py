from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatCustomUserStatus(RocketChatBase):
    @paginated("statuses")
    def custom_user_status_list(self, **kwargs):
        """Lists all available custom user's status."""
        return self.call_api_get("custom-user-status.list", kwargs=kwargs)

    def custom_user_status_create(self, name, status_type, **kwargs):
        """Creates custom user status.

        :param name: The name of the custom status.
        :param status_type: The statusType of the custom status. Valid status type includes: Online, Busy, Away, Offline.
        """
        return self.call_api_post(
            "custom-user-status.create",
            name=name,
            statusType=status_type,
            kwargs=kwargs,
        )

    def custom_user_status_delete(self, custom_user_status_id, **kwargs):
        """Deletes a custom user status."""
        return self.call_api_post(
            "custom-user-status.delete",
            customUserStatusId=custom_user_status_id,
            kwargs=kwargs,
        )

    def custom_user_status_update(
        self, custom_user_status_id, name, status_type, **kwargs
    ):
        """Updates a custom user status."""
        return self.call_api_post(
            "custom-user-status.update",
            _id=custom_user_status_id,
            name=name,
            statusType=status_type,
            kwargs=kwargs,
        )
