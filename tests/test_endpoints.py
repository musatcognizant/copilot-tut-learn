def test_root_redirect(client):
    """Test that GET / redirects to the static index page"""
    # Arrange - client fixture provides TestClient instance

    # Act - make GET request to root endpoint without following redirects
    response = client.get("/", follow_redirects=False)

    # Assert - verify redirect response
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange - client fixture provides TestClient instance

    # Act - make GET request to activities endpoint
    response = client.get("/activities")

    # Assert - verify response contains activity data
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Should have 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data

    # Verify structure of first activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)