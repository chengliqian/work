from app import app, db, celery
from app.models import ServerMonitor, User, Role, NexApiCase, Url
from flask_script import Manager, Shell, Command, Option, Server
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                ServerMonitor=ServerMonitor, NexApiCase=NexApiCase)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
	manager.run()