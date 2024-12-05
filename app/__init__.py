import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "sqlite:///site.db"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True,
    )

    from app.auth import auth_blueprint
    from app.watchlist import watchlist_blueprint
    from app.recommendations import recommendations_blueprint
    from app.routes import api

    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(watchlist_blueprint, url_prefix="/api/watchlist")
    app.register_blueprint(recommendations_blueprint, url_prefix="/api")
    app.register_blueprint(api)

    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "site.db")
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()

    return app
