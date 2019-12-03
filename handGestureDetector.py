#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson
DETAILED DESCRIPTION:
    This file is used for the detection of hand gestures within the system. This module simply loads the needed haar
    cascades and then adds the detection processes to the process manager to check for fists and palms within the
    current frame. More detailed information is available in section 3.2.10 in the SDD
REQUIREMENTS ADDRESSED:
    FR.2, FR.3, FR.10, FR.14, NFR.2, NFR.8, NFR.6, EIR.1
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

from processManager import ProcessManager
from gesture import Gesture


class HandGestureDetector():
    def __init__(self):
        self.process_manager = ProcessManager()
        self.fist = Gesture("fist.xml")
        self.palm = Gesture("palm.xml")
        
    def detect(self, frame, flipped_frame, has_made_fist, has_made_palm):
        self.process_manager.add_process(
                self.fist.detect, (frame, flipped_frame, has_made_fist, 'fist'))
        self.process_manager.add_process(
                self.palm.detect, (frame, flipped_frame, has_made_palm, 'palm'))
        self.process_manager.on_done()

