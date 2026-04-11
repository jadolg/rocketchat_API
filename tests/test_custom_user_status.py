import uuid

import pytest


@pytest.fixture
def status_name():
    return "test_status_" + str(uuid.uuid1()).replace("-", "")[:12]


@pytest.fixture
def created_status(logged_rocket, status_name):
    result = logged_rocket.custom_user_status_create(
        name=status_name, status_type="online"
    )
    status = result.get("customUserStatus")
    assert status is not None

    yield status

    logged_rocket.custom_user_status_delete(custom_user_status_id=status["_id"])


def test_custom_user_status_list(logged_rocket, created_status):
    result = logged_rocket.custom_user_status_list()
    assert "statuses" in result
    found = any(s["_id"] == created_status["_id"] for s in result["statuses"])
    assert found


def test_custom_user_status_create_delete(logged_rocket):
    name = "test_status_" + str(uuid.uuid1()).replace("-", "")[:12]
    result = logged_rocket.custom_user_status_create(name=name, status_type="busy")
    status = result.get("customUserStatus")
    assert status is not None
    assert status["name"] == name
    assert status["statusType"] == "busy"

    logged_rocket.custom_user_status_delete(custom_user_status_id=status["_id"])

    statuses = logged_rocket.custom_user_status_list().get("statuses", [])
    assert not any(s["_id"] == status["_id"] for s in statuses)


def test_custom_user_status_update(logged_rocket, created_status):
    new_name = created_status["name"] + "_upd"
    result = logged_rocket.custom_user_status_update(
        custom_user_status_id=created_status["_id"],
        name=new_name,
        status_type="away",
    )
    updated = result.get("customUserStatus")
    assert updated is not None
    assert updated["name"] == new_name
    assert updated["statusType"] == "away"


def test_custom_user_status_create_all_types(logged_rocket):
    created_ids = []
    for status_type in ("online", "busy", "away", "offline"):
        name = "test_" + status_type + "_" + str(uuid.uuid1()).replace("-", "")[:8]
        result = logged_rocket.custom_user_status_create(
            name=name, status_type=status_type
        )
        status = result.get("customUserStatus")
        assert status is not None
        assert status["statusType"] == status_type
        created_ids.append(status["_id"])

    for sid in created_ids:
        logged_rocket.custom_user_status_delete(custom_user_status_id=sid)
