from flask import Flask
from App.Upload import app as upload_module

app = Flask(__name__)
app.register_blueprint(upload_module, url_prefix='/upload')