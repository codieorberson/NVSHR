import cv2
from timer import Timer
import numpy as np
import datetime

class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.has_made_fist = False
        self.has_made_palm = False
        #self.has_made_left_wink = False
        #self.has_made_right_wink = False
        self.fist_callback = None
        self.palm_callback = None
       #self.left_wink_callback = None
       #self.right_wink_callback = None

    def on_fist(self, callback):
        self.fist_callback = callback

    def on_palm(self, callback):
        self.palm_callback = callback

    #def on_left_wink(self, callback):
        #self.left_wink_callback = callback

    #def on_right_wink(self, callback):
        #self.right_wink_callback = callback

    def __on_tick__(self):
        #The next line is just for debugging, we need to remove it eventually.
        file=open("logfile.txt", 'a')
        now = datetime.datetime.now()
        print("tick")
        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False
            fist_tuple = (now.isoformat()[:10], "    ", now.isoformat()[12:19], "    ", "fist" ," \n")
            fist_text=''.join(fist_tuple)
            file.write(fist_text)
            

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False
            palm_tuple = (now.isoformat()[:10], "    ", now.isoformat()[12:19], "    ", "palm", "\n")
            palm_text=''.join(palm_tuple)
            file.write(palm_text)

        #if self.has_made_left_wink and self.left_wink_callback:
          #  self.left_wink_callback()
          #  self.has_made_left_wink = False

        #if self.has_made_right_wink and self.right_wink_callback:
         #  self.right_wink_callback()
          # self.has_made_right_wink = False
        file.close()
    def nothing():
        pass

    def start(self):
        timer = Timer(self.time_increment)
        timer.on_time(self.__on_tick__)

        cap = cv2.VideoCapture(0)

        #face_cascade = cv2.CascadeClassifier('face.xml')
        fist_cascade = cv2.CascadeClassifier('fist.xml')
        palm_cascade = cv2.CascadeClassifier('palm.xml')
        #eye_cascade = cv2.CascadeClassifier('eye.xml')

        
        panel = np.zeros([100, 700], np.uint8)


        hContrastRed = 0
        lContrastRed = 170

        hContrastGreen = 0
        lContrastGreen = 255

        hContrastBlue = 0
        lContrastBlue = 255


        while True:
            ret, frame = cap.read()


            low_contrast = np.array([hContrastRed, hContrastGreen, hContrastBlue])
            high_contrast = np.array([lContrastRed, lContrastGreen, lContrastBlue])

            mask = cv2.inRange(frame, low_contrast, high_contrast)
            mask_inv = cv2.bitwise_not(mask)

            color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
            gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        
            
            fists = fist_cascade.detectMultiScale(gray_frame, 1.3, 5)

            if len(fists) > 0:                
                self.has_made_fist = True

            for (x,y,w,h) in fists:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

            palms = palm_cascade.detectMultiScale(gray_frame, 1.3, 5)
            if len(palms) > 0:
                self.has_made_palm = True
            for (x,y,w,h) in palms:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

            #faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            #center_pixel = cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2
            #center_face = None

            #for (x,y,w,h) in faces:
             #   center_offset = center_pixel - (x + (w / 2))
               # if not center_face or abs(center_offset) - abs(center_face[4]) > 0:
                 #   center_face = (x, y, w, h, center_offset)

            timer.check_time()
            cv2.imshow('Frame', gray_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
