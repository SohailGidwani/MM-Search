import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('app.env'))

class Config:
    SECRET_KEY               = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI  = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER            = os.path.join(os.getcwd(), 'uploads')
    CELERY_BROKER_URL        = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND    = 'redis://localhost:6379/0'
    QDRANT_URL               = os.getenv('QDRANT_URL')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')