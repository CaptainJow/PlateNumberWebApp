from flask import request, jsonify, send_file
import os
from marshmallow import ValidationError 
from deeplearning import object_detection
from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename

from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.collection import CollectionModel
from models.item import ItemModel
from schemas import CollectionSchema, ItemSchema

blp = Blueprint("object_detection", __name__, description="Detecting images number plate")

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
PREDICT_PATH = os.path.join(BASE_PATH,'static/predict/')

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blp.route('/api/object_detection_text')
class ObjectDetectionText(MethodView):
    def post(self):
        if 'image_name' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        upload_file = request.files['image_name']
        if upload_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(upload_file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        # process the file
        filename = secure_filename(upload_file.filename)
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)

        filename2, text_list = object_detection(path_save, filename)

        return jsonify({'text_list': text_list})


@blp.route('/api/object_detection_image')
class ObjectDetectionImage(MethodView):
    def post(self):
        if 'image_name' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        upload_file = request.files['image_name']
        if upload_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(upload_file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)

        filename, text_list = object_detection(path_save, filename)
        predicted_path = os.path.join(PREDICT_PATH, filename)

        return send_file(predicted_path)



@blp.route('/collections', methods=['POST'])
def create_collection():
    collection_schema = CollectionSchema()
    try:
        collection = collection_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_collection = CollectionModel(name=collection['name'])

    db.session.add(new_collection)
    db.session.commit()

    serialized_collection = collection_schema.dump(new_collection)
    return jsonify(serialized_collection), 201


@blp.route('/collections', methods=['GET'])
def get_collections():
    collections = CollectionModel.query.all()
    collection_schema = CollectionSchema(many=True)
    return jsonify(collection_schema.dump(collections))



@blp.route('/collections/items', methods=['POST'])
def add_item_to_collection():
    item_schema = ItemSchema()
    try:
        item = item_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    collection_id = item.get('collection_id')
    collection = CollectionModel.query.get_or_404(collection_id)

    new_item = ItemModel(value=item['value'], collection_id=collection.id)

    try:
        db.session.add(new_item)
        db.session.commit()
    except SQLAlchemyError :
        return jsonify("An error occurred while inserting the item."), 500

    serialized_item = item_schema.dump(new_item)
    serialized_collection = CollectionSchema().dump(collection)
    serialized_collection['items'].append(serialized_item)
    
    return jsonify(serialized_item), 201
    

@blp.route('/collections/items', methods=['DELETE'])
def delete_item():
    try:
        item_id = request.json['id']
    except KeyError:
        return {'message': 'No item ID provided'}, 400

    query = ItemModel.query.filter_by(id=item_id)
    result = query.delete()

    if result > 0:
        db.session.commit()
        return {'message': 'Item deleted successfully'}, 200
    else:
        return {'message': 'Item not found'}, 404


