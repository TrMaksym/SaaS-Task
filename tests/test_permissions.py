def test_user_not_in_team(client, auth_header):
    response = client.post(
        "/projects",
        json={"name": "Test", "team_id": 999},
        headers=auth_header
    )
    assert response.status_code == 403

def test_user_not_owner(client, auth_header):
    team_id = 1
    payload = {"name": "Test"}
    response = client.post(
        f"/teams/{team_id}/projects",
        json=payload,
        headers=auth_header
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Owner only"

def test_user_is_owner(client, auth_header):
    team_id = 1
    payload = {"name": "Test", "role": "owner"}
    response = client.post(
        f"/teams/{team_id}/projects",
        json=payload,
        headers=auth_header
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Access successful"