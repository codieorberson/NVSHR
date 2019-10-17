import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import pwd

#postgres will need the information in this map:
_database_configuration = {
        'database' : 'nvshr',
        'user' : pwd.getpwuid(os.getuid())[0], 
        'password' : 'nvshr'
        }

_default_values = {
        'open_eye_ratio' : 0.2,
        'minimum_time_increment' : 2,
        'maximum_time_increment' : 5,
        'low_contrast' : None,
        'high_contrast' : None
        }

class DatabaseManager():
    def __init__(self):
        #If table does not exist, default ear is 0.2
        self.connection = self.__get_connection__()
        self.cursor = self.connection.cursor()
    
    def __get_connection__(self):
        connection = psycopg2.connect(
                user = _database_configuration['user'],
                password = _database_configuration['password'])

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        if not self.__is_initialised__(cursor):
            connection = self.__initialise__(cursor, connection)
        else:
            connection = psycopg2.connect(
                    database = _database_configuration['database'],
                    user = _database_configuration['user'],
                    password = _database_configuration['password'])

        return connection

    def __is_initialised__(self, cursor):
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '"
                + _database_configuration['database'] +"'")
        return cursor.fetchone()

    def __initialise__(self, cursor, connection):
        cursor.execute('CREATE DATABASE ' + _database_configuration['database'])

        cursor.close()
        connection.commit()

        connection = psycopg2.connect(
                database = _database_configuration['database'],
                user = _database_configuration['user'],
                password = _database_configuration['password'])

        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE configuration ( 
                open_eye_ratio FLOAT,
                minimum_time_increment INTEGER,
                maximum_time_increment INTEGER,
                low_contrast INTEGER,
                high_contrast INTEGER
                )''')

        cursor.execute('''INSERT INTO configuration(open_eye_ratio) VALUES ('''
                + str(_default_values['open_eye_ratio']) + 
                ''');''')

        cursor.close()
        connection.commit()

        return connection

#        'open_eye_ratio' : 0.2,
#        'minimum_time_increment' : 2,
#        'maximum_time_increment' : 5,
#        'low_contrast' : None,
#        'high_contrast' : None

    def __set_configuration__(configuration_column_name, value):
        pass

    def set_open_eye_threshold(self, new_open_eye_threshold):
        self.__set_configuration__('open_eye_threshold', new_open_eye_value)

    def get_open_eye_threshold(self):
        pass
          
    def close(self):
        pass
