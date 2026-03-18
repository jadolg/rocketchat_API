from datetime import datetime, timedelta, timezone

import pytest


@pytest.fixture()
def date_range():
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    return {
        "start": start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    }



def test_engagement_dashboard_new_users(logged_rocket, skip_if_no_license, date_range):
    result = logged_rocket.engagement_dashboard_new_users(
        start=date_range["start"], end=date_range["end"]
    )
    assert "days" in result
    assert "period" in result
    assert "yesterday" in result
    assert isinstance(result["days"], list)
    assert isinstance(result["period"]["count"], int)


def test_engagement_dashboard_active_users(
    logged_rocket, skip_if_no_license, date_range
):
    result = logged_rocket.engagement_dashboard_active_users(
        start=date_range["start"], end=date_range["end"]
    )
    assert "month" in result


def test_engagement_dashboard_chat_busier_hourly(
    logged_rocket, skip_if_no_license, date_range
):
    result = logged_rocket.engagement_dashboard_chat_busier_hourly(
        start=date_range["start"]
    )
    assert "hours" in result


def test_engagement_dashboard_chat_busier_weekly(
    logged_rocket, skip_if_no_license, date_range
):
    result = logged_rocket.engagement_dashboard_chat_busier_weekly(
        start=date_range["start"]
    )
    assert "month" in result


def test_engagement_dashboard_users_by_time_of_day(
    logged_rocket, skip_if_no_license, date_range
):
    result = logged_rocket.engagement_dashboard_users_by_time_of_day(
        start=date_range["start"], end=date_range["end"]
    )
    assert "week" in result
    assert isinstance(result["week"], list)
