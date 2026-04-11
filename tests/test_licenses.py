def test_licenses_info_works_without_license(logged_rocket):
    licenses_info = logged_rocket.licenses_info()
    assert "license" in licenses_info


def test_licenses_info(logged_rocket, skip_if_no_license, skip_if_version_under):
    skip_if_version_under("8.1.0")
    licenses_info = logged_rocket.licenses_info()
    assert "license" in licenses_info
    license_data = licenses_info["license"]
    assert "activeModules" in license_data
    assert "hasValidLicense" in license_data
    assert "tags" in license_data
    assert "limits" in license_data
    assert isinstance(license_data["activeModules"], list)
    assert isinstance(license_data["tags"], list)


def test_licenses_max_active_users(logged_rocket, skip_if_no_license):
    result = logged_rocket.licenses_max_active_users()
    assert "maxActiveUsers" in result
    assert "activeUsers" in result
