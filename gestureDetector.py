from inspect import signature
#^^^See comment in the .start method for an explanation of why this is here,
#   It shouldn't stay here long.

import cv2
from time import time
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gesture import Gesture
#I really don't like the following two module names, because I feel like they
#imply that they extend THIS module while the reverse is more-or-less true.
from handGestureDetector import HandGestureDetector
from faceGestureDetector import FaceGestureDetector


class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.process_manager = ProcessManager()
        self.hand_gesture_detector = HandGestureDetector()
        self.face_gesture_detector = FaceGestureDetector()

    def on_fist(self, callback):
        self.fist_event = callback

    def on_palm(self, callback):
        self.palm_event = callback

    def on_left_wink(self, callback):
        self.left_wink_event = callback

    def on_right_wink(self, callback):
        self.right_wink_event = callback

    def start(self):
        cap = cv2.VideoCapture(0)

        while(True):
            ret, frame = cap.read()
            timestamp = time()

            fist_perimeter = MultithreadedPerimeter()
            palm_perimeter = MultithreadedPerimeter()
            face_perimeter = MultithreadedPerimeter()
            left_eye_perimeter = MultithreadedPerimeter()
            right_eye_perimeter = MultithreadedPerimeter()
            
            self.process_manager.add_process(self.hand_gesture_detector.detect, 
                    (frame, fist_perimeter, palm_perimeter))
            self.process_manager.add_process(self.face_gesture_detector.detect, 
                    (frame, cap, face_perimeter, left_eye_perimeter, right_eye_perimeter))
            self.process_manager.on_done()

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

                cv2.rectangle(frame, fist_perimeter.get_top_corner(),
                        fist_perimeter.get_bottom_corner(), (255, 0, 0), 2)

            if palm_perimeter.is_set():
                if len(signature(self.palm_event).parameters) == 1:
                    self.palm_event(timestamp)
                else:             
                    self.palm_event()

                cv2.rectangle(frame, palm_perimeter.get_top_corner(), 
                        palm_perimeter.get_bottom_corner(), (0, 0, 255), 2)             

            if face_perimeter.is_set():
                cv2.rectangle(frame, face_perimeter.get_top_corner(), 
                        face_perimeter.get_bottom_corner(), (255, 255, 255), 2)

                if left_eye_perimeter.is_set():
                     cv2.rectangle(frame, left_eye_perimeter.get_top_corner(), 
                             left_eye_perimeter.get_bottom_corner(), (0, 255, 0), 2)
                     if not right_eye_perimeter.is_set():
                         if len(signature(self.left_wink_event).parameters) == 1:
                             self.left_wink_event(timestamp)
                         else:             
                             self.left_wink_event()

                if right_eye_perimeter.is_set():
                    cv2.rectangle(frame, right_eye_perimeter.get_top_corner(), 
                            right_eye_perimeter.get_bottom_corner(), (0, 255, 0), 2)
                    if not left_eye_perimeter.is_set():
                        if len(signature(self.right_wink_event).parameters) == 1:
                            self.right_wink_event(timestamp)
                        else:             
                            self.right_wink_event()

            cv2.imshow('NVSHR', cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

        cap.release()
        cv2.destroyAllWindows()
