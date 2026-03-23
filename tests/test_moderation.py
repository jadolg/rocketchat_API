import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketApiException,
    RocketBadStatusCodeException,
)


@pytest.fixture
def reported_message(logged_rocket):
    """Post a message in GENERAL, report it, yield ids, then clean up."""
    msg = logged_rocket.chat_post_message("message to report", channel="GENERAL").get(
        "message"
    )
    msg_id = msg["_id"]
    user_id = msg["u"]["_id"]
    logged_rocket.chat_report_message(
        message_id=msg_id, description="test moderation report"
    )
    reports = list(logged_rocket.moderation_reports(msg_id=msg_id))
    report_id = reports[0]["_id"] if reports else None
    yield {"msg_id": msg_id, "user_id": user_id, "report_id": report_id}
    try:
        logged_rocket.moderation_dismiss_reports(msg_id=msg_id, reason="cleanup")
    except (RocketApiException, RocketBadStatusCodeException):
        pass
    try:
        logged_rocket.chat_delete(room_id="GENERAL", msg_id=msg_id)
    except (RocketApiException, RocketBadStatusCodeException):
        pass


@pytest.fixture
def reported_user(logged_rocket):
    """Report the logged-in user (self-report), yield user_id, then clean up."""
    user_id = logged_rocket.me().get("_id")
    logged_rocket.moderation_report_user(
        user_id=user_id, description="test user report"
    )
    yield user_id
    logged_rocket.moderation_dismiss_user_reports(user_id=user_id, reason="cleanup")


def test_moderation_reports(logged_rocket, reported_message):
    reports = list(logged_rocket.moderation_reports(msg_id=reported_message["msg_id"]))
    assert len(reports) > 0
    report = reports[0]
    assert report["_id"] == reported_message["report_id"]
    assert "description" in report
    assert "reportedBy" in report
    assert "room" in report


def test_moderation_report_info(logged_rocket, reported_message):
    result = logged_rocket.moderation_report_info(
        report_id=reported_message["report_id"]
    )
    assert result["report"]["_id"] == reported_message["report_id"]
    assert result["report"]["room"]["_id"] == "GENERAL"


def test_moderation_reports_by_users(logged_rocket, reported_message):
    reports = list(logged_rocket.moderation_reports_by_users())
    assert len(reports) > 0
    assert any(r["userId"] == reported_message["user_id"] for r in reports)


def test_moderation_user_reported_messages(logged_rocket, reported_message):
    result = logged_rocket.moderation_user_reported_messages(
        user_id=reported_message["user_id"]
    )
    assert "messages" in result
    assert len(result["messages"]) > 0
    assert result["user"]["_id"] == reported_message["user_id"]
    assert any(
        m["message"]["_id"] == reported_message["msg_id"] for m in result["messages"]
    )


def test_moderation_report_user(logged_rocket, reported_user):
    reports = list(logged_rocket.moderation_user_reports())
    assert len(reports) > 0
    assert any(r["reportedUser"]["_id"] == reported_user for r in reports)


def test_moderation_user_reports(logged_rocket, reported_user):
    reports = list(logged_rocket.moderation_user_reports())
    assert len(reports) > 0
    report = reports[0]
    assert "reportedUser" in report
    assert "ts" in report
    assert "count" in report


def test_moderation_user_reports_by_user_id(logged_rocket, reported_user):
    result = logged_rocket.moderation_user_reports_by_user_id(user_id=reported_user)
    assert result["user"]["_id"] == reported_user
    assert "reports" in result
    assert len(result["reports"]) > 0


def test_moderation_dismiss_reports_by_msg(logged_rocket, reported_message):
    logged_rocket.moderation_dismiss_reports(msg_id=reported_message["msg_id"])
    reports = list(logged_rocket.moderation_reports(msg_id=reported_message["msg_id"]))
    assert len(reports) == 0


def test_moderation_dismiss_reports_by_user(logged_rocket, reported_message):
    logged_rocket.moderation_dismiss_reports(user_id=reported_message["user_id"])
    reports = list(logged_rocket.moderation_reports_by_users())
    assert not any(r["userId"] == reported_message["user_id"] for r in reports)


def test_moderation_dismiss_user_reports(logged_rocket, reported_user):
    logged_rocket.moderation_dismiss_user_reports(user_id=reported_user)
    reports = list(logged_rocket.moderation_user_reports())
    assert not any(r["reportedUser"]["_id"] == reported_user for r in reports)


def test_moderation_user_delete_reported_messages(logged_rocket):
    msg = logged_rocket.chat_post_message(
        "message to delete via moderation", channel="GENERAL"
    ).get("message")
    msg_id = msg["_id"]
    user_id = msg["u"]["_id"]
    logged_rocket.chat_report_message(
        message_id=msg_id, description="report before delete"
    )
    logged_rocket.moderation_user_delete_reported_messages(user_id=user_id)
    deleted = list(
        logged_rocket.chat_get_deleted_messages(
            room_id="GENERAL", since="2000-01-01T00:00:00.000Z"
        )
    )
    assert any(m["_id"] == msg_id for m in deleted)
