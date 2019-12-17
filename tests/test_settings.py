def test_settings(logged_rocket):
    settings = logged_rocket.settings().json()
    assert settings.get('success')
    settings_get = logged_rocket.settings_get(
        _id='API_Allow_Infinite_Count').json()
    assert settings_get.get('success')
    assert settings_get.get('value')
    settings_update = logged_rocket.settings_update(
        _id='API_Allow_Infinite_Count', value=True).json()
    assert settings_update.get('success')
