from flask import  abort, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.collection import CollectionModel
from models.item import ItemModel
from schemas import ItemSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("Items" , "items", description="Operations on items")

@blp.route("/collections/items")
class ItemSubmission(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self , Item_data):
        Item = ItemModel(**Item_data)

        try:
            db.session.add(Item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred creating the Item.")
        
        return Item
    

    