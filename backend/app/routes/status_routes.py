"""System status endpoints."""
from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)


@status_bp.route('/status', methods=['GET'])
def status():
    """Health check."""
    return jsonify({'status': 'ok'})


@status_bp.route('/stats', methods=['GET'])
def stats():
    """Return basic statistics placeholder."""
    return jsonify({})
