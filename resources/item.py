from flask import  abort, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.collection import CollectionModel
from models.item import ItemModel
from models.user import UserModel
from schemas import ItemSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

blp = Blueprint("Items" , "items", description="Operations on items")

@blp.route("/collections/items")
class ItemSubmission(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        page_size = request.args.get('page_size', type=int, default=10)
        page_index = request.args.get('page_index', type=int, default=1)
        user_id = get_jwt_identity()
        collection_id = UserModel.query.get(user_id).collection.id

        query = ItemModel.query.filter_by(collection_id=collection_id)\
                            .paginate(page=page_index, per_page=page_size)
        return query.items

    @jwt_required()
    # @blp.arguments(ItemSchema)
    # @blp.response(201, ItemSchema)
    def post(self , Item_data):
        user_id = get_jwt_identity()

        collection_id = UserModel.query.get(user_id).collection.id

        Item = ItemModel(value=Item_data["value"], collection_id=collection_id)

        try:
            db.session.add(Item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred creating the Item.")
        
        # return Item
    

    