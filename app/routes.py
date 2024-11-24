from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app import db, bcrypt
from app.models import User, Watchlist
from app.movie_recommendation import get_recommendations
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)


@api.route("/api/watchlist", methods=["GET"])
@jwt_required()
def view_watchlist():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    
    watchlist = Watchlist.query.filter_by(user_id=user.id).order_by(Watchlist.priority).all()
    
    movies = [{"title": entry.movie_title, "priority": entry.priority} for entry in watchlist]

    return jsonify(movies), 200


@api.route("/api/watchlist/add", method=["POST"])
@jwt_required()
def add_to_watchlist():
    data = request.json
    movie_title = data.get('movie_title')

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if Watchlist.query.filter_by(user_id=user.id, movie_title=movie_title).first():
        return jsonify({"error": f'"{movie_title}" is already in your watchlist'}), 400
    
    highest_priority = db.session.query(db.func.max(Watchlist.priority)).filter_by(user_id=user.id).scalar()

    new_priority = (highest_priority or 0) + 1

    new_watchlist_entry = Watchlist(user_id=user.id, movie_title=movie_title, priority=new_priority)
    db.session.add(new_watchlist_entry)
    db.session.commit()

    return jsonify({"message": f'"{movie_title}" added to your watchlist!'}), 200


@api.route("/api/watchlist/remove", methods=["POST"])
@jwt_required()
def remove_from_watchlist():
    data = request.json
    movie_title = data.get('movie_title')

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    watchlist_entry = Watchlist.query.filter_by(user_id=user.id, movie_title=movie_title).first()

    if not watchlist_entry:
        return jsonify({"error": f'"{movie_title}" is not in your watchlist'}), 404

    db.session.delete(watchlist_entry)
    db.session.commit()

    return jsonify({"message": f'"{movie_title}" removed from your watchlist!'}), 200
