#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file is responsible for logging the detected gestures and gesture sequences onto the console. The logger also
    logs information to the console on whether or not a smart home device was actually contacted by the system. More
    detailed information is available in section 3.2.5 in the SDD
REQUIREMENTS ADDRESSED:
    FR.10, LDR.1
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


class Logger:
    def __init__(self):
        self.output = ""
        exists = os.path.exists("logfile.txt")
        if not exists:
            self.file = open("logfile.txt", 'w+')
            self.file.write("   Date        Time     Command\n")
            print("   Date        Time     Command\n")
        else:
            self.file = open("logfile.txt", "a+")
            
    def log(self, output):
        self.__init__()
        self.output = output
        self.file.write(output)
        print(output) 
    
    def get_output(self):
        return self.output

    def log_gesture(self, gesture_name, now):
        self.log(''.join((now.isoformat()[:10], "    ", now.isoformat()[12:19], 
                "    ", gesture_name ," \n")))

    def log_gesture_sequence(self, gesture_sequence, now, was_recognised):
        if was_recognised:
            ending = "] recognised"
        else:
            ending = "] not recognised"

        self.log_gesture("pattern: [" + ', '.join(gesture_sequence) + ending, now)

    def log_device_state_change(self, device, device_linked, state, now):
        if device_linked:
            ending = " is now " + state + "."
        else:
            ending = " is not linked to the system. No state change will be observed."

        self.log_gesture(device + ending, now)

    def get_output(self):
        return self.output

    def close(self):
        self.file.seek(0)
        self.file.close()
        os.remove("logfile.txt")
