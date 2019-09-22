import cv2
from timer import Timer
from gesture import Gesture
#I really don't like the following two module names, because I feel like they
#imply that they extend THIS module while the reverse is actually true.
from handGestureDetector import HandGestureDetector
from faceGestureDetector import FaceGestureDetector

class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.hand_gesture_detector = HandGestureDetector()
        self.face_gesture_detector = FaceGestureDetector()

    def on_fist(self, callback):
        self.hand_gesture_detector.on_fist(callback)

    def on_palm(self, callback):
        self.hand_gesture_detector.on_palm(callback)

    def on_left_wink(self, callback):
        self.face_gesture_detector.on_left_wink(callback)

    def on_right_wink(self, callback):
        self.face_gesture_detector.on_right_wink(callback)

    def __on_tick__(self):
        #The next line is just for debugging, we need to remove it eventually.
        print("tick")

        self.hand_gesture_detector.cycle()
        self.face_gesture_detector.cycle()

    def start(self):
        timer = Timer(self.time_increment)
        timer.on_time(self.__on_tick__)

        cap = cv2.VideoCapture(0)

        while(True):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.hand_gesture_detector.detect(frame)
            self.face_gesture_detector.detect(frame, gray, cap)

            timer.check_time()
            cv2.imshow('insaneInTheFrame', cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

        cap.release()
        cv2.destroyAllWindows()
