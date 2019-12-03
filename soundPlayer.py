#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre
DETAILED DESCRIPTION:
    This file creates an interface for the playing of the NVSHR confirm and failure sounds.
REQUIREMENTS ADDRESSED:
    FR.10, EIR.3
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

from subprocessExecutor import SubprocessExecutor
from playsound import playsound
from platform import system


class SoundPlayer:
    def __init__(self):
        self.subprocess_executor = SubprocessExecutor()
        self.is_linux = system() == 'Linux'

    def play_success_sound(self):
        self.__play_file__('Success.wav')

    def play_failure_sound(self):
        self.__play_file__('Failure.wav')

    def __play_file__(self, file_name):
        if self.is_linux:
            self.subprocess_executor.execute('./play_file.py', file_name)
        else:
            playsound(file_name, False)
