import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketMissingParamException,
    RocketApiException,
    RocketBadStatusCodeException,
)


@pytest.fixture
def test_team_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_team_id(test_team_name, logged_rocket):
    _test_team_id = (
        logged_rocket.teams_create(name=test_team_name, team_type=1)
        .get("team")
        .get("_id")
    )
    return _test_team_id


@pytest.fixture
def testuser_id(logged_rocket):
    testuser = logged_rocket.users_info(username="testuser1")

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    try:
        logged_rocket.users_delete(_testuser_id)
    except (RocketApiException, RocketBadStatusCodeException):
        pass


@pytest.fixture
def test_group_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_group_id(test_group_name, logged_rocket):
    _test_group_id = (
        logged_rocket.groups_create(test_group_name).get("group").get("_id")
    )
    return _test_group_id


def test_teams_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    teams_create = logged_rocket.teams_create(name=name, team_type=1)
    assert name == teams_create.get("team").get("name")
    logged_rocket.teams_delete(team_name=name)

    teams_create = logged_rocket.teams_create(name=name, team_type=1)
    team_id = teams_create.get("team").get("_id")
    logged_rocket.teams_delete(team_id=team_id)

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_delete()


def test_teams_list_all(logged_rocket):
    name = str(uuid.uuid1())
    logged_rocket.teams_create(name=name, team_type=1)

    iterated_teams = list(logged_rocket.teams_list_all())
    assert len(iterated_teams) >= 1

    for team in iterated_teams:
        assert "_id" in team
        assert "name" in team


def test_teams_info(logged_rocket, test_team_name, test_team_id):
    teams_info_by_id = logged_rocket.teams_info(team_id=test_team_id)
    assert "teamInfo" in teams_info_by_id
    assert teams_info_by_id.get("teamInfo").get("_id") == test_team_id

    teams_info_by_name = logged_rocket.teams_info(team_name=test_team_name)
    assert "teamInfo" in teams_info_by_name
    assert teams_info_by_name.get("teamInfo").get("_id") == test_team_id

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_info()


def test_teams_members(logged_rocket, test_team_name, test_team_id):
    iterated_members = list(logged_rocket.teams_members(team_id=test_team_id))
    assert len(iterated_members) > 0, "Should have at least one member"

    for member in iterated_members:
        assert "user" in member
        assert "_id" in member.get("user")

    # Test by team name
    iterated_members_by_name = list(
        logged_rocket.teams_members(team_name=test_team_name)
    )
    assert len(iterated_members_by_name) > 0

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_members()


def test_teams_add_update_remove_members(logged_rocket, test_team_id, testuser_id):
    logged_rocket.teams_add_members(
        team_id=test_team_id,
        members=[
            {
                "userId": testuser_id,
                "roles": [
                    "member",
                ],
            }
        ],
    )

    teams_members = list(logged_rocket.teams_members(team_id=test_team_id))
    assert len(teams_members) == 2
    user_ids = [member.get("user").get("_id") for member in teams_members]
    assert testuser_id in user_ids

    # Make testuser owner
    logged_rocket.teams_update_member(
        team_id=test_team_id, member={"userId": testuser_id, "roles": ["owner"]}
    )

    teams_members = list(logged_rocket.teams_members(team_id=test_team_id))
    testuser_member = list(
        filter(
            lambda member: member.get("user").get("_id") == testuser_id,
            teams_members,
        )
    )[0]
    assert "owner" in testuser_member.get("roles")

    logged_rocket.teams_remove_member(team_id=test_team_id, user_id=testuser_id)
    teams_members = list(logged_rocket.teams_members(team_id=test_team_id))
    assert len(teams_members) == 1

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_add_members()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_update_member()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_remove_member()


def test_teams_add_update_remove_members_team_name(
    logged_rocket, test_team_name, test_team_id, testuser_id
):
    logged_rocket.teams_add_members(
        team_name=test_team_name,
        members=[
            {
                "userId": testuser_id,
                "roles": [
                    "member",
                ],
            }
        ],
    )

    teams_members = list(logged_rocket.teams_members(team_name=test_team_name))
    assert len(teams_members) == 2
    user_ids = [member.get("user").get("_id") for member in teams_members]
    assert testuser_id in user_ids

    # Make testuser owner
    logged_rocket.teams_update_member(
        team_name=test_team_name, member={"userId": testuser_id, "roles": ["owner"]}
    )

    teams_members = list(logged_rocket.teams_members(team_name=test_team_name))
    testuser_member = list(
        filter(
            lambda member: member.get("user").get("_id") == testuser_id,
            teams_members,
        )
    )[0]
    assert "owner" in testuser_member.get("roles")

    logged_rocket.teams_remove_member(team_name=test_team_name, user_id=testuser_id)
    teams_members = list(logged_rocket.teams_members(team_name=test_team_name))
    assert len(teams_members) == 1


def test_teams_list_rooms(logged_rocket, test_team_name, test_team_id):
    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_list_rooms()


def test_teams_add_update_remove_rooms(logged_rocket, test_team_id, test_group_id):
    created_room = logged_rocket.teams_add_rooms(
        team_id=test_team_id, rooms=[test_group_id]
    )
    assert "rooms" in created_room
    assert created_room.get("rooms")[0]["_id"] == test_group_id

    teams_rooms = list(logged_rocket.teams_list_rooms(team_id=test_team_id))
    assert len(teams_rooms) == 1
    assert teams_rooms[0]["_id"] == test_group_id

    teams_update_room = logged_rocket.teams_update_room(test_group_id, is_default=True)
    assert teams_update_room.get("room")["_id"] == test_group_id
    assert teams_update_room.get("room")["teamDefault"]

    teams_rooms = list(logged_rocket.teams_list_rooms(team_id=test_team_id))
    assert len(teams_rooms) == 1
    assert teams_rooms[0]["_id"] == test_group_id
    assert teams_rooms[0]["teamDefault"]

    logged_rocket.teams_remove_room(team_id=test_team_id, room_id=test_group_id)

    teams_rooms = list(logged_rocket.teams_list_rooms(team_id=test_team_id))
    assert len(teams_rooms) == 0


def test_teams_add_update_remove_rooms_name(
    logged_rocket, test_team_name, test_team_id, test_group_id
):
    created_room = logged_rocket.teams_add_rooms(
        team_name=test_team_name, rooms=[test_group_id]
    )
    assert "rooms" in created_room
    assert created_room.get("rooms")[0]["_id"] == test_group_id

    teams_rooms = list(logged_rocket.teams_list_rooms(team_name=test_team_name))
    assert len(teams_rooms) == 1
    assert teams_rooms[0]["_id"] == test_group_id

    teams_update_room = logged_rocket.teams_update_room(test_group_id, is_default=True)
    assert teams_update_room.get("room")["_id"] == test_group_id
    assert teams_update_room.get("room")["teamDefault"]

    teams_rooms = list(logged_rocket.teams_list_rooms(team_name=test_team_name))
    assert len(teams_rooms) == 1
    assert teams_rooms[0]["_id"] == test_group_id
    assert teams_rooms[0]["teamDefault"]

    logged_rocket.teams_remove_room(team_name=test_team_name, room_id=test_group_id)

    teams_rooms = list(logged_rocket.teams_list_rooms(team_name=test_team_name))
    assert len(teams_rooms) == 0

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_add_rooms()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_remove_room()
