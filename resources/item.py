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
import json

blp = Blueprint("Items" , "items", description="Operations on items")

@blp.route("/collections/items")
class ItemSubmission(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):

        user_id = get_jwt_identity()
        collection_id = UserModel.query.get(user_id).collection.id

        # Count the total number of items in the collection
        total_count = ItemModel.query.filter_by(collection_id=collection_id).count()

        page_size = request.args.get('page_size', type=int, default=10)
        page_index = request.args.get('page_index', type=int, default=1)

        # Get paginated items
        query = ItemModel.query.filter_by(collection_id=collection_id)\
                            .paginate(page=page_index, per_page=page_size)
        # Return a dictionary with the total count and paginated items
        items_data = []

        for item in query.items:
            items_data.append({
                "collection_id":collection_id,
                "id": item.id,
                "value":item.value,
                "created_at":item.created_at.strftime("%d-%m-%Y"),
                "image_name":item.image_name
            })

        

        data={
            "total_count": total_count,
            "data": items_data
            
        }
        return jsonify(data)

    @jwt_required()
    def post(self , Item_data):
        user_id = get_jwt_identity()

        collection_id = UserModel.query.get(user_id).collection.id

        Item = ItemModel(value=Item_data["value"], collection_id=collection_id,image_name=Item_data["image_name"])

        try:
            db.session.add(Item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred creating the Item.")
        
        # return Item
    

    