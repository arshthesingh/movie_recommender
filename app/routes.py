from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import db, bcrypt
from app.models import User, Watchlist
from app.movie_recommendation import get_movie_recommendations

from flask_cors import CORS

api = Blueprint("api", __name__)
CORS(api)

from app import create_app
from flask import Flask, jsonify, send_from_directory

app = create_app()


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the backend API!"})


if __name__ == "__main__":
    app.run(debug=True)


# Route to serve Swagger YAML file
@app.route("/static/swagger.yaml")
def serve_swagger_yaml():
    return send_from_directory("static", "swagger.yaml")
