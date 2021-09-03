import uuid


def test_team_create(logged_rocket):
    name = str(uuid.uuid1())
    team_create = logged_rocket.teams_create(
        name=name,
        team_type=1,
    ).json()
    assert team_create.get("success")
    assert "team" in team_create
    assert team_create.get("team").get("name") == name
    assert team_create.get("team").get("type") == 1
