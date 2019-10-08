import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from gesture import Gesture
#I really don't like the following two module names, we should change them.
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector

class GestureDetector():
    def __init__(self):
        #Next value not being used right now, but may be in the near future.
        #self.is_black_and_white = False

        self.process_manager = ProcessManager()
        self.hand_gesture_detector = HandGestureDetector()
        self.blink_detector = BlinkDetector()

        self.fist_event = None
        self.palm_event = None
        self.blink_event = None

    def on_fist(self, callback):
        self.fist_event = callback

    def on_palm(self, callback):
        self.palm_event = callback

    def on_blink(self, callback):
        self.blink_event = callback

    #This method is expected to be run in a separate thread, which is why it
    #accepts MultithreadedPerimeter instances as arguments.
    def detect(self, frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):

        '''
        panel = np.zeros([100, 700], np.uint8)

        hContrastRed = 0
        lContrastRed = 170

        low_contrast = np.array([hContrastRed, hContrastGreen, hContrastBlue])
        high_contrast = np.array([lContrastRed, lContrastGreen, lContrastBlue])

        mask = cv2.inRange(frame, low_contrast, high_contrast)
        mask_inv = cv2.bitwise_not(mask)

        color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

        if self.is_black_and_white:
            current_frame = gray_frame
        else:
            current_frame = frame
        '''
        #The above code makes gesture detection worse for me right now, but may
        #be useful shortly. Codie's code at the bottom of this file might be
        #better, and it should certainly be in a separate method. The next line
        #just sets an alias for frame that will be convenient if we want to
        #detect gestures from a modified version while keeping the original.
        #At the moment renaming every instance of current_frame to frame
        #wouldn't have broken anything, but it used to, and it probably will
        #again once we start using that high-contrast/low-contrast code in a 
        #way that allows it to be adjusted for a particular environment with
        #particular lighting details.
        current_frame = frame
          
        #We're already in a child process, relative to main.py; now we're
        #spawning two grandchild processes (again relative to main.py).
        #Of these, the first (hand_gesture_detector.detect) will spin up
        #two more subprocesses, while blink_detector.detect will not --
        #which isn't to say that it shouldn't.
        self.process_manager.add_process(self.hand_gesture_detector.detect, 
                (current_frame, fist_perimeter, palm_perimeter))
        self.process_manager.add_process(self.blink_detector.detect, (current_frame, left_eye_perimeter, right_eye_perimeter))

        #Wait for children to yield control back to this process...
        self.process_manager.on_done()
        #...then yield control back to the parent process (main).

    #This method will be run synchronously, allowing the callbacks to have
    #access to the actual values of the parent process instead of just
    #operating on copies of them.
    def trigger_events(self, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter):

        if fist_perimeter.is_set():
            self.fist_event(timestamp)

        if palm_perimeter.is_set():
            self.palm_event(timestamp)

        #Repetitious, I know. This could be written in a more clever manner.
        
        if left_eye_perimeter.is_set() and right_eye_perimeter.is_set():
            if  open_eye_threshold > (left_eye_perimeter.get_ratio() + right_eye_perimeter.get_ratio() / 2):
                self.blink_event(timestamp)

#The methods beyond this point were things pulled from Codie's code that I
#didn't want to throw out entirely, but which seemed to generally impair
#my ability to detect frames. This wasn't always the case, it seems to depend
#highly on lighting. I think having this logic would be really useful once the
#high-contrast/low-contrast settings can be set by an admin looking at a debug
#screen. For the demo tomorrow, I think we'll have better luck without them.

    def set_frame_contrast(Red, Green, Blue):  # used for creating contrast within the frame to detect hand gestures
        # more clearly
        redContrast = Red
        greenContrast = Green
        blueContrast = Blue
        return [redContrast, greenContrast, blueContrast]

    def get_gray_hand_frame():
        low_contrast = np.array(GestureDetector.set_frame_contrast(0, 0, 0))
        high_contrast = np.array(
                GestureDetector.set_frame_contrast(132, 255, 255))

        return GestureDetector.changing_hand_frame(
                self, hand_frame, low_contrast, high_contrast)

    def changing_hand_frame(self, frame, low_cont, high_cont):
        mask = cv2.inRange(frame, low_cont, high_cont)
        mask_inv = cv2.bitwise_not(mask)
        color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def get_cropped_hand_frame():
       return imutils.resize(frame, width=800)

#Well, these two are for writing to the log file. I don't think this belongs in
#this class, or the class I have it in (more on that in a comment at the end of
#main.py), but I do think the code shoved in these methods may be better than
#the code I'm currently using.

    def get_gray_blink_frame(cropped_blink_frame):
       return cv2.cvtColor(cropped_blink_frame, cv2.COLOR_BGR2GRAY)

    def operate_on_file():
        #import os to use this method, wherever it goes.
        file_exists = os.path.exists("logfile.txt")
        if file_exists == False:
            self.file = open("logfile.txt", 'w+')
            self.file.write("   Date        Time     Command\n")
        else:
            self.file = open("logfile.txt", "a+")
        now = datetime.datetime.now()

        print("tick")  # used for debugging purposes

        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False
            fist_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                          12:19], "    ", "fist", " \n")
            fist_text = ''.join(fist_tuple)
            self.file.write(fist_text)

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False
            palm_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                          12:19], "    ", "palm", "\n")
            palm_text = ''.join(palm_tuple)
            self.file.write(palm_text)

        if self.has_made_blink and self.blink_callback:
            self.blink_callback()
            self.has_made_blink = False
            blink_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                12:19], "    ", "blink", "\n")
            blink_text = ''.join(blink_tuple)
            self.file.write(blink_text)

        self.file.close()

    def close_file():
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            self.file = open("logfile.txt", "w+")
            self.file.seek(0)
            self.file.truncate()
            self.file.close()
