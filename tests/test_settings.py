def test_settings(logged_rocket):
    settings = list(logged_rocket.settings())
    assert len(settings) > 0
    for setting in settings:
        assert "_id" in setting
    settings_get = logged_rocket.settings_get(_id="API_Allow_Infinite_Count")
    assert settings_get.get("value")
    logged_rocket.settings_update(_id="API_Allow_Infinite_Count", value=True)


def test_settings_public(rocket):
    settings_public = list(rocket.settings_public())
    assert len(settings_public) > 0
    for setting in settings_public:
        assert "_id" in setting


def test_service_configurations(rocket):
    service_configurations = rocket.service_configurations()
    assert "configurations" in service_configurations
