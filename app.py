from flask import Flask
from flask_smorest import Api
from resources.object_detection import blp as ObjectDetection
from resources.user import blp as User
import models
from db import db
import os
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "IMAGE WEB API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)


    app.config["JWT_SECRET_KEY"]= 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
    jwt = JWTManager(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
            db.create_all()

    api.register_blueprint(ObjectDetection)
    api.register_blueprint(User)

    return app
