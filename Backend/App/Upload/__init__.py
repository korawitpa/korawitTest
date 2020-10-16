from flask import Blueprint, jsonify, request
import datetime

# Blueprint
app = Blueprint('upload', __name__)

# # init database
# database = Database.Database(Config['mysql']['database'])

sym_warning = u'🚸'
sym_correct = u'✅'


# Flask Module allow origin
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('', methods=['GET'])
def RootEndpoint():
    return jsonify({'message': 'welcome to upload module'})