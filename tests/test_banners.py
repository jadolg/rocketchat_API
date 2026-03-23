from datetime import datetime, timezone

import pytest
from pymongo import MongoClient


@pytest.fixture
def test_banner():
    """There's no add_banner method in the public API so we need to add the test data manually to mongodb"""
    client = MongoClient("mongodb://127.0.0.1:27017/rocketchat?directConnection=true")
    db = client["rocketchat"]
    banner = {
        "_id": "test-banner-api",
        "platform": ["web"],
        "roles": ["user"],
        "startAt": datetime(2020, 1, 1, tzinfo=timezone.utc),
        "expireAt": datetime(2030, 1, 1, tzinfo=timezone.utc),
        "createdBy": "system",
        "createdAt": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "active": True,
        "surface": "banner",
        "view": {
            "appId": "banner-core",
            "viewId": "test-banner-api",
            "type": "banner",
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "Test"}}],
        },
    }
    db["rocketchat_banner"].insert_one(banner)
    yield banner
    db["rocketchat_banner"].delete_one({"_id": "test-banner-api"})
    db["rocketchat_banner_dismiss"].delete_many({"bannerId": "test-banner-api"})
    client.close()


def test_banners(logged_rocket, test_banner):
    result = logged_rocket.banners(platform="web")
    assert "banners" in result
    try:
        banner = next(b for b in result["banners"] if b["_id"] == "test-banner-api")
    except StopIteration:
        pytest.fail("Test banner not found in banners list")
    assert banner["platform"] == test_banner["platform"]
    assert banner["surface"] == test_banner["surface"]


def test_banners_get_by_id(logged_rocket, test_banner):
    result = logged_rocket.banners_get_by_id("test-banner-api", platform="web")
    assert "banners" in result
    banner = result["banners"][0]
    assert banner["_id"] == "test-banner-api"
    assert banner["platform"] == test_banner["platform"]
    assert banner["roles"] == test_banner["roles"]
    assert banner["surface"] == test_banner["surface"]
    assert banner["view"]["appId"] == test_banner["view"]["appId"]
    assert banner["view"]["blocks"] == test_banner["view"]["blocks"]


def test_banners_dismiss(logged_rocket, test_banner):
    logged_rocket.banners_dismiss("test-banner-api")
    remaining = logged_rocket.banners(platform="web").get("banners", [])
    assert not any(b["_id"] == "test-banner-api" for b in remaining)
