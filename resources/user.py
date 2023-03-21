from flask import  jsonify
import os
from flask_jwt_extended import create_access_token, get_jwt, jwt_required,create_refresh_token,get_jwt_identity
from blocklist import BLOCKLIST 
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models.user import UserModel
from schemas import UserSchema ,LoginSchema
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

blp = Blueprint("Users" , "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data):
        email = user_data["email"].lower()

        try:
            user = UserModel(
                username = user_data["username"],
                email = email,
                password = pbkdf2_sha256.hash(user_data["password"])
            )
            db.session.add(user)
            db.session.commit()
            user.create_collection()

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id )

            return {
                    "message":"User created successfully" , 
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                    }
                } , 201

        except IntegrityError:
            db.session.rollback()
            return {"message": "A user with the same email address already exists"}, 409
        
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
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id )
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
            }
        
        return jsonify({"message":"Invalid Credentials"}) , 401


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        return {"access_token": new_token}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
