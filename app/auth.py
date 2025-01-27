from flask import Blueprint, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db, bcrypt

auth_blueprint = Blueprint("auth", __name__)
CORS(auth_blueprint)


@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    """
    Registers a new user.
    """

    data = request.json
    print("Parsed JSON:", data)

    username = data.get("username")
    password = data.get("password")

    # Validating input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login_user_api():
    """
    Logs in a user and returns a JWT.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return (
            jsonify(
                {"message": "Logged in successfully", "access_token": access_token}
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 401


@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout_user_api():
    """
    Logs out the user. JWTs are stateless, so logout is just an acknowledgment.
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"User '{current_user}' logged out successfully"}), 200
