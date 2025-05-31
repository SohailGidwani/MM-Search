"""Search API endpoints."""
from flask import Blueprint, request, jsonify

from ..services.search_service import SearchService

search_bp = Blueprint('search', __name__)


@search_bp.route('', methods=['POST'])
def search():
    """Perform search."""
    data = request.get_json(force=True)
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    service = SearchService()
    results = service.search(query)
    return jsonify({'results': results})


@search_bp.route('/suggestions', methods=['GET'])
def suggestions():
    """Return static suggestions placeholder."""
    return jsonify({'suggestions': []})


@search_bp.route('/history', methods=['GET'])
def history():
    """Return search history placeholder."""
    return jsonify([])
