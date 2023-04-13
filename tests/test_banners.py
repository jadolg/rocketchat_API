def test_banners(logged_rocket):
    banners = logged_rocket.banners(platform="web").json()
    assert banners.get("success")
    assert "banners" in banners
