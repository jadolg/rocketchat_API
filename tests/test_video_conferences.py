import pytest


# TODO: Go back to this test once the ticket has being answered
@pytest.mark.skip(
    reason="Broken in 5.0. https://github.com/RocketChat/Rocket.Chat/issues/26520"
)
def test_update_jitsi_timeout(logged_rocket):
    update_jitsi_timeout = logged_rocket.update_jitsi_timeout(room_id="GENERAL").json()
    assert update_jitsi_timeout.get("success")
