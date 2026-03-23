import pytest


def test_banners(logged_rocket):
    banners = logged_rocket.banners(platform="web")
    assert "banners" in banners


def test_banners_get_by_id(logged_rocket):
    banner_list = logged_rocket.banners(platform="web").get("banners", [])
    if not banner_list:
        pytest.skip("No banners available in test environment")
    banner_id = banner_list[0].get("_id")
    banner = logged_rocket.banners_get_by_id(banner_id, platform="web")
    assert banner.get("banner").get("_id") == banner_id


def test_banners_dismiss(logged_rocket):
    banner_list = logged_rocket.banners(platform="web").get("banners", [])
    if not banner_list:
        pytest.skip("No banners available in test environment")
    banner_id = banner_list[0].get("_id")
    logged_rocket.banners_dismiss(banner_id)
    remaining = logged_rocket.banners(platform="web").get("banners", [])
    assert not any(b.get("_id") == banner_id for b in remaining)
