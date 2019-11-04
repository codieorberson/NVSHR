from fileManager import FileManager

_default_log_values = ["   Date        Time     Command\n"]

_default_command_values = []

_default_configuration_values = ["0.05\n",
        "2\n",
        "5\n",
        #I never got the contrast settings to improve detection, so I don't
        #know if these next two values are reasonable defaults:
        "50\n",
        "100\n"
        ]

_configuration_index_map = {
        'open_eye_ratio' : 0,
        'minimum_time_increment' : 1,
        'maximum_time_increment' : 2,
        'low_contrast' : 3,
        'high_contrast' : 4
        }

def _get_configuration_index(configuration_column_name):
      return _configuration_index_map[configuration_column_name]

class DatabaseManager():
    def __init__(self):
        self.log_manager = FileManager("log.csv", 
                _default_log_values)
        self.command_manager = FileManager("commands.csv", 
                _default_command_values)
        self.configuration_manager = FileManager("configuration.csv", 
                _default_configuration_values)

    def __set_configuration__(self, column_name, value):
        self.configuration_manager.set_line(
                _get_configuration_index(column_name), str(value) + "\n")

    def __get_configuration__(self, column_name):
        return self.configuration_manager.get_line(
                _get_configuration_index(column_name))

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






    # !!!!!!!!!Methods past this point are not actually implemented!!!!!!!!!!




    def add_command(self, gesture_sequence, device, command):
        if self.is_connected:
            pass
        else:
            pass

    def remove_command(self, geseture_sequence):
        if self.is_connected:
            pass
        else:
            pass

    def get_commands(self):
        if self.is_connected:
            pass
#            self.
        else:
            return self.commands
#        return []

    def add_log_message(self, gesture_sequence, was_recognised, timestamp):
        pass

    def get_log_messages(self):

        return []
