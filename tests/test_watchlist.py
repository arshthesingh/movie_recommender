def test_add_to_watchlist_success(client):
    """
    Test adding a movie to the watchlist successfully.
    """
    # Register and log in
    client.post(
        "/api/auth/register", json={"username": "testuser", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/auth/login", json={"username": "testuser", "password": "testpassword"}
    )

    # Debugging: Print the token received
    token = login_response.json["access_token"]
    print("Access Token:", token)

    # Add a movie
    response = client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Debugging: Print the response
    print("Add to Watchlist Response:", response.json)

    # Assertions
    assert response.status_code == 200
    assert response.json == {"message": '"Inception" added to your watchlist!'}


def test_view_watchlist(client):
    """
    Test viewing the user's watchlist.
    """
    # Register and log in
    client.post(
        "/api/auth/register", json={"username": "testuser2", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/auth/login", json={"username": "testuser2", "password": "testpassword"}
    )
    token = login_response.json["access_token"]

    # Add movies to the watchlist
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Titanic"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # View the watchlist
    response = client.get(
        "/api/watchlist", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json == [
        {"title": "Inception", "priority": 1},
        {"title": "Titanic", "priority": 2},
    ]


def test_add_duplicate_movie(client):
    """
    Test adding a duplicate movie to the watchlist.
    """
    # Register and log in
    client.post(
        "/api/auth/register", json={"username": "testuser3", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/auth/login", json={"username": "testuser3", "password": "testpassword"}
    )
    token = login_response.json["access_token"]

    # Add a movie
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Attempt to add the same movie again
    response = client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json == {"error": '"Inception" is already in your watchlist'}


def test_remove_from_watchlist(client):
    """
    Test removing a movie from the watchlist.
    """
    # Register and log in
    client.post(
        "/api/auth/register", json={"username": "testuser4", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/auth/login", json={"username": "testuser4", "password": "testpassword"}
    )
    token = login_response.json["access_token"]

    # Add a movie
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Remove the movie
    response = client.post(
        "/api/watchlist/remove",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": '"Inception" removed from your watchlist!'}


def test_move_movie_up(client):
    """
    Test moving a movie up in the watchlist.
    """
    # Register and log in
    client.post(
        "/api/auth/register", json={"username": "testuser5", "password": "testpassword"}
    )
    login_response = client.post(
        "/api/auth/login", json={"username": "testuser5", "password": "testpassword"}
    )
    token = login_response.json["access_token"]

    # Add movies to the watchlist
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Titanic"},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/api/watchlist/add",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Move "Inception" up
    response = client.post(
        "/api/watchlist/move-up",
        json={"movie_title": "Inception"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json == {"message": '"Inception" moved up in the watchlist'}
