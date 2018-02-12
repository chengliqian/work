from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import DOCUMENTS, UploadSet, configure_uploads
from config import Config
from celery import Celery
from celery.utils.log import get_task_logger

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
document_set = UploadSet('document')


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
	app = Flask(__name__)
	app.debug = True
	app.config.from_object(Config)
	configure_uploads(app, document_set)
	Config.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	db.init_app(app)

	return app

def create_celery(app):
	celery = Celery(
	    app.import_name,
	    backend=app.config['CELERY_RESULT_BACKEND'],
	    broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	TaskBase = celery.Task

	class ContextTask(TaskBase):
	    abstract = True
	    def __call__(self, *args, **kwargs):
	        with app.app_context():
	            return TaskBase.__call__(self, *args, **kwargs)

	celery.Task = ContextTask
	return celery

def register_app_blueprint(app):
	from .controllers import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .controllers import mointor as mointor_blueprint
	app.register_blueprint(mointor_blueprint, url_prefix='/mointor')

	from .controllers import case as case_blueprint
	app.register_blueprint(case_blueprint, url_prefix='/case')

	from .controllers import url as url_blueprint
	app.register_blueprint(url_blueprint, url_prefix='/url')

	from .controllers import dashboard as dashboard_blueprint
	app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

app = create_app()
celery = create_celery(app)
register_app_blueprint(app)