#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file creates all the needed default configurations and external files needed for data persistence within the
    system. This module has all needed getters and setters for all three external files. If a file is already found on
    the computer being used, the system will load the data from that file into the system instead of the default
    values. More detailed information is available in section 3.2.4 in the SDD
REQUIREMENTS ADDRESSED:
    FR.14, NFR.5, LDR.1
LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 4
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from fileManager import FileManager

_default_log_values = ["   Date        Time     Command\n"]

_default_command_values = [
    "fist-palm-blink, None, None\n",
    "palm-fist-blink, None, None\n",
    "fist-blink-palm, None, None\n",
    "palm-blink-fist, None, None\n"
]

_default_configuration_values = ["0.05\n",
                                 "2\n",
                                 "5\n"
                                 ]

_configuration_index_map = {
        'open_eye_ratio' : 0,
        'minimum_time_increment' : 1,
        'maximum_time_increment' : 2
        }


def _get_configuration_index(configuration_column_name):
    return _configuration_index_map[configuration_column_name]


class DatabaseManager:
    def __init__(self):
        self.log_manager = FileManager("log.csv",
                                       _default_log_values)
        self.command_manager = FileManager("commands.csv",
                                           _default_command_values)
        self.configuration_manager = FileManager("configuration.csv",
                                                 _default_configuration_values)

    def set_gesture(self, gesture_name, now):
        self.log_manager.append_line(''.join((now.isoformat()[:10], "    ",
                                              now.isoformat()[12:19], "    ", gesture_name, " \n")))

    def set_gesture_sequence(self, gesture_sequence, now, was_recognised):
        if was_recognised:
            ending = "] recognised."
        else:
            ending = "] not recognised."

        self.log_manager.append_line(''.join((now.isoformat()[:10], "    ",
                                              now.isoformat()[12:19], "    ", "pattern: [",
                                              ", ".join(gesture_sequence), ending, " \n")))

    def set_gesture_sequence_link(self, device, device_linked, state, now):
        if device_linked:
            ending = " is now " + state + "."
        else:
            ending = " is not linked to the system. No state change will be observed."

        self.log_manager.append_line(''.join((now.isoformat()[:10], "    ",
                                              now.isoformat()[12:19], "    ", device, ending, " \n")))

    def set_gesture_sequence_error(self, output):
        self.log_manager.append_line(output)

    def get_gestures(self):
        return self.log_manager.get_lines()

    def set_command(self, gesture_sequence, command_text, device_name):
        commands = self.get_commands()
        is_registered = False
        line_index = 0

        for command in commands:
            if command["gesture_sequence"] == gesture_sequence:
                is_registered = True
                break
            else:
                line_index += 1

        gesture_sequence = '-'.join(gesture_sequence)
        line_contents = gesture_sequence + ', ' + command_text + ', ' + device_name + '\n'

        if is_registered:
            self.command_manager.set_line(line_index, line_contents)
        else:
            self.command_manager.append_line(line_contents)

    def get_commands(self):
        lines = self.command_manager.get_lines()
        commands = []
        for line in lines:
            line = line.split(', ')
            commands.append({
                "gesture_sequence": line[0].split('-'),
                "command_text": line[1],
                "device_name": line[2][:-1]
            })
        return commands

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
 
    def set_minimum_time_increment(self, new_minimum_time_increment):
        self.__set_configuration__('minimum_time_increment', new_minimum_time_increment)

    def get_minimum_time_increment(self):
        return float(self.__get_configuration__('minimum_time_increment'))

    def set_maximum_time_increment(self, new_maximum_time_increment):
        self.__set_configuration__('maximum_time_increment', new_maximum_time_increment)

    def get_maximum_time_increment(self):
        return float(self.__get_configuration__('maximum_time_increment'))
