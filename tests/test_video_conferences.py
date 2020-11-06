def test_update_jitsi_timeout(logged_rocket):
    update_jitsi_timeout = logged_rocket.update_jitsi_timeout(room_id="GENERAL").json()
    assert update_jitsi_timeout.get("success") == False
