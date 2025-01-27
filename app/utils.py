from flask_jwt_extended import get_jwt_identity
from app.models import User


def get_current_user():
    """
    Retrieves the currently logged-in user based on the JWT.
    """
    current_identity = get_jwt_identity()

    print("Current JWT Identity (username):", current_identity)
    user = User.query.filter_by(username=current_identity).first()

    if not user:
        raise ValueError("User not found")

    print("Retrieved User:", user)
    return user
