import json
import uuid


def _sound_name():
    return "test_sound_" + str(uuid.uuid1()).replace("-", "")[:12]


def _create_sound(logged_rocket, name):
    """Create a custom sound entry via method.call and return its _id."""
    result = logged_rocket.call_api_post(
        "method.call/insertOrUpdateSound",
        message=json.dumps(
            {
                "msg": "method",
                "id": "1",
                "method": "insertOrUpdateSound",
                "params": [{"name": name, "extension": "mp3", "newFile": True}],
            }
        ),
    )
    return json.loads(result["message"])["result"]


def _delete_sound(logged_rocket, sound_id):
    """Delete a custom sound entry via method.call."""
    logged_rocket.call_api_post(
        "method.call/deleteCustomSound",
        message=json.dumps(
            {
                "msg": "method",
                "id": "1",
                "method": "deleteCustomSound",
                "params": [sound_id],
            }
        ),
    )


def test_custom_sounds_list(logged_rocket):
    result = list(logged_rocket.custom_sounds_list())
    assert isinstance(result, list)


def test_custom_sounds_list_structure(logged_rocket):
    name = _sound_name()
    sound_id = _create_sound(logged_rocket, name)
    try:
        sounds = list(logged_rocket.custom_sounds_list())
        assert any(s["_id"] == sound_id for s in sounds)
        sound = next(s for s in sounds if s["_id"] == sound_id)
        assert "name" in sound
        assert "extension" in sound
    finally:
        _delete_sound(logged_rocket, sound_id)


def test_custom_sounds_list_filter_by_name(logged_rocket):
    name = _sound_name()
    sound_id = _create_sound(logged_rocket, name)
    try:
        sounds = list(logged_rocket.custom_sounds_list(name=name))
        assert len(sounds) >= 1
        assert all(name.lower() in s["name"].lower() for s in sounds)
    finally:
        _delete_sound(logged_rocket, sound_id)


def test_custom_sounds_get_one(logged_rocket, skip_if_version_under):
    skip_if_version_under("8.3.0")
    name = _sound_name()
    sound_id = _create_sound(logged_rocket, name)
    try:
        result = logged_rocket.custom_sounds_get_one(sound_id)
        assert "sound" in result
        assert result["sound"]["_id"] == sound_id
        assert result["sound"]["name"] == name
    finally:
        _delete_sound(logged_rocket, sound_id)
