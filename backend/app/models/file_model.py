# backend/app/models/file_model.py
from app import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class File(db.Model):
    __tablename__ = 'files'

    id                = db.Column(db.Integer, primary_key=True)
    filename          = db.Column(db.String(255),  nullable=False)
    original_filename = db.Column(db.String(255),  nullable=False)
    file_path         = db.Column(db.Text,         nullable=False)
    file_type         = db.Column(db.String(50),   nullable=False)
    file_size         = db.Column(db.BigInteger,   nullable=False)
    mime_type         = db.Column(db.String(100))
    upload_timestamp  = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(50), default='pending')
    user_id           = db.Column(db.String(100))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at        = db.Column(db.DateTime,
                                  default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

    chunks = db.relationship("ContentChunk", back_populates="file",
                             cascade="all, delete-orphan")


class ContentChunk(db.Model):
    __tablename__ = 'content_chunks'

    id            = db.Column(db.Integer, primary_key=True)
    file_id       = db.Column(db.Integer, db.ForeignKey('files.id'), index=True)
    chunk_type    = db.Column(db.String(50),  nullable=False)    # text/image/audio/video
    content_text  = db.Column(db.Text)
    chunk_index   = db.Column(db.Integer)
    start_time    = db.Column(db.Float)
    end_time      = db.Column(db.Float)
    extra_metadata = db.Column("metadata", JSONB)   # 👈 renamed but keeps DB column name
    vector_id     = db.Column(db.String(100))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    file = db.relationship("File", back_populates="chunks")


class SearchLog(db.Model):
    __tablename__ = 'search_logs'

    id               = db.Column(db.Integer, primary_key=True)
    query            = db.Column(db.Text, nullable=False)
    results_count    = db.Column(db.Integer)
    response_time_ms = db.Column(db.Integer)
    search_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id          = db.Column(db.String(100))