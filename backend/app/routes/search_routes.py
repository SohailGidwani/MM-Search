# app/routes/search_routes.py
from flask import Blueprint, request, jsonify
from app.services.search_service import SearchService
from app.utils.logger import logger_msg
from app.models.file_model import db, SearchLog

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('', methods=['POST'])
def search():
    data  = request.get_json(force=True)
    query = data.get('query')
    if not query:
        return jsonify({"error": "Missing 'query'"}), 400

    results, latency = SearchService.search_text(query)
    # log
    log = SearchLog(query=query, results_count=len(results),
                    response_time_ms=latency)
    db.session.add(log); db.session.commit()

    logger_msg(f"Logged search id={log.id}", "debug")
    return jsonify({
        "query":    query,
        "latency":  latency,
        "results":  results
    })