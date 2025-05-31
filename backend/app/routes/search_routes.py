"""Search API endpoints."""
from flask import Blueprint, request, jsonify

from ..services.search_service import SearchService

search_bp = Blueprint('search', __name__)


@search_bp.route('', methods=['POST'])
def search():
    """Perform search."""
    body = request.get_json(force=True)
    query = body.get('query', '')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    service = SearchService()
    result = service.search(query)
    return jsonify(result)


@search_bp.route('/suggestions', methods=['GET'])
def suggestions():
    """Return static suggestions placeholder."""
    return jsonify({'suggestions': []})


@search_bp.route('/history', methods=['GET'])
def history():
    """Return search history placeholder."""
    return jsonify([])
