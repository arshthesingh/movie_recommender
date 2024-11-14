from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import db, bcrypt
from app.models import User, Watchlist
from app.movie_recommendation import get_recommendations
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)

@api.route("/api/register", methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@api.route("/api/login", methods=["POST"])
def login_user_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': username})
        return jsonify({"message": "Logged in successfully", "access_token": access_token}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401


@api.route("/api/logout", methods=["POST"])
@login_required
def logout_user_api():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

