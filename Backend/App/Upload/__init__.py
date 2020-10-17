from flask import Blueprint, jsonify, request, send_file, send_from_directory
import datetime
import os
from werkzeug.utils import secure_filename
from Database import Database

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Define constant
CONFIG_FILE = 'Config.yaml'

# Load configuration
try:
    FileStream = open(CONFIG_FILE, "r")
    # Load configuration into config
    Config = load(FileStream, Loader=Loader)
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)


# Blueprint
app = Blueprint('upload', __name__)

# init database
database = Database()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config['allowed_extensions']


# Flask Module allow origin
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# @app.route('', methods=['GET'])
# def RootEndpoint():
#     return jsonify({'message': 'welcome to upload module'})


@app.route('', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file key'}), 404
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 404
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        upload_data = {}
        upload_data['FilePath'] = os.path.join(Config['upload_folder'], filename)
        upload_data['FileName'] = filename
        upload_data['FileType'] = file.content_type

        # Check file
        result_status, result_msg = database.getData(upload_data['FileName'])
        if not result_status:
            return jsonify({'error': result_msg}), 406
        if result_msg:
            return jsonify({'error': 'Duplicate file'}), 406

        # Save file
        file.save(os.path.join(Config['upload_folder'], upload_data['FileName']))

        with open(os.path.join(Config['upload_folder'], upload_data['FileName']), 'rb') as f:
            upload_data['FileSize'] = len(f.read())

        # Upload to database
        result_status, result_msg = database.uploadData(upload_data)
        if not result_status:
            return jsonify({'error': result_msg}), 406
        return jsonify({'msg': 'upload success'})
    return jsonify({'error': 'File type is unsupported'}), 406


@app.route('<string:filename>', methods=['GET'])
def get(filename):
    result_status, result_msg = database.getData(filename=filename)
    if not result_status:
        return jsonify({'error': result_msg}), 406
    return send_file(os.path.join(os.getcwd(), result_msg[0]['FilePath']))


@app.route('', methods=['PUT'])
def update():
    params = request.json

    old_filename = params['old_filename'].split('/')[-1]
    path = params['old_filename'].replace(old_filename, '')

    update_data = {}
    update_data['FileName'] = params['new_filename'].split('/')[-1]
    update_data['FilePath'] = f"{path}{update_data['FileName']}"
    update_data['ID'] = params['id']

    # Check there is file
    result_status, result_msg = database.getData(filename=old_filename)
    if not result_status:
        return jsonify({'error': result_msg}), 406
    if not result_msg:
        return jsonify({'error': 'File not found'}), 404

    # Rename file from storage
    os.rename(params['old_filename'], params['new_filename'])

    # Rename file from database
    result_status, result_msg = database.updateData(update_data)
    if not result_status:
        return jsonify({'error': result_msg}), 406

    return jsonify({'msg': 'rename file success'})