from App import app

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


# Open flask application
try:
    app.run(debug=Config['debug'], port=Config['port'], host=Config['host'])
except Exception as e:
    print("Cannot start Flask service daemon:", e)
    exit(1)