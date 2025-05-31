"""System status endpoints."""
import logging
from flask import Blueprint, jsonify

status_bp = Blueprint('status', __name__)
logger = logging.getLogger(__name__)


@status_bp.route('/status', methods=['GET'])
def status():
    """Health check."""
    logger.info("/status called")
    return jsonify({'status': 'ok'})


@status_bp.route('/stats', methods=['GET'])
def stats():
    """Return basic statistics placeholder."""
    logger.info("/status/stats called")
    return jsonify({})
