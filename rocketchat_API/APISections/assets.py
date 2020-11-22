import mimetypes

from rocketchat_API.APISections.base import RocketChatBase


class RocketChatAssets(RocketChatBase):
    def assets_set_asset(self, asset_name, file, **kwargs):
        """Set an asset image by name."""
        content_type = mimetypes.MimeTypes().guess_type(file)
        files = {
            asset_name: (file, open(file, "rb"), content_type[0], {"Expires": "0"}),
        }
        return self.call_api_post(
            "assets.setAsset", kwargs=kwargs, use_json=False, files=files
        )

    def assets_unset_asset(self, asset_name):
        """Unset an asset by name"""
        return self.call_api_post("assets.unsetAsset", assetName=asset_name)
