def test_user_not_in_team(client, auth_header):
    response = client.post(
        "/projects",
        json={"name": "Test", "team_id": 999},
        headers=auth_header
    )
    assert response.status_code == 403


