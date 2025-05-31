"""Search log model."""
from datetime import datetime
from .. import db

class SearchLog(db.Model):
    __tablename__ = 'search_logs'

    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    results_count = db.Column(db.Integer)
    search_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_time_ms = db.Column(db.Integer)
    user_id = db.Column(db.String(100))
    filters_applied = db.Column(db.JSON)

    def __repr__(self) -> str:
        return f"<SearchLog {self.query[:20]}>"
