from fileManager import FileManager

_default_log_values = ["   Date        Time     Command\n"]

_default_command_values = [
    "fist-palm-blink, 192.168.1.197, Smart Plug\n",
    "palm-fist-blink, 192.168.1.198, Smart Plug\n",
    "fist-blink-palm, Heat on/off, Alexa\n",
    "palm-blink-fist, AC on/off, Alexa\n",
    "palm, STOP, Alexa\n"
]

_default_configuration_values = [
        "0.05\n",
        "2\n",
        "5\n",
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
        self.log_manager = FileManager("log.csv", _default_log_values)
        self.command_manager = FileManager("commands.csv", 
                _default_command_values)
        self.configuration_manager = FileManager("configuration.csv",
                _default_configuration_values)

    def set_gesture(self, gesture_name, now):
        self.log_manager.append_line(''.join((now.isoformat()[:10], "    ",
                                              now.isoformat()[12:19], "    ", gesture_name, " \n")))

    def get_gestures(self):
        return self.log_manager.get_lines()

    def set_command(self, gesture_sequence, command_text, device_name):
        line_index = self.__get_line_index__(gesture_sequence)
        gesture_sequence = '-'.join(gesture_sequence)
        command_text = self.__stash_commas__(command_text)
        line_contents = gesture_sequence + ', ' + command_text + ', ' + device_name + '\n'

        if line_index == None:
            self.command_manager.append_line(line_contents)
        else:
            self.command_manager.set_line(line_index, line_contents)

    def get_commands(self):
        lines = self.command_manager.get_lines()
        commands = []
        for line in lines:
            line = line.split(', ')
            commands.append({
                "gesture_sequence": line[0].split('-'),
                "command_text": self.__restore_commas__(line[1]),
                "device_name": line[2][:-1]
            })
        return commands

    def __get_line_index__(self, gesture_sequence):
        commands = self.get_commands()
        line_index = 0

        for command in commands:
            if command["gesture_sequence"] == gesture_sequence:
                return line_index
            else:
                line_index += 1

    def __stash_commas__(self, command_text):
        return command_text.replace(",", "☢")

    def __restore_commas__(self, command_text):
        return command_text.replace("☢", ",")

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

    def close(self):
        self.log_manager.close()
        self.command_manager.close()
        self.configuration_manager.close() 
