def test_licenses_info(logged_rocket):
    licenses_info = logged_rocket.licenses_info()
    assert "license" in licenses_info
