from flask import Flask
from App.Upload import app as upload_module

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


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config['file_size'] * 1024 * 1024  # Mb unit

app.register_blueprint(upload_module, url_prefix='/upload')
