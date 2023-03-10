from flask import request, jsonify, send_file
import os
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError 
from deeplearning import object_detection
from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename
import re
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.user import UserModel
from models.item import ItemModel
from schemas import CollectionSchema, ItemSchema ,UserSchema ,LoginSchema
from passlib.hash import pbkdf2_sha256


blp = Blueprint("Users" , "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            return jsonify("a User with the same Email address already Exists"), 409

        # Validate email format
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(email_regex, user_data["email"]):
            return jsonify("Invalid email format."), 400

        user = UserModel(
            username = user_data["username"],
            email = user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message":"User created successfuly "} , 201
        
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.id)
            return{"access_token" : access_token , "data": jsonify(user)}
        
        return jsonify({"message":"Invalid Credentials"}) , 401
