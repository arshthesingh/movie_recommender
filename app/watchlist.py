from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Watchlist
from app import db
from app.utils import get_current_user

watchlist_blueprint = Blueprint("watchlist", __name__)


@watchlist_blueprint.route("/add", methods=["POST"])
@jwt_required()
def add_to_watchlist():
    """
    Adds a movie to the user's watchlist.
    """
    data = request.json
    print("Received Data:", data) 

    movie_title = data.get("movie_title")
    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    user = get_current_user()
    print("User:", user.username) 

    # Check for duplicates
    if Watchlist.query.filter_by(user_id=user.id, movie_title=movie_title).first():
        return jsonify({"error": f'"{movie_title}" is already in your watchlist'}), 400

    
    highest_priority = (
        db.session.query(db.func.max(Watchlist.priority))
        .filter_by(user_id=user.id)
        .scalar()
    )
    new_priority = (highest_priority or 0) + 1
    new_watchlist_entry = Watchlist(
        user_id=user.id, movie_title=movie_title, priority=new_priority
    )
    db.session.add(new_watchlist_entry)
    db.session.commit()

    print(
        f"Movie '{movie_title}' added to watchlist for user '{user.username}'"
    )  
    return jsonify({"message": f'"{movie_title}" added to your watchlist!'}), 200


@watchlist_blueprint.route("", methods=["GET"])
@jwt_required()
def view_watchlist():
    """
    Retrieves the user's watchlist, ordered by priority.
    """
    user = get_current_user()
    watchlist = (
        Watchlist.query.filter_by(user_id=user.id).order_by(Watchlist.priority).all()
    )
    movies = [
        {"title": entry.movie_title, "priority": entry.priority} for entry in watchlist
    ]
    return jsonify(movies), 200


@watchlist_blueprint.route("/remove", methods=["POST"])
@jwt_required()
def remove_from_watchlist():
    """
    Removes a movie from the user's watchlist.
    """
    data = request.json
    movie_title = data.get("movie_title")

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    user = get_current_user()
    watchlist_entry = Watchlist.query.filter_by(
        user_id=user.id, movie_title=movie_title
    ).first()

    if not watchlist_entry:
        return jsonify({"error": f'"{movie_title}" is not in your watchlist'}), 404

    db.session.delete(watchlist_entry)
    db.session.commit()

    return jsonify({"message": f'"{movie_title}" removed from your watchlist!'}), 200


@watchlist_blueprint.route("/move-up", methods=["POST"])
@jwt_required()
def move_movie_up():
    """
    Moves a movie up in the user's watchlist.
    """
    data = request.json
    movie_title = data.get("movie_title")

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    user = get_current_user()
    current_movie = Watchlist.query.filter_by(
        user_id=user.id, movie_title=movie_title
    ).first()

    if not current_movie:
        return jsonify({"error": f'"{movie_title}" is not in your watchlist'}), 404

    movie_above = Watchlist.query.filter_by(
        user_id=user.id, priority=current_movie.priority - 1
    ).first()

    if movie_above:
        current_movie.priority, movie_above.priority = (
            movie_above.priority,
            current_movie.priority,
        )
        db.session.commit()

    return jsonify({"message": f'"{movie_title}" moved up in the watchlist'}), 200


@watchlist_blueprint.route("/move-down", methods=["POST"])
@jwt_required()
def move_movie_down():
    """
    Moves a movie down in the user's watchlist.
    """
    data = request.json
    movie_title = data.get("movie_title")

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    user = get_current_user()
    current_movie = Watchlist.query.filter_by(
        user_id=user.id, movie_title=movie_title
    ).first()

    if not current_movie:
        return jsonify({"error": f'"{movie_title}" is not in your watchlist'}), 404

    movie_below = Watchlist.query.filter_by(
        user_id=user.id, priority=current_movie.priority + 1
    ).first()

    if movie_below:
        current_movie.priority, movie_below.priority = (
            movie_below.priority,
            current_movie.priority,
        )
        db.session.commit()

    return jsonify({"message": f'"{movie_title}" moved down in the watchlist'}), 200
