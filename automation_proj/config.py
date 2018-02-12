import os
basedir = os.path.abspath(os.path.dirname(__file__))
download_url = basedir+"\doc"
from flask_uploads import DOCUMENTS

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False

    # sql
    DEV_DATABASE_URL = 'mysql+pymysql://root:123456@10.165.124.22:3306/qa_test'
    # SQLALCHEMY_ECHO=True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = DEV_DATABASE_URL or os.environ.get('DATABASE_URL')

    # flask_uploads document
    UPLOADED_DOCUMENT_DEST = './app/static/uploads/'
    UPLOADED_DOCUMENT_ALLOW = DOCUMENTS
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'])

    # celery
    CELERY_TIMEZONE='Asia/Shanghai'
    CELERY_BROKER_URL = 'redis://:123456@10.165.124.28:9208/0'
    CELERY_RESULT_BACKEND = 'redis://:123456@10.165.124.28:9208/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_EVENT_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    @staticmethod
    def init_app(app):
        pass