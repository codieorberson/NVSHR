#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file creates an interface for combining the detection of eye blinks and hand gestures. It starts by creating
    instances of the needed subcomponents and then sets up the system to begin drawing the red rectangles within the
    debug tab. Once everything is set up correctly, the system can then begin calling the detect method to reset the
    perimeters for the rectangles, detect the various gestures (including the left hand) and eye blinks, and triggering
    the linked events for those gestures. Once it recognizes a gesture, it begins to draw the rectangles that are shown
    in the debug tab. More detailed information is available in section 3.2.2 in the SDD
REQUIREMENTS ADDRESSED:
    FR.1, FR.2, FR.3, FR.8, FR.14, NFR.2, NFR.5, NFR.6, EIR.1, OR.1
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

import cv2
import imutils
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gesture import Gesture
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector


class GestureDetector:
    def __init__(self):
        self.__set_up_helpers__()
        self.__set_up_perimeters__()
        self.gesture_events = []
        self.gesture_detected = None

    def on_gesture(self, callback):
        self.gesture_events.append(callback)

    def get_gesture_detected(self):
        return self.gesture_detected

    # Method is to be run in separate thread
    def detect(self, frame, timestamp, open_eye_threshold):
        self.__reset_perimeters__()
        self.__detect_shapes__(frame)
        self.__trigger_events__(timestamp, open_eye_threshold)
        return self.__draw_rectangles__(frame)

    def __detect_shapes__(self, frame):
        self.process_manager.add_process(
                self.hand_gesture_detector.detect, (frame, self.flip_frame(frame), self.fist_perimeter, self.palm_perimeter))

        self.blink_detector.detect(frame, self.left_eye_perimeter, self.right_eye_perimeter)
  
        self.process_manager.on_done()

    def __trigger_events__(self, timestamp, open_eye_threshold):
        self.gesture_detected = None

        self.__trigger_hand_events__(self.fist_perimeter, 'fist', timestamp)
        self.__trigger_hand_events__(self.palm_perimeter, 'palm', timestamp)
        self.__trigger_blink_events__(timestamp, open_eye_threshold)

    def __trigger_hand_events__(self, perimeter, gesture_name, timestamp):
        if perimeter.is_set():
            self.gesture_detected = gesture_name
            for event in self.gesture_events:
                event(gesture_name, timestamp)

    def __trigger_blink_events__(self, timestamp, open_eye_threshold):
        if self.left_eye_perimeter.is_set() and self.right_eye_perimeter.is_set():
            if open_eye_threshold / 100 > (
                    self.left_eye_perimeter.get_ratio() + self.right_eye_perimeter.get_ratio()) / 2:
                self.gesture_detected = "blink"

                for event in self.gesture_events:
                    event('blink', timestamp)

    def __draw_rectangles__(self, frame):
        for perimeter in self.perimeters:
            if perimeter.is_set():
                cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)

        return frame

    def __reset_perimeters__(self):
        for perimeter in self.perimeters:
            perimeter.set((0, 0, 0, 0))

    def __set_up_helpers__(self):
        self.process_manager = ProcessManager()
        self.hand_gesture_detector = HandGestureDetector()
        self.blink_detector = BlinkDetector()

    def __set_up_perimeters__(self):
        self.fist_perimeter = MultithreadedPerimeter()
        self.palm_perimeter = MultithreadedPerimeter()
        self.left_eye_perimeter = MultithreadedPerimeter()
        self.right_eye_perimeter = MultithreadedPerimeter()

        self.perimeters = [
            self.fist_perimeter,
            self.palm_perimeter,
            self.left_eye_perimeter,
            self.right_eye_perimeter
        ]

    def flip_frame(self, frame):
        frame = cv2.flip(frame, flipCode=1)
        return frame
