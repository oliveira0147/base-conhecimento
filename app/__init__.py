from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from markupsafe import Markup
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

def nl2br(value):
    if value:
        return Markup(value.replace('\n', '<br>\n'))
    return ''

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Registrar o filtro nl2br
    app.jinja_env.filters['nl2br'] = nl2br

    # Registrar blueprints
    from app.auth import auth
    app.register_blueprint(auth)

    # Importar e registrar o blueprint principal
    from app.routes import main
    app.register_blueprint(main)

    @login_manager.user_loader
    def load_user(id):
        from app.models import User
        return User.query.get(int(id))

    return app

from app import models 