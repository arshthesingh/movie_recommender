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
