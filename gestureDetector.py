import cv2
from timer import Timer

class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.has_made_fist = False
        self.has_made_palm = False
        self.has_made_wink = False
        self.fist_callback = None
        self.palm_callback = None
        self.wink_callback = None

    def on_fist(self, callback):
        self.fist_callback = callback

    def on_palm(self, callback):
        self.palm_callback = callback

    def on_wink(self, callback):
        self.wink_callback = callback

    def __on_tick__(self):
        print("tick")

        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False

        if self.has_made_wink and self.wink_callback:
            self.wink_callback()
            self.has_made_wink = False

    def start(self):
        timer = Timer(self.time_increment)
        timer.on_time(self.__on_tick__)

        cap = cv2.VideoCapture(0)

        fist_cascade = cv2.CascadeClassifier('fist.xml')
        palm_cascade = cv2.CascadeClassifier('palm.xml')
        eye_cascade = cv2.CascadeClassifier('eye.xml')

        while(True):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fists = fist_cascade.detectMultiScale(gray, 1.3, 5)

            if len(fists) > 0:                
                self.has_made_fist = True

            for (x,y,w,h) in fists:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

            palms = palm_cascade.detectMultiScale(gray, 1.3, 5)
            if len(palms) > 0:
                self.has_made_palm = True
            for (x,y,w,h) in palms:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

            if len(eyes) == 1:
                self.has_made_wink = True

            for (x,y,w,h) in eyes:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            timer.check_time()
            cv2.imshow('insaneInTheFrame', cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

        cap.release()
        cv2.destroyAllWindows()
