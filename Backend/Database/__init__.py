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
        # Insert into data
        try:
            querty_string = "INSERT INTO {} ".format(Config['mysql']['table'])
            querty_string += "(FilePath, FileThumbnailPath, FileName, FileType, FileSize, Action, UploadDate, LastActionDate) " \
                             "VALUES (%(FilePath)s, %(FileThumbnailPath)s, %(FileName)s, %(FileType)s, %(FileSize)s, %(Action)s, %(UploadDate)s, " \
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

    def getData(self, filename=None, filter=None):
        try:
            querty_string = 'SELECT * FROM {}'.format(Config['mysql']['table'])
            if filename:
                querty_string += ' WHERE FileName="{}"'.format(filename)
            elif filter is not None:
                querty_string += ' WHERE'
                querty_set = []
                if 'FileName' in filter:
                    if filter['FileName'] != '':
                        querty_set.append(" FileName LIKE '%{}%'".format(filter['FileName']))
                if 'FileType' in filter:
                    if filter['FileType'] != '':
                        querty_set.append(" FileType LIKE '%{}%'".format(filter['FileType']))
                if 'UploadDate' in filter:
                    if filter['UploadDate'] != '':
                        querty_set.append(" UploadDate BETWEEN '{0} 00:00:00' AND '{0} 23:59:59'".format(filter['UploadDate']))
                querty_string+= ' AND'.join(querty_set)

            connection_context, cursor = self.connectToDatabase()
            cursor.execute(querty_string)
            result = cursor.fetchall()
            # Close connection to database
            self.disconnectToDatabase(connection_context)
            return True, result
        except Exception as e:
            return False, "Select file error: {}".format(e)

    # rename
    def updateData(self, data):
        data['LastActionDate'] = datetime.datetime.now().isoformat()
        data['Action'] = 'Rename'

        check_data = self.getData(data['FileName'])
        if check_data:
            query_string = "UPDATE {} SET".format(Config['mysql']['table'])
            update_set = []
            for d in data:
                if type(data[d]) is str or type(data[d]) is bytes:
                    update_set.append(' %s="%s"' % (d, data[d]))
                elif type(data[d]) is int:
                    update_set.append(' %s=%d' % (d, data[d]))
                elif type(data[d]) is float:
                    update_set.append(' %s=%f' % (d, data[d]))
            query_string += ','.join(update_set)
            query_string += ' WHERE ID="%s"' % data['ID']
            try:
                connection_context, cursor = self.connectToDatabase()
                cursor.execute(query_string)
                connection_context.commit()
                self.disconnectToDatabase(connection_context)
                return True, 'Update filename success'
            except Exception as e:
                return False, e
        return False, 'Can\'t update filename'

    # remove
    def removeData(self, id):
        query_string = 'DELETE FROM {} WHERE ID="{}"'.format(Config['mysql']['table'], id)
        try:
            connection_context, cursor = self.connectToDatabase()
            cursor.execute(query_string)
            connection_context.commit()
            # Close connection to database
            self.disconnectToDatabase(connection_context)
            return True, 'Delete file in database success'
        except Exception as e:
            return False, 'Delete file in database error: {}'.format(e)
