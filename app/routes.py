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

