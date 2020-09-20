def test_assets_set_asset(logged_rocket):
    assets_set_asset = logged_rocket.assets_set_asset(
        asset_name="logo", file="tests/assets/logo.png"
    ).json()
    assert assets_set_asset.get("success")


def test_assets_unset_asset(logged_rocket):
    assets_unset_asset = logged_rocket.assets_unset_asset(asset_name="logo").json()
    assert assets_unset_asset.get("success")
