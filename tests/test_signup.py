def test_signup_successful(client):
    """Test successful signup for an activity"""
    # Arrange - client fixture and test data
    activity_name = "Basketball Team"
    email = "test@example.com"

    # Act - make POST request to signup endpoint
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert - verify successful response and participant added
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was actually added to the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404"""
    # Arrange - client fixture and invalid activity name
    invalid_activity = "NonExistent Activity"
    email = "test@example.com"

    # Act - make POST request with invalid activity
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})

    # Assert - verify 404 error response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_already_signed_up(client):
    """Test signup when student is already signed up returns 400"""
    # Arrange - client fixture and existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club from initial data

    # Act - attempt to signup again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert - verify 400 error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]