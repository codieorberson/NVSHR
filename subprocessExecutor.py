#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre
DETAILED DESCRIPTION:
    This file creates an interface for the NVSHR system to execute subprocesses that have been created and also allows
    the system to clean those processes up.
REQUIREMENTS ADDRESSED:
    NFR.7, NFR.9
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

from subprocess import Popen


class SubprocessExecutor:
    def __init__(self):
        self.subprocesses = []

    def execute(self, file_name, argument):
        self.__clean_up_subprocesses__()
        self.subprocesses.append(Popen(['python3', file_name, argument]))

    def __clean_up_subprocesses__(self):
        running_subprocesses = []
        for subprocess in self.subprocesses:
            if subprocess.poll() is None:
                running_subprocesses.append(subprocess)
            else:
                subprocess.terminate()
        self.subprocesses = running_subprocesses
