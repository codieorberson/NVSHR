#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson
DETAILED DESCRIPTION:
    This file creates and regulates the processes of the system. If the system is on Linux, the multiprocessing is used.
    If the system is on any other operating system, it will use synchronous processes to complete actions. More detailed
    information is available in section 3.2.11 in the SDD
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

import multiprocessing
from multiprocessing import Process
import platform


class SynchronousProcess:
    def __init__(self, target=None, args=None):
        if args:
            target(*args)
        else:
            target()

    def start(self):
        pass

    def join(self):
        pass


if platform.system() == 'Linux':
    # On Linux, we use multiprocessing.
    ProcessConstructor = Process
else:
    # On Windows, we use the previously defined kludge.
    ProcessConstructor = SynchronousProcess


class ProcessManager:
    def __init__(self):
        self.processes = []

    def add_process(self, callback, arguments=None):
        if arguments:
            if not isinstance(arguments, tuple):
                arguments = (arguments, )
            self.process = ProcessConstructor(target=callback, args=arguments)
        else:
            self.process = ProcessConstructor(target=callback)
            
        self.processes.append(self.process)
        self.process.start()

    def on_done(self, callback=None):
        for self.process in self.processes:
            self.process.join()
        self.processes = []
        if callback:
            callback()
