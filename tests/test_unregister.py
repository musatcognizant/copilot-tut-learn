def test_unregister_successful(client):
    """Test successful unregister from an activity"""
    # Arrange - client fixture and existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act - make DELETE request to unregister endpoint
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert - verify successful response and participant removed
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify participant was actually removed from the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity returns 404"""
    # Arrange - client fixture and invalid activity name
    invalid_activity = "NonExistent Activity"
    email = "test@example.com"

    # Act - make DELETE request with invalid activity
    response = client.delete(f"/activities/{invalid_activity}/unregister", params={"email": email})

    # Assert - verify 404 error response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_signed_up(client):
    """Test unregister when student is not signed up returns 400"""
    # Arrange - client fixture and student not in activity
    activity_name = "Basketball Team"
    email = "notsignedup@example.com"  # Not in Basketball Team

    # Act - attempt to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert - verify 400 error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up" in data["detail"]