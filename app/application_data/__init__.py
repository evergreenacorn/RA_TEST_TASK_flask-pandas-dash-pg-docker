from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask import Flask
from dash import Dash


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_server(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    return app

def create_app_from_server(server, stylesheets, config_class=Config):
    return Dash(__name__, server = server, url_base_pathname='/dashboard/', external_stylesheets=stylesheets)
