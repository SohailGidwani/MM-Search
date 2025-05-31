"""Register blueprints."""

from flask import Flask

from .upload_routes import upload_bp
from .search_routes import search_bp
from .file_routes import file_bp
from .status_routes import status_bp


def register_blueprints(app: Flask) -> None:
    """Register all blueprints."""
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(file_bp, url_prefix='/api/files')
    app.register_blueprint(status_bp, url_prefix='/api')
