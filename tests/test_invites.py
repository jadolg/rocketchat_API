import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketApiException,
    RocketBadStatusCodeException,
)


@pytest.fixture
def invite(logged_rocket):
    """Create an invite for GENERAL, yield it, then clean up."""
    result = logged_rocket.find_or_create_invite(rid="GENERAL", days=7, max_uses=5)
    yield result
    try:
        logged_rocket.remove_invite(result["_id"])
    except (RocketApiException, RocketBadStatusCodeException):
        pass


def test_find_or_create_invite(invite):
    assert invite.get("days") == 7
    assert invite.get("maxUses") == 5
    assert invite.get("rid") == "GENERAL"


def test_list_invites(logged_rocket, invite):
    list_invites = logged_rocket.list_invites()
    assert isinstance(list_invites, list)
    assert any(i["_id"] == invite["_id"] for i in list_invites)


def test_remove_invite(logged_rocket, invite):
    logged_rocket.remove_invite(invite["_id"])
    list_invites = logged_rocket.list_invites()
    assert not any(i["_id"] == invite["_id"] for i in list_invites)


def test_validate_invite_token(logged_rocket, invite):
    result = logged_rocket.validate_invite_token(token=invite["_id"])
    assert result.get("valid") is True


def test_use_invite_token(logged_rocket, invite):
    result = logged_rocket.use_invite_token(token=invite["_id"])
    assert "room" in result
    assert result["room"]["rid"] == "GENERAL"


def test_send_invitation_email(logged_rocket):
    logged_rocket.send_invitation_email(emails=["test@example.com"])
