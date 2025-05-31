"""Application factory."""

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apscheduler import APScheduler
from .config import DevelopmentConfig

# Extensions

db = SQLAlchemy()
scheduler = APScheduler()


def _setup_logging(log_file: str, level: str) -> None:
    """Configure logging for the application."""
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=2)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=[handler],
        force=True,
    )


def create_app(config_class=DevelopmentConfig) -> Flask:
    """Create Flask app with provided configuration."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    _setup_logging(app.config['LOG_FILE'], app.config['LOG_LEVEL'])
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from .routes import register_blueprints
    register_blueprints(app)

    return app
