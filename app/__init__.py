from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录后使用"
login_manager.session_protection = "basic"


def dateformat(value, fmt="%Y-%m-%d %H:%M"):
    return value.strftime(fmt)


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.jinja_env.filters['dateformat'] = dateformat
    config[config_name].init__app(app)
    db.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .file import file as file_blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(admin_blueprint)

    return app