import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import pwd

import logging

#postgres will need the information in this map:
_database_configuration = {
        'database' : 'nvshr',
        'user' : pwd.getpwuid(os.getuid())[0], #<--This is the username of the
                                               #   user running main.py
        'password' : 'nvshr'
        }

_default_values = {
        'open_eye_ratio' : 0.2,
        'minimum_time_increment' : 2,
        'maximum_time_increment' : 5,
        #I never got the contrast settings to improve detection, so I don't
        #know if these next two values are reasonable defaults:
        'low_contrast' : 50,
        'high_contrast' : 100
        }

#These indexes correspond to the columns in theconfiguration table in postgres.
#The order of keys on these dicts is not gauranteed, but it doesn't matter for
#our purposes.
_default_value_indexes = {
        'open_eye_ratio' : 0,
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

        except Exception:
            print("Warning: NVSHR is not connected to a database and settings" +
                    " created in this session will not be saved.\n")
            self.is_connected = False

             #Uncomment this line if you want more details about why you 
             #failed to connect to postgres:
#            logging.exception("Failed database details:")

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

                VALUES (''' + 
                str(_default_values['open_eye_ratio']) + ", " + 
                str(_default_values['minimum_time_increment']) + ", " + 
                str(_default_values['maximum_time_increment']) + ", " + 
                str(_default_values['low_contrast']) +  ", " + 
                str(_default_values['high_contrast']) + 
                ");")

        cursor.execute('''CREATE TABLE log ( 
                id SERIAL,
                gesture_sequence STRING,
                timestamp INTEGER,
                was_recognised BOOLEAN
                )''')

        cursor.execute('''CREATE TABLE command_head ( 
                id SERIAL,
                link_id INTEGER
                )''')

        cursor.execute('''CREATE TABLE command_segment ( 
                id SERIAL,
                gesture STRING,
                link_id INTEGER,
                is_linked_to_tail BOOLEAN
                )''')

        cursor.execute('''CREATE TABLE command_tail ( 
                id SERIAL,
                device STRING,
                command STRING
                )''')

        cursor.close()
        connection.commit()

        return connection

    def __set_configuration__(self, configuration_column_name, value):
        if self.is_connected:  
            self.cursor.execute("UPDATE configuration SET "
                    +  configuration_column_name + " = " + str(value))
            self.cursor.close()
            self.connection.commit()
            self.cursor = self.connection.cursor()

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

    def set_open_eye_threshold(self, new_open_eye_ratio):
        self.__set_configuration__('open_eye_ratio', new_open_eye_ratio / 100)

    def get_open_eye_threshold(self):
        return  float(self.__get_configuration__('open_eye_ratio')) * 100

    def set_low_contrast(self, new_low_contrast):
        self.__set_configuration__('low_contrast', new_low_contrast)

    def get_low_contrast(self):
        return float(self.__get_configuration__('low_contrast'))
 
    def set_high_contrast(self, new_high_contrast):
        self.__set_configuration__('high_contrast', new_high_contrast)

    def get_high_contrast(self):
        return float(self.__get_configuration__('high_contrast'))
 
    def set_min_time_inc(self, new_min_time_inc):
        self.__set_configuration__('minimum_time_increment', new_min_time_inc)

    def get_min_time_inc(self):
        return float(self.__get_configuration__('minimum_time_increment'))
 
    def set_max_time_inc(self, new_max_time_inc):
        self.__set_configuration__('maximum_time_increment', new_max_time_inc)

    def get_max_time_inc(self):
        return float(self.__get_configuration__('maximum_time_increment'))
          
    def close(self):
        pass
