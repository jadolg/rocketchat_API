from rocketchat_API.APISections.base import RocketChatBase


class RocketChatLivechat(RocketChatBase):
    def livechat_rooms(self, **kwargs):
        """Retrieves a list of livechat rooms."""
        return self.call_api_get("livechat/rooms", kwargs=kwargs)

    def livechat_inquiries_list(self, **kwargs):
        """Lists all of the open livechat inquiries."""
        return self.call_api_get("livechat/inquiries.list", kwargs=kwargs)

    def livechat_inquiries_take(self, inquiry_id, **kwargs):
        """Takes an open inquiry."""
        return self.call_api_post(
            "livechat/inquiries.take", inquiryId=inquiry_id, kwargs=kwargs
        )

    def livechat_get_users(self, user_type, **kwargs):
        """Get a list of agents or managers."""
        return self.call_api_get(f"livechat/users/{user_type}", kwargs=kwargs)

    def livechat_create_user(self, user_type, **kwargs):
        """Register a new agent or manager."""
        return self.call_api_post(f"livechat/users/{user_type}", kwargs=kwargs)

    def livechat_get_user(self, user_type, user_id, **kwargs):
        """Get info about an agent or manager."""
        return self.call_api_get(f"livechat/users/{user_type}/{user_id}", kwargs=kwargs)

    def livechat_delete_user(self, user_type, user_id):
        """GRemoves an agent or manager."""
        return self.call_api_delete(f"livechat/users/{user_type}/{user_id}")
