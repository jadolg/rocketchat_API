def test_licenses_info(logged_rocket):
    licenses_info = logged_rocket.licenses_info().json()
    assert licenses_info.get("success")
