def test_settings(logged_rocket):
    settings = logged_rocket.settings()
    assert all(key in settings for key in ["settings", "count", "offset", "total"])
    settings_get = logged_rocket.settings_get(_id="API_Allow_Infinite_Count")
    assert settings_get.get("value")
    logged_rocket.settings_update(_id="API_Allow_Infinite_Count", value=True)


def test_settings_public(rocket):
    settings_public = rocket.settings_public()
    assert "settings" in settings_public


def test_service_configurations(rocket):
    service_configurations = rocket.service_configurations()
    assert "configurations" in service_configurations
