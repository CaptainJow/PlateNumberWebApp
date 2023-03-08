from flask import Flask, request, jsonify
import os 
from deeplearning import object_detection

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')

@app.route('/api/object_detection', methods=['POST'])
def detect_text():
    if 'image_name' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    upload_file = request.files['image_name']
    filename = upload_file.filename
    path_save = os.path.join(UPLOAD_PATH, filename)
    upload_file.save(path_save)
    
    text_list = object_detection(path_save, filename)
    os.remove(path_save)
    
    return jsonify({'text_list': text_list})

if __name__ == "__main__":
    app.run(debug=True)
