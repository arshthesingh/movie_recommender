from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.movie_recommendation import get_movie_recommendations

recommendations_blueprint = Blueprint("recommendations", __name__)


@recommendations_blueprint.route("/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    title = request.args.get("title")

    if not title:
        return jsonify({"error": "Movie title is required"}), 400

    recommendations = get_movie_recommendations(title)

    if not recommendations:
        return jsonify({"error": f"No recommendations found for {title}"}), 404

    return jsonify(recommendations), 200
