import mysql.connector
import datetime
import re


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


class Database:
    def __init__(self):
        self.__database_config = {
            'user': Config['mysql']['username'],
            'password': Config['mysql']['password'],
            'host': Config['mysql']['url'],
            'port': Config['mysql']['port'],
            'database': Config['mysql']['database'],
            'raise_on_warnings': True,
            'connection_timeout': 5
        }

    # Database connection
    def connectToDatabase(self):
        # Connect to database
        connection_context = None
        try:
            connection_context = mysql.connector.connect(**self.__database_config)
            cursor = connection_context.cursor(dictionary=True)
        except Exception as e:
            print("Connect to database error:", e)
            exit(1)
        # On connect success return connection context and cursor
        return connection_context, cursor

    # Close database
    def disconnectToDatabase(self, connection_context):
        if connection_context != None:
            connection_context.close()

    def uploadData(self, data):
        data['UploadDate'] = datetime.datetime.now().isoformat()
        data['LastActionDate'] = data['UploadDate']
        data['Action'] = 'Upload'
        data['Status'] = 'Active'
        # Insert into data
        try:
            querty_string = "INSERT INTO {} ".format(Config['mysql']['table'])
            querty_string += "(FilePath, FileName, FileType, FileSize, Status, Action, UploadDate, LastActionDate) " \
                             "VALUES (%(FilePath)s, %(FileName)s, %(FileType)s, %(FileSize)s, %(Status)s, %(Action)s, %(UploadDate)s, " \
                             "%(LastActionDate)s)"
            connection_context, cursor = self.connectToDatabase()
            cursor.execute(querty_string, data)
            # Commit insert
            connection_context.commit()
            # Close connection to database
            self.disconnectToDatabase(connection_context)
            return True, 'Insert file success'
        except Exception as e:
            return False, "Insert file error: {}".format(e)

    def getData(self, filename=None):
        try:
            querty_string = 'SELECT * FROM {}'.format(Config['mysql']['table'])
            if filename:
                querty_string += ' WHERE FileName="{}"'.format(filename)
            connection_context, cursor = self.connectToDatabase()
            cursor.execute(querty_string)
            result = cursor.fetchall()
            # Close connection to database
            self.disconnectToDatabase(connection_context)
            return True, result
        except Exception as e:
            return False, "Select file error: {}".format(e)
