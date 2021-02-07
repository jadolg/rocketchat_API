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
