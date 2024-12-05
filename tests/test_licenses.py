def test_licenses_get(logged_rocket, skip_v7):
    licenses_get = logged_rocket.licenses_get().json()
    assert licenses_get.get("success")


def test_licenses_info(logged_rocket):
    licenses_info = logged_rocket.licenses_info().json()
    assert licenses_info.get("success")
