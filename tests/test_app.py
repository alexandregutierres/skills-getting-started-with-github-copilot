def test_get_activities(client):
    # Arrange: none needed (app has default data)

    # Act: GET /activities
    response = client.get("/activities")

    # Assert: status 200, response is dict with "Chess Club" key
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_participant(client):
    # Arrange: choose unique email not in default data
    email = "test@example.com"

    # Act: POST /activities/Chess Club/signup?email=test@example.com
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert: status 200, participant added to "Chess Club" in GET /activities
    assert response.status_code == 200
    data = client.get("/activities").json()
    assert email in data["Chess Club"]["participants"]


def test_signup_duplicate(client):
    # Arrange: sign up email once
    email = "duplicate@example.com"
    client.post("/activities/Chess Club/signup", params={"email": email})

    # Act: POST /activities/Chess Club/signup?email=duplicate@example.com again
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert: status 400, detail "Student already signed up"
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    # Arrange: sign up email first
    email = "remove@example.com"
    client.post("/activities/Chess Club/signup", params={"email": email})

    # Act: DELETE /activities/Chess Club/participants?email=remove@example.com
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert: status 200, participant removed from "Chess Club"
    assert response.status_code == 200
    data = client.get("/activities").json()
    assert email not in data["Chess Club"]["participants"]


def test_remove_missing_participant(client):
    # Arrange: none (use non-existent email)
    email = "missing@example.com"

    # Act: DELETE /activities/Chess Club/participants?email=missing@example.com
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    # Assert: status 404, detail "Participant not found"
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"