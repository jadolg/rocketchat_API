def test_banners(logged_rocket):
    banners = logged_rocket.banners(platform="web")
    assert "banners" in banners
