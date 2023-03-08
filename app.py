from flask import Flask, request, jsonify, send_file
import os 
from deeplearning import object_detection

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
PREDICT_PATH = os.path.join(BASE_PATH,'static/predict/')

@app.route('/api/object_detection_text', methods=['POST'])
def detect_text():
    if 'image_name' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    upload_file = request.files['image_name']
    filename = upload_file.filename
    path_save = os.path.join(UPLOAD_PATH, filename)
    upload_file.save(path_save)
    
    filename2 ,text_list = object_detection(path_save, filename)
    
    return jsonify({'text_list': text_list})

@app.route('/api/object_detection_image', methods=['POST'])
def detect_image():
    if 'image_name' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    upload_file = request.files['image_name']
    filename = upload_file.filename
    path_save = os.path.join(UPLOAD_PATH, filename)
    upload_file.save(path_save)
    
    filename , text_list = object_detection(path_save, filename)
    predicted_path = os.path.join(PREDICT_PATH, filename)
    

    return send_file(predicted_path)


if __name__ == "__main__":
    app.run(debug=True)
