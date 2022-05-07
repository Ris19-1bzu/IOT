from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .database import db
from config import Config
import cv2

login = LoginManager()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    with app.test_request_context():
        db.create_all()

        import cvlock.front.controllers as panel

        app.register_blueprint(panel.module)

        return app