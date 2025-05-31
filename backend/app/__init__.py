"""Application factory."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from .config import DevelopmentConfig

# Extensions

db = SQLAlchemy()
scheduler = APScheduler()


def create_app(config_class=DevelopmentConfig) -> Flask:
    """Create Flask app with provided configuration."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from .routes import register_blueprints
    register_blueprints(app)

    return app
