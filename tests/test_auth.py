import uuid
from app.models import User, db


def test_register_success(client):
    """
    Test successful user registration.
    """
    unique_username = f"user_{uuid.uuid4().hex[:8]}"  # Generate a unique username
    response = client.post("/api/auth/register", json={
        "username": unique_username,
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}

    # Verify user was added to the database
    with client.application.app_context():
        user = User.query.filter_by(username=unique_username).first()
        assert user is not None
        assert user.username == unique_username


def test_register_missing_fields(client):
    """
    Test user registration with missing fields.
    """
    response = client.post("/api/auth/register", json={
        "username": "testuser"
    })  # Missing password
    assert response.status_code == 400
    assert response.json == {"error": "Username and password are required"}


def test_register_duplicate_user(client):
    """
    Test user registration with a duplicate username.
    """
    with client.application.app_context():
        # Add a user to the database
        db.session.add(User(username="testuser", password="hashedpassword"))
        db.session.commit()

    # Attempt registration w/ the same username
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json == {"error": "Username already exists"}
    

def test_login_success(client):
    """
    Test successful login.
    """
    # Register a user first
    client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })

    # Attempt to log in
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_credentials(client):
    """
    Test login with invalid credentials.
    """
    response = client.post("/api/auth/login", json={
        "username": "invaliduser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json == {"error": "Invalid username or password"}


def test_logout_success(client):
    """
    Test successful logout.
    """
    # Register and log in
    client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })

    token = login_response.json["access_token"]

    # Logout
    response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json == {"message": "User 'testuser' logged out successfully"}  