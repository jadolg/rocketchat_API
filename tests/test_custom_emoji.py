import uuid

import pytest


@pytest.fixture
def emoji_name():
    return "test_emoji_" + str(uuid.uuid1()).replace("-", "")[:12]


@pytest.fixture
def created_emoji(logged_rocket, emoji_name):
    logged_rocket.custom_emoji_create(
        name=emoji_name,
        emoji_file="tests/assets/avatar.png",
        aliases=emoji_name + "_alias",
    )

    emojis = logged_rocket.custom_emoji_list()
    emoji = next(
        (e for e in emojis["emojis"]["update"] if e["name"] == emoji_name), None
    )
    assert emoji is not None

    yield {"_id": emoji["_id"], "name": emoji_name}

    logged_rocket.custom_emoji_delete(emoji_id=emoji["_id"])


def test_custom_emoji_create_delete(logged_rocket):
    name = "test_emoji_" + str(uuid.uuid1()).replace("-", "")[:12]
    logged_rocket.custom_emoji_create(
        name=name,
        emoji_file="tests/assets/avatar.png",
        aliases=name + "_alias",
    )

    emojis = logged_rocket.custom_emoji_list()
    emoji = next((e for e in emojis["emojis"]["update"] if e["name"] == name), None)
    assert emoji is not None
    assert emoji["name"] == name

    logged_rocket.custom_emoji_delete(emoji_id=emoji["_id"])


def test_custom_emoji_list(logged_rocket, created_emoji):
    result = logged_rocket.custom_emoji_list()
    assert "emojis" in result
    assert "update" in result["emojis"]
    assert "remove" in result["emojis"]
    found = any(e["_id"] == created_emoji["_id"] for e in result["emojis"]["update"])
    assert found


def test_custom_emoji_list_updated_since(logged_rocket, created_emoji):
    result = logged_rocket.custom_emoji_list(updatedSince="2017-11-25T15:08:17.248Z")
    assert "emojis" in result


def test_custom_emoji_all(logged_rocket, created_emoji):
    emojis = list(logged_rocket.custom_emoji_all())
    assert len(emojis) > 0
    found = any(e["_id"] == created_emoji["_id"] for e in emojis)
    assert found


def test_custom_emoji_update(logged_rocket, created_emoji):
    new_name = created_emoji["name"] + "_upd"
    logged_rocket.custom_emoji_update(
        emoji_id=created_emoji["_id"],
        name=new_name,
        aliases=new_name + "_alias",
    )

    emojis = logged_rocket.custom_emoji_list()
    emoji = next(
        (e for e in emojis["emojis"]["update"] if e["_id"] == created_emoji["_id"]),
        None,
    )
    assert emoji is not None
    assert emoji["name"] == new_name


def test_custom_emoji_update_with_file(logged_rocket, created_emoji):
    logged_rocket.custom_emoji_update(
        emoji_id=created_emoji["_id"],
        name=created_emoji["name"],
        emoji_file="tests/assets/logo.png",
    )
