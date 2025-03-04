from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import jinja2

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Adiciona o filtro nl2br
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return s
        return jinja2.utils.markupsafe.Markup(s.replace('\n', '<br>'))

    from app.routes import main
    app.register_blueprint(main)

    return app 