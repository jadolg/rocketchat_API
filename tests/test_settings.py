import time

import pytest


def test_settings(logged_rocket):
    settings = logged_rocket.settings().json()
    assert settings.get("success")
    settings_get = logged_rocket.settings_get(_id="API_Allow_Infinite_Count").json()
    assert settings_get.get("success")
    assert settings_get.get("value")
    settings_update = logged_rocket.settings_update(
        _id="API_Allow_Infinite_Count", value=True
    ).json()
    assert settings_update.get("success")


def test_settings_public(rocket):
    settings_public = rocket.settings_public().json()
    assert settings_public.get("success")
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
    oauth_get = logged_rocket.settings_oauth().json()
    assert oauth_get.get("success")
    if oauth_get.get("services"):
        # remove the OAuth app Test beforehand, when this is not the first test run (for reproducibility)
        response = logged_rocket.call_api_post(
            "method.call/removeOAuthService",
            message='{"method": "removeOAuthService", "params": ["Test"]}',
        )
        assert response.ok
        oauth_get = logged_rocket.settings_oauth().json()
        assert not oauth_get.get("services")

    oauth_set = logged_rocket.settings_addcustomoauth("Test").json()
    assert oauth_set.get("success")
    oauth_set = logged_rocket.settings_update("Accounts_OAuth_Custom-Test", True).json()
    time.sleep(3)
    assert oauth_set.get("success")
    oauth_get = logged_rocket.settings_oauth().json()
    assert oauth_get.get("success")
    assert oauth_get.get("services")[0].get("service") == "test"


def test_service_configurations(rocket):
    service_configurations = rocket.service_configurations().json()
    assert service_configurations.get("success")
    assert "configurations" in service_configurations
