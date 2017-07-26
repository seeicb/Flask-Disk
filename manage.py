from flask_script import Manager, Shell
from app.models import UserTable, FileTable
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, user_table=UserTable, file_table=FileTable)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    pass


@manager.command
def test():
    pass


@manager.command
def deploy():
    from app.models import UserTable
    UserTable.insert_admin()


if __name__ == "__main__":
    manager.run()
