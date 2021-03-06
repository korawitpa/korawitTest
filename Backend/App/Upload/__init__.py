from flask import Blueprint, jsonify, request, send_file, send_from_directory
import datetime
import os
from werkzeug.utils import secure_filename
from Database import Database
from PIL import Image
import cv2

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


def video_to_frames(video_filename):
    """Extract frames from video"""
    cap = cv2.VideoCapture(video_filename)
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    frames = []
    if cap.isOpened() and video_length > 0:
        frame_ids = [0]
        if video_length >= 4:
            frame_ids = [0,
                         round(video_length * 0.25),
                         round(video_length * 0.5),
                         round(video_length * 0.75),
                         video_length - 1]
        count = 0
        success, image = cap.read()
        while success:
            if count in frame_ids:
                frames.append(image)
            success, image = cap.read()
            count += 1
    return frames


def image_to_thumbs(img):
    """Create thumbs from image"""
    height, width, channels = img.shape
    thumbs = {"original": img}
    sizes = [30]
    for size in sizes:
        if (width >= size):
            r = (size + 0.0) / width
            max_size = (size, int(height * r))
            thumbs[str(size)] = cv2.resize(img, max_size, interpolation=cv2.INTER_AREA)
    return thumbs

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
            upload_data['FileSize'] = len(f.read()) / 1024 /1024  # Convert to MB


        ### THUMBNAIL ###
        thumbnail_filename = upload_data['FileName'].split('.')[0] + '-thumbnail.png'
        if upload_data['FileType'] == "image/png" or upload_data['FileType'] == 'image/jpeg' or upload_data['FileType'] == 'image/jpg':

            image = Image.open(os.path.join(Config['upload_folder'], upload_data['FileName']))
            thumb = 30, 30
            thumbnail_image = image.copy()
            thumbnail_image.thumbnail(thumb, Image.LANCZOS)
            thumbnail_image.save(os.path.join(Config['upload_folder'], thumbnail_filename), optimize=True, quality=95)
        else:
            frames = video_to_frames(upload_data['FilePath'])[0]
            thumb = image_to_thumbs(frames)
            for k, v in thumb.items():
                cv2.imwrite(os.path.join(Config['upload_folder'], thumbnail_filename), v)
        upload_data['FileThumbnailPath'] = os.path.join(Config['upload_folder'], thumbnail_filename)

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
    if not result_msg:
        return jsonify({'error': 'File not found'}), 404

    return send_file(os.path.join(os.getcwd(), result_msg[0]['FilePath']))


# Get thumbnail
@app.route('<string:filename>/thumbnail', methods=['GET'])
def getThumbnail(filename):
    result_status, result_msg = database.getData(filename=filename)
    if not result_status:
        return jsonify({'error': result_msg}), 406
    if not result_msg:
        return jsonify({'error': 'File not found'}), 404
    return send_file(os.path.join(os.getcwd(), result_msg[0]['FileThumbnailPath']))


@app.route('', methods=['PUT'])
def update():
    params = request.json
    old_filename = params['old_filename'].split('/')[-1]
    directory = params['old_filename'].replace('/'+old_filename, '')

    update_data = {}
    update_data['FileName'] = params['new_filename'].split('/')[-1]
    update_data['FilePath'] = '{}\\\{}'.format(directory, update_data['FileName'])
    update_data['FileThumbnailPath'] = update_data['FilePath'].split('.')[0] + '-thumbnail.png'
    update_data['ID'] = params['id']

    # Check there is file
    result_status, result_msg = database.getData(filename=old_filename)
    if not result_status:
        return jsonify({'error': result_msg}), 406
    if not result_msg:
        return jsonify({'error': 'File not found'}), 404

    # Rename file from storage
    os.rename(params['old_filename'], params['new_filename'])
    # Rename file thumbnail from storage
    os.rename(params['old_filename'].split('.')[0]+'-thumbnail.png', params['new_filename'].split('.')[0]+'-thumbnail.png')

    # Rename file from database
    result_status, result_msg = database.updateData(update_data)
    if not result_status:
        return jsonify({'error': result_msg}), 406

    return jsonify({'msg': 'rename file success'})


@app.route('', methods=['DELETE'])
def remove():
    params = {}
    params['id'] = int(request.args.get('id'))
    params['file_path'] = request.args.get('file_path')
    params['file_thumbnail_path'] = request.args.get('file_thumbnail_path')

    temp_param = {}
    temp_param['file_path'] = params['file_path'].replace('\\', '/')
    temp_param['file_thumbnail_path'] = params['file_thumbnail_path'].replace('\\', '/')


    # Remove file from storage
    if os.path.exists(temp_param['file_path']):
        os.remove(temp_param['file_path'])
    if os.path.exists(temp_param['file_thumbnail_path']):
        os.remove(temp_param['file_thumbnail_path'])

    # Remove file from database
    result_status, result_msg = database.removeData(params['id'])
    if not result_status:
        return jsonify({'error': result_msg}), 406

    return jsonify({'msg': 'Remove file success'})


@app.route('database', methods=['GET'])
def getDatabase():
    params = {}
    params['FileName'] = request.args.get('filename')
    params['FileType'] = request.args.get('filetype')
    params['UploadDate'] = request.args.get('uploaddate')

    if params['FileName'] == '' and params['FileType'] == '' and params['UploadDate'] == '':
        params = None

    result_status, result_msg = database.getData(filter=params)
    if not result_status:
        return jsonify({'error': result_msg}), 406
    return jsonify({'msg': result_msg})