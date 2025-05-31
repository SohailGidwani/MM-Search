# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
from flask_migrate import Migrate         # ready for future use
from dotenv import load_dotenv, find_dotenv
import os, sys

from app.utils.logger import logger_msg, handle_exception

# ──────────────────────────────────────────────────────────────
# Environment
# ──────────────────────────────────────────────────────────────
load_dotenv(find_dotenv('app.env'))

db       = SQLAlchemy()
migrate  = Migrate()                       # optional but harmless

# ──────────────────────────────────────────────────────────────
# Celery helper
# ──────────────────────────────────────────────────────────────
def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker = app.config['CELERY_BROKER_URL'],
        backend= app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# ──────────────────────────────────────────────────────────────
# Factory
# ──────────────────────────────────────────────────────────────
def create_app(config_name: str = 'development'):
    app = Flask(__name__)
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)              # no-op until you run flask db …
    CORS(app)
    celery = make_celery(app)

    # Global exception hook
    sys.excepthook = handle_exception

    # ── Auto-create tables (dev or explicit opt-in) ───────────────────────
    if app.config.get('DEBUG') or os.getenv('AUTO_DB_CREATE', 'false').lower() == 'true':
        with app.app_context():
            logger_msg("Running db.create_all() (auto-create enabled)", "info")
            db.create_all()

    # Blueprints
    from app.routes.upload_routes import upload_bp
    from app.routes.search_routes import search_bp
    from app.routes.file_routes   import file_bp

    app.register_blueprint(upload_bp, url_prefix='/api/uploads')
    app.register_blueprint(search_bp,  url_prefix='/api/search')
    app.register_blueprint(file_bp,    url_prefix='/api/files')

    logger_msg("Flask application initialized.", "info")
    return app, celery