from rocketchat_API.APISections.base import RocketChatBase


class RocketChatBanners(RocketChatBase):
    def banners(self, platform, **kwargs):
        """Gets the banner to be shown to the authenticated user"""
        return self.call_api_get(
            "banners",
            platform=platform,
            kwargs=kwargs,
        )

    def banners_get_by_id(self, banner_id, platform, **kwargs):
        """Gets a banner by its ID."""
        return self.call_api_get(
            "banners/{}".format(banner_id),
            platform=platform,
            kwargs=kwargs,
        )

    def banners_dismiss(self, banner_id, **kwargs):
        """Dismisses a banner for the authenticated user."""
        return self.call_api_post("banners.dismiss", bannerId=banner_id, kwargs=kwargs)
