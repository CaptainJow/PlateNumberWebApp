from flask import  abort, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models.collection import CollectionModel
from schemas import CollectionSchema


blp = Blueprint("collections" , "collections", description="Operations on collections")



# @blp.route('/collections')
class CollectionSubmission(MethodView):
    @blp.arguments(CollectionSchema)
    @blp.response(201, CollectionSchema)
    def post(self , collection_data ):
        collection = CollectionModel(**collection_data)
        try:
            db.session.add(collection)
            db.session.commit()
        except IntegrityError:
            abort(400, "A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, "An error occurred creating the store.")
        
        return collection
    
    @blp.response(200, CollectionSchema(many=True))
    def get(self):
        return CollectionModel.query.all()

