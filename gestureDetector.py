from inspect import signature
#^^^See comment in the .start method for an explanation of why this is here,
#   It shouldn't stay here long.

import cv2
import numpy as np
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gesture import Gesture
#I really don't like the following two module names, because I feel like they
#imply that they extend THIS module while the reverse is more-or-less true.
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector

class GestureDetector():
    def __init__(self, time_increment, is_black_and_white):
        self.time_increment = time_increment
        self.is_black_and_white = is_black_and_white

        self.process_manager = ProcessManager()
        self.hand_gesture_detector = HandGestureDetector()
        self.blink_detector = BlinkDetector()

        self.fist_event = None
        self.palm_event = None
        self.blink_event = None
        self.left_wink_event = None
        self.right_wink_event = None

    def on_fist(self, callback):
        self.fist_event = callback

    def on_palm(self, callback):
        self.palm_event = callback

    def on_blink(self, callback):
        self.blink_event = callback

    def on_left_wink(self, callback):
        self.left_wink_event = callback

    def on_right_wink(self, callback):
        self.right_wink_event = callback      

    def detect(self, frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):
#        cap = cv2.VideoCapture(0)
        panel = np.zeros([100, 700], np.uint8)

        hContrastRed = 0
        lContrastRed = 170

        hContrastGreen = 0
        lContrastGreen = 255

        hContrastBlue = 0
        lContrastBlue = 255

        low_contrast = np.array([hContrastRed, hContrastGreen, hContrastBlue])
        high_contrast = np.array([lContrastRed, lContrastGreen, lContrastBlue])

#        while(True):
#            ret, frame = cap.read()
#            timestamp = datetime.now()

        mask = cv2.inRange(frame, low_contrast, high_contrast)
        mask_inv = cv2.bitwise_not(mask)

        color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

        if self.is_black_and_white:
            current_frame = gray_frame
        else:
            current_frame = frame
          
        self.process_manager.add_process(self.hand_gesture_detector.detect, 
                (current_frame, fist_perimeter, palm_perimeter))
        self.process_manager.add_process(self.blink_detector.detect, (current_frame, left_eye_perimeter, right_eye_perimeter))

        self.process_manager.on_done()


    def trigger_events(self, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):
        is_left_eye_closed = False
        is_right_eye_closed = False

        if fist_perimeter.is_set():
                #There shouldn't be any actual scenario where this takes one 
                #argument, but since Landan is already working on testing the
                #GestureDetector interface I'm allowing this callback to continue
                #functioning with just one argument. When Landan commits his tests
                #I'll modify them and change this part of the code. This comment
                #applies to palm_perimeter as well.
            if len(signature(self.fist_event).parameters) == 1:
                self.fist_event(timestamp)
            else:
                self.fist_event()

        if palm_perimeter.is_set():
            if len(signature(self.palm_event).parameters) == 1:
                self.palm_event(timestamp)
            else:             
                self.palm_event()

        if left_eye_perimeter.is_set():

            if open_eye_threshold > left_eye_perimeter.get_ratio():
                is_left_eye_closed = True

        if right_eye_perimeter.is_set():

            if open_eye_threshold > right_eye_perimeter.get_ratio():
                is_right_eye_closed = True

        if is_right_eye_closed and is_left_eye_closed:
            if len(signature(self.blink_event).parameters) == 1:
                self.blink_event(timestamp)
            else:             
                self.blink_event()

        elif is_left_eye_closed:
            if len(signature(self.left_wink_event).parameters) == 1:
                self.left_wink_event(timestamp)
            else:             
                self.left_wink_event()

        elif is_right_eye_closed:
            if len(signature(self.right_wink_event).parameters) == 1:
                self.right_wink_event(timestamp)
            else:             
                self.right_wink_event()
