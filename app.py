import datetime
from flask import Flask, jsonify
from flask_smorest import Api
from resources.object_detection import blp as ObjectDetection
from resources.user import blp as User
from resources.collection import blp as collection
from resources.item import blp as Item
import models
from db import db
from blocklist import BLOCKLIST
import os
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "IMAGE WEB API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] =  db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)


    app.config["JWT_SECRET_KEY"]= 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]= datetime.timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"]= datetime.timedelta(days=30)

    migrate = Migrate(app , db)

    jwt = JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    api = Api(app)

    @app.before_first_request
    def create_tables():
            db.create_all()

    api.register_blueprint(ObjectDetection)
    api.register_blueprint(User)
    api.register_blueprint(collection)
    api.register_blueprint(Item)

    return app
