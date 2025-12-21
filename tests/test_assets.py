def test_assets_set_asset(logged_rocket):
    logged_rocket.assets_set_asset(asset_name="logo", file="tests/assets/logo.png")


def test_assets_unset_asset(logged_rocket):
    logged_rocket.assets_unset_asset(asset_name="logo")
