import time

import pytest


def test_settings(logged_rocket):
    settings = logged_rocket.settings()
    assert all(key in settings for key in ["settings", "count", "offset", "total"])
    settings_get = logged_rocket.settings_get(_id="API_Allow_Infinite_Count")
    assert settings_get.get("value")
    logged_rocket.settings_update(_id="API_Allow_Infinite_Count", value=True)


def test_settings_public(rocket):
    settings_public = rocket.settings_public()
    assert "settings" in settings_public


@pytest.mark.skip(
    reason="Broken in 5.0 https://github.com/jadolg/rocketchat_API/issues/168"
)
def test_settings_oauth(logged_rocket):
    # refresh is not done with any API call ever, so we need to call it manually here
    response = logged_rocket.call_api_post(
        "method.call/refreshOAuthService",
        message='{"method": "refreshOAuthService", "params": []}',
    )
    assert response.ok
    oauth_get = logged_rocket.settings_oauth()
    if oauth_get.get("services"):
        # remove the OAuth app Test beforehand, when this is not the first test run (for reproducibility)
        response = logged_rocket.call_api_post(
            "method.call/removeOAuthService",
            message='{"method": "removeOAuthService", "params": ["Test"]}',
        )
        assert response.ok
        oauth_get = logged_rocket.settings_oauth()
        assert not oauth_get.get("services")

    logged_rocket.settings_addcustomoauth("Test")
    logged_rocket.settings_update("Accounts_OAuth_Custom-Test", True)
    time.sleep(3)
    oauth_get = logged_rocket.settings_oauth()
    assert oauth_get.get("services")[0].get("service") == "test"


def test_service_configurations(rocket):
    service_configurations = rocket.service_configurations()
    assert "configurations" in service_configurations
