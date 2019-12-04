#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther, Justin Culbertson-Faegre, Danielle Bode, Evan Pollitt
DETAILED DESCRIPTION:
    This file is responsible for recognizing user inputted sequences as commands. All valid sequences are loaded into
    the gesture parser map on start up and related events are added into the events list. When the parser is sent a
    sequence (or sequences) from the lexer, the parser joins the list of gestures into one string and then checks to see
    if the full sequence or a portion of the sequence is housed within the system. Because the system is designed with
    disabled users in mind, the parser recognizes the first subset within the sequence to create an ease of use. More
    detailed information is available in section 3.2.6 in the SDD
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


class GestureParser:
    def __init__(self):
        self.gesture_pattern_map = {}
        self.gesture_sequence_events = []

    def add_pattern(self, gestures):
        self.gesture_pattern_map["-".join(gestures)] = True

    def on_gesture_sequence(self, event):
        self.gesture_sequence_events.append(event)

    def parse_pattern(self, gesture_sequence, now):
        joined_gesture_sequence = "-".join(gesture_sequence)
        was_recognised = joined_gesture_sequence in self.gesture_pattern_map

        if not was_recognised:
            for valid_gesture_sequence in self.gesture_pattern_map.keys():
                if valid_gesture_sequence in joined_gesture_sequence:
                    gesture_sequence = valid_gesture_sequence.split("-")
                    was_recognised = True
                    break

        for event in self.gesture_sequence_events:
            event(gesture_sequence, now, was_recognised)

    def parse_patterns(self, gesture_patterns, now):
        for gesture_pattern in gesture_patterns:
            self.parse_pattern(gesture_pattern, now)
