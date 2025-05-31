"""File model."""
from datetime import datetime
from .. import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    mime_type = db.Column(db.String(100))
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(50), default='pending')
    processing_started_at = db.Column(db.DateTime)
    processing_completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    user_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chunks = db.relationship('ContentChunk', backref='file', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<File {self.filename}>"
