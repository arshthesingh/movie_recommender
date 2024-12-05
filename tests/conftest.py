import pytest
from app import create_app, db


@pytest.fixture
def app():
    """
    Set up the Flask application for testing.
    """
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            # uses in memory DB for tests
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  
            "SECRET_KEY": "test_secret_key",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Provides a test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Provides a test CLI runner.
    """
    return app.test_cli_runner()
