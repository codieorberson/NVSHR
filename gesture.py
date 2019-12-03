#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson
DETAILED DESCRIPTION:
    This file is responsible for adding the perimeters to the gestures being detected. This is also where the system
    checks a flipped frame from the camera in order to recognize gestures from the users left hand. This is also where
    the system loads in the haar cascades used to detect the hand gestures.
REQUIREMENTS ADDRESSED:
    FR.2, FR.3, FR.14, NFR.2, NFR.6
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


class Gesture:
    def __init__(self, haar_cascade_xml, 
            detection_check = lambda detected_gestures: len(detected_gestures) > 0, 
            debug_color = (0, 0, 255)):
        self.haar_cascade = cv2.CascadeClassifier(haar_cascade_xml)
        self.detection_check = detection_check
        self.debug_color = debug_color

    def set_debug_color(self, rgb_tuple):
        self.debug_color = rgb_tuple

    def set_detection_criteria(self, detection_check):
        self.detection_check = detection_check

    def detect(self, frame, flipped_frame, multithreaded_perimeter, hand_gesture):
        gesture = self.haar_cascade.detectMultiScale(frame, 1.3, 5)
        flipped_gesture = self.haar_cascade.detectMultiScale(flipped_frame, 1.3, 5)
        if self.detection_check(gesture):
            multithreaded_perimeter.set(gesture[0])
        elif self.detection_check(flipped_gesture):
            if hand_gesture == 'fist':
                flipped_gesture = self.detect_flipped_gesture(flipped_gesture, 550)
                multithreaded_perimeter.set(flipped_gesture[0])
            elif hand_gesture == 'palm':
                flipped_gesture = self.detect_flipped_gesture(flipped_gesture, 500)
                multithreaded_perimeter.set(flipped_gesture[0])

    def detect_flipped_gesture(self, flipped_gesture, size):
        flipped_gesture[0][0] = size - flipped_gesture[0][0]
        return flipped_gesture
