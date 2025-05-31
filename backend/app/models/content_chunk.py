"""Content chunk model."""
from datetime import datetime
from .. import db

class ContentChunk(db.Model):
    __tablename__ = 'content_chunks'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id', ondelete='CASCADE'))
    chunk_type = db.Column(db.String(50), nullable=False)
    content_text = db.Column(db.Text)
    chunk_index = db.Column(db.Integer)
    start_time = db.Column(db.Float)
    end_time = db.Column(db.Float)
    related_metadata = db.Column(db.JSON)
    vector_id = db.Column(db.String(100))
    embedding_model = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ContentChunk {self.id} of file {self.file_id}>"
