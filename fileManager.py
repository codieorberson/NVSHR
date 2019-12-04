#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file is responsible for managing the the external files. This is used to open the external files, read from the
    external files, and write to the external files.
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

import os


class FileManager:
    def __init__(self, file_name, default_lines):
        self._file_name = file_name
        self._cached_lines = []
        if not os.path.exists(file_name):
            with open(self._file_name, "w+") as file:
                file.writelines(default_lines)
            self._cached_lines = default_lines
        else:
            with open(self._file_name) as file:
                self._cached_lines = file.readlines()

    def set_line(self, line_number, line_contents):
        with open(self._file_name, 'r') as file:
            lines = file.readlines()
            lines[line_number] = line_contents
        with open(self._file_name, 'w') as file:
            file.writelines(lines)
        self._cached_lines[line_number] = line_contents

    def append_line(self, line_contents):
        with open(self._file_name, "a") as file:
            file.write(line_contents)
        self._cached_lines.append(line_contents)

    def get_lines(self):
        return self._cached_lines

    def get_line(self, line_number):
        return self._cached_lines[line_number]

    def get_length(self):
        return len(self._cached_lines)
