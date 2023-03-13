import datetime
import uuid
from flask import request, jsonify, send_file
import os
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError 
from deeplearning import object_detection
from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename

from db import db
from models.item import ItemModel
from resources.item import ItemSubmission

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
    @jwt_required()
    def post(self):
        if 'image_name' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        upload_file = request.files['image_name']
        if upload_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(upload_file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        # process the file
        user_id = get_jwt_identity()
        now = datetime.datetime.utcnow().date()
        current_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        filename = secure_filename(f"{user_id}_{str(uuid.uuid4())}_{current_time}{os.path.splitext(upload_file.filename)[1]}")

        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)

        filename, text_list = object_detection(path_save, filename)
        predicted_path = os.path.join(PREDICT_PATH, filename)
        
        if text_list:
            item_submission = ItemSubmission()
            for text in text_list:
                item_data_sent = {"value": text,
                                  "image_name":filename}  # replace COLLECTION_ID with the appropriate collection ID
                item_submission.post(Item_data=item_data_sent)

        return send_file(predicted_path)


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


