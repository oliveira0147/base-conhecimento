from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import jinja2

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

@login_manager.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Adiciona o filtro nl2br
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return s
        return jinja2.utils.markupsafe.Markup(s.replace('\n', '<br>'))

    from app.routes import main
    from app.auth import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app 