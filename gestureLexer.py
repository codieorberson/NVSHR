#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Evan Pollitt
DETAILED DESCRIPTION:
    This file creates the user inputted gesture sequence the system will compare to already configured commands. To
    begin, all gestures are added to the gestures list, which will then be lexed over to combine multiple gestures and
    ensure the gesture sequence sent to the parser is more readable and easier to compare to system commands.
    If a gesture falls within the minimum time increment (set by the administrator) from the time of the first
    recognized instance of that gesture, it will not be added into the gesture sequence. This module is also
    responsible for checking the maximum time increment for a gesture sequence to be complete and sends the current
    gesture sequence to the parser if it is above that time increment. More detailed information is
    available in section 3.2.7 in the SDD
REQUIREMENTS ADDRESSED:
    FR.3, FR.10, FR.14, NFR.7, NFR.2, NFR.6
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


class GestureLexer:
    def __init__(self):
        self.gestures = []
        self.gesture_patterns = []

    def add(self, gesture_name, now):
        self.gestures.append((gesture_name, now.timestamp()))

    # Iterates over list of gestures in proper order. If a timestamp is less than current time - set max increment,
    # that gesture sequence is added to list of all sequences.
    def lex(self, now, min_increment, max_increment):
        last_dict = {'fist' : None, 'palm' : None, 'blink' : None, 'left_wink' : None, 'right_wink' : None}

        now = now.timestamp()
        gesture_pattern = []
        for gesture in self.gestures:
            if not last_dict[gesture[0]]:
                last_dict[gesture[0]] = gesture[1]
                gesture_pattern.append(gesture[0])
            elif last_dict[gesture[0]] + min_increment < gesture[1]:
                last_dict[gesture[0]] = gesture[1]
                gesture_pattern.append(gesture[0])

        if len(self.gestures) > 0:
            if float(now) > max_increment + self.gestures[len(self.gestures) - 1][1]:
                if gesture_pattern != []:
                    self.gesture_patterns.append(gesture_pattern)
                    self.gestures = []

        current_patterns = self.gesture_patterns
        self.gesture_patterns = []

        return current_patterns
