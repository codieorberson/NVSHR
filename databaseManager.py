import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import pwd

#postgres will need the information in this map:
_database_configuration = {
        'database' : 'nvshr',
        'user' : pwd.getpwuid(os.getuid())[0], #<--This is the username of the
                                               #   user running main.py
        'password' : 'nvshr'
        }

_default_values = {
        'open_eye_threshold' : 0.2,
        'minimum_time_increment' : 2,
        'maximum_time_increment' : 5,
        'low_contrast' : None,
        'high_contrast' : None
        }

#These indexes correspond to the columns in theconfiguration table in postgres.
#The order of keys on these dicts is not gauranteed, but it doesn't matter for
#our purposes.
_default_value_indexes = {
        'open_eye_threshold' : 0,
        'minimum_time_increment' : 1,
        'maximum_time_increment' : 2,
        'low_contrast' : 3,
        'high_contrast' : 4
        }

class DatabaseManager():
    def __init__(self):
        #If table does not exist, default ear is 0.2
        try:
            self.connection = self.__get_connection__()
            self.cursor = self.connection.cursor()
            self.is_connected = True

        except:
            print("Warning: NVSHR is not connected to a database and settings" +
                    " created in this session will not be saved.\n")
            self.is_connected = False

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

        cursor.execute('''INSERT INTO configuration(
                open_eye_ratio, 
                minimum_time_increment, 
                maximum_time_increment,
                low_contrast, 
                high_contrast) 

                VALUES ('''
                + str(_default_values['open_eye_ratio']) + ", " +
                + str(_default_values['minimum_time_increment']) + ", " +
                + str(_default_values['maximum_time_increment']) + ", " +
                + str(_default_values['low_contrast']) + ", " +
                + str(_default_values['high_contrast']) +
                ");")

        cursor.close()
        connection.commit()

        return connection

    def __set_configuration__(self, configuration_column_name, value):
        if self.is_connected:
            #Not actual behavior, just a placeholder:
            _default_values[configuration_column_name] = value          

        else:
            _default_values[configuration_column_name] = value

    def __get_configuration__(self, configuration_column_name):
        if self.is_connected:
            self.cursor.execute("SELECT * FROM configuration")
            rows = self.cursor.fetchall()
            configuration = rows[0]

            return configuration[_default_value_indexes[configuration_column_name]]
        else: 
            return _default_values[configuration_column_name]

    def set_open_eye_threshold(self, new_open_eye_threshold):
        self.__set_configuration__('open_eye_threshold', new_open_eye_threshold)

    def get_open_eye_threshold(self):
        return float(self.__get_configuration__('open_eye_threshold'))
          
    def close(self):
        pass
