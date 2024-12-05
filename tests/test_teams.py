import uuid

import pytest

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException


@pytest.fixture
def test_team_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_team_id(test_team_name, logged_rocket):
    _test_team_id = (
        logged_rocket.teams_create(name=test_team_name, team_type=1)
        .json()
        .get("team")
        .get("_id")
    )
    return _test_team_id


@pytest.fixture
def testuser_id(logged_rocket):
    testuser = logged_rocket.users_info(username="testuser1").json()

    _testuser_id = testuser.get("user").get("_id")

    yield _testuser_id

    logged_rocket.users_delete(_testuser_id)


@pytest.fixture
def test_group_name():
    return str(uuid.uuid1())


@pytest.fixture
def test_group_id(test_group_name, logged_rocket):
    _test_group_id = (
        logged_rocket.groups_create(test_group_name).json().get("group").get("_id")
    )
    return _test_group_id


def test_teams_create_delete(logged_rocket):
    name = str(uuid.uuid1())
    teams_create = logged_rocket.teams_create(name=name, team_type=1).json()
    assert teams_create.get("success")
    assert name == teams_create.get("team").get("name")
    teams_delete = logged_rocket.teams_delete(team_name=name).json()
    assert teams_delete.get("success")
    teams_create = logged_rocket.teams_create(name=name, team_type=1).json()
    assert teams_create.get("success")
    team_id = teams_create.get("team").get("_id")
    teams_delete = logged_rocket.teams_delete(team_id=team_id).json()
    assert teams_delete.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_delete()


def test_teams_list_all(logged_rocket):
    teams_list = logged_rocket.teams_list_all().json()
    assert teams_list.get("success")
    assert "teams" in teams_list


def test_teams_info(logged_rocket, test_team_name, test_team_id):
    teams_info_by_id = logged_rocket.teams_info(team_id=test_team_id).json()
    assert teams_info_by_id.get("success")
    assert "teamInfo" in teams_info_by_id
    assert teams_info_by_id.get("teamInfo").get("_id") == test_team_id

    teams_info_by_name = logged_rocket.teams_info(team_name=test_team_name).json()
    assert teams_info_by_name.get("success")
    assert "teamInfo" in teams_info_by_name
    assert teams_info_by_name.get("teamInfo").get("_id") == test_team_id

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_info()


def test_teams_members(logged_rocket, test_team_name, test_team_id):
    teams_members = logged_rocket.teams_members(team_id=test_team_id).json()
    assert teams_members.get("success")
    teams_members = logged_rocket.teams_members(team_name=test_team_name).json()
    assert teams_members.get("success")

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_members()


def test_teams_add_update_remove_members(logged_rocket, test_team_id, testuser_id):
    teams_add_members = logged_rocket.teams_add_members(
        team_id=test_team_id,
        members=[
            {
                "userId": testuser_id,
                "roles": [
                    "member",
                ],
            }
        ],
    ).json()
    assert teams_add_members.get("success"), teams_add_members.get("error")

    teams_members = logged_rocket.teams_members(team_id=test_team_id).json()
    assert teams_members.get("success")
    assert "members" in teams_members
    assert len(teams_members.get("members")) == 2
    user_ids = [
        member.get("user").get("_id") for member in teams_members.get("members")
    ]
    assert testuser_id in user_ids

    # Make testuser owner
    teams_update_member = logged_rocket.teams_update_member(
        team_id=test_team_id, member={"userId": testuser_id, "roles": ["owner"]}
    ).json()
    assert teams_update_member.get("success"), teams_update_member.get("error")

    teams_members = logged_rocket.teams_members(team_id=test_team_id).json()
    testuser_member = list(
        filter(
            lambda member: member.get("user").get("_id") == testuser_id,
            teams_members.get("members"),
        )
    )[0]
    assert "owner" in testuser_member.get("roles")

    teams_remove_member = logged_rocket.teams_remove_member(
        team_id=test_team_id, user_id=testuser_id
    ).json()
    assert teams_remove_member.get("success"), teams_remove_member.get("error")
    teams_members = logged_rocket.teams_members(team_id=test_team_id).json()
    assert "members" in teams_members
    assert len(teams_members.get("members")) == 1

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_add_members()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_update_member()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_remove_member()


def test_teams_add_update_remove_members_team_name(
    logged_rocket, test_team_name, test_team_id, testuser_id
):
    teams_add_members = logged_rocket.teams_add_members(
        team_name=test_team_name,
        members=[
            {
                "userId": testuser_id,
                "roles": [
                    "member",
                ],
            }
        ],
    ).json()
    assert teams_add_members.get("success"), teams_add_members.get("error")

    teams_members = logged_rocket.teams_members(team_name=test_team_name).json()
    assert teams_members.get("success")
    assert "members" in teams_members
    assert len(teams_members.get("members")) == 2
    user_ids = [
        member.get("user").get("_id") for member in teams_members.get("members")
    ]
    assert testuser_id in user_ids

    # Make testuser owner
    teams_update_member = logged_rocket.teams_update_member(
        team_name=test_team_name, member={"userId": testuser_id, "roles": ["owner"]}
    ).json()
    assert teams_update_member.get("success"), teams_update_member.get("error")

    teams_members = logged_rocket.teams_members(team_name=test_team_name).json()
    testuser_member = list(
        filter(
            lambda member: member.get("user").get("_id") == testuser_id,
            teams_members.get("members"),
        )
    )[0]
    assert "owner" in testuser_member.get("roles")

    teams_remove_member = logged_rocket.teams_remove_member(
        team_name=test_team_name, user_id=testuser_id
    ).json()
    assert teams_remove_member.get("success"), teams_remove_member.get("error")
    teams_members = logged_rocket.teams_members(team_name=test_team_name).json()
    assert "members" in teams_members
    assert len(teams_members.get("members")) == 1


def test_teams_list_rooms(logged_rocket, test_team_name, test_team_id):
    teams_rooms = logged_rocket.teams_list_rooms(
        team_id=test_team_id, room_type=1
    ).json()
    assert teams_rooms.get("success")
    assert "rooms" in teams_rooms

    teams_rooms_name = logged_rocket.teams_list_rooms(
        team_name=test_team_name, room_type=1
    ).json()
    assert teams_rooms_name.get("success")
    assert "rooms" in teams_rooms_name

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_list_rooms()


def test_teams_add_update_remove_rooms(logged_rocket, test_team_id, test_group_id):
    created_room = logged_rocket.teams_add_rooms(
        team_id=test_team_id, rooms=[test_group_id]
    ).json()
    assert created_room.get("success"), created_room.get("error")
    assert "rooms" in created_room
    assert created_room.get("rooms")[0]["_id"] == test_group_id

    teams_rooms = logged_rocket.teams_list_rooms(team_id=test_team_id).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 1
    assert teams_rooms.get("rooms")[0]["_id"] == test_group_id

    teams_update_room = logged_rocket.teams_update_room(
        test_group_id, is_default=True
    ).json()
    assert teams_update_room.get("success"), teams_update_room.get("success")
    assert teams_update_room.get("room")["_id"] == test_group_id
    assert teams_update_room.get("room")["teamDefault"]

    teams_rooms = logged_rocket.teams_list_rooms(team_id=test_team_id).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 1
    assert teams_rooms.get("rooms")[0]["_id"] == test_group_id
    assert teams_rooms.get("rooms")[0]["teamDefault"]

    teams_remove_room = logged_rocket.teams_remove_room(
        team_id=test_team_id, room_id=test_group_id
    ).json()
    assert teams_remove_room.get("success"), teams_remove_room.get("error")

    teams_rooms = logged_rocket.teams_list_rooms(team_id=test_team_id).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 0


def test_teams_add_update_remove_rooms_name(
    logged_rocket, test_team_name, test_team_id, test_group_id
):
    created_room = logged_rocket.teams_add_rooms(
        team_name=test_team_name, rooms=[test_group_id]
    ).json()
    assert created_room.get("success"), created_room.get("error")
    assert "rooms" in created_room
    assert created_room.get("rooms")[0]["_id"] == test_group_id

    teams_rooms = logged_rocket.teams_list_rooms(team_name=test_team_name).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 1
    assert teams_rooms.get("rooms")[0]["_id"] == test_group_id

    teams_update_room = logged_rocket.teams_update_room(
        test_group_id, is_default=True
    ).json()
    assert teams_update_room.get("success"), teams_update_room.get("success")
    assert teams_update_room.get("room")["_id"] == test_group_id
    assert teams_update_room.get("room")["teamDefault"]

    teams_rooms = logged_rocket.teams_list_rooms(team_name=test_team_name).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 1
    assert teams_rooms.get("rooms")[0]["_id"] == test_group_id
    assert teams_rooms.get("rooms")[0]["teamDefault"]

    teams_remove_room = logged_rocket.teams_remove_room(
        team_name=test_team_name, room_id=test_group_id
    ).json()
    assert teams_remove_room.get("success"), teams_remove_room.get("error")

    teams_rooms = logged_rocket.teams_list_rooms(team_name=test_team_name).json()
    assert teams_rooms.get("success"), teams_rooms.get("error")
    assert len(teams_rooms.get("rooms")) == 0

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_add_rooms()

    with pytest.raises(RocketMissingParamException):
        logged_rocket.teams_remove_room()
