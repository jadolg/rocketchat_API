import mimetypes

from packaging import version

from rocketchat_API.APISections.base import RocketChatBase


class RocketChatAssets(RocketChatBase):
    def assets_set_asset(self, asset_name, file, **kwargs):
        """Set an asset image by name."""
        server_info = self.info().json()
        content_type = mimetypes.MimeTypes().guess_type(file)

        file_name = asset_name
        if version.parse(server_info.get("info").get("version")) >= version.parse(
            "5.1"
        ):
            file_name = "asset"

        files = {
            file_name: (file, open(file, "rb"), content_type[0], {"Expires": "0"}),
        }

        return self.call_api_post(
            "assets.setAsset",
            kwargs=kwargs,
            assetName=asset_name,
            use_json=False,
            files=files,
        )

    def assets_unset_asset(self, asset_name):
        """Unset an asset by name"""
        return self.call_api_post("assets.unsetAsset", assetName=asset_name)
