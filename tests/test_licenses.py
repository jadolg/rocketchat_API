def test_licenses_get(logged_rocket):
    licenses_get = logged_rocket.licenses_get().json()
    assert licenses_get.get("success")
