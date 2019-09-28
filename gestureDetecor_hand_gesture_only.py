import cv2
from timer import Timer
import numpy as np

class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.has_made_fist = False
        self.has_made_palm = False
        #self.has_made_left_wink = False
        #self.has_made_right_wink = False
        self.fist_callback = None
        self.palm_callback = None
       # self.left_wink_callback = None
       #self.right_wink_callback = None

    def on_fist(self, callback):
        self.fist_callback = callback

    def on_palm(self, callback):
        self.palm_callback = callback

    #def on_left_wink(self, callback):
        self.left_wink_callback = callback

    #def on_right_wink(self, callback):
        self.right_wink_callback = callback

    def __on_tick__(self):
        #The next line is just for debugging, we need to remove it eventually.
        print("tick")

        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False

        #if self.has_made_left_wink and self.left_wink_callback:
          #  self.left_wink_callback()
          #  self.has_made_left_wink = False

        #if self.has_made_right_wink and self.right_wink_callback:
         #   self.right_wink_callback()
          #  self.has_made_right_wink = False
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
        cv2.namedWindow('panel')

        cv2.createTrackbar('High Contrast Red', 'panel', 0, 255, self.nothing)
        cv2.createTrackbar('Low Contrast Red', 'panel', 132, 255, self.nothing) #This one we may have to change

        cv2.createTrackbar('High Contrast Green', 'panel', 0, 255, self.nothing)
        cv2.createTrackbar('Low Contrast Green', 'panel', 255, 255, self.nothing)

        cv2.createTrackbar('High Contrast Blue', 'panel', 0, 255, self.nothing)
        cv2.createTrackbar('Low Contrast Blue', 'panel', 255, 255, self.nothing)

        cv2.createTrackbar('North Rows', 'panel', 0, 480, self.nothing)
        cv2.createTrackbar('South Rows', 'panel', 480, 480, self.nothing)
        cv2.createTrackbar('Left Columns', 'panel', 0, 640, self.nothing)
        cv2.createTrackbar('Right Columns', 'panel', 640, 640, self.nothing)

        while True:
            ret, frame = cap.read()

            north_rows = cv2.getTrackbarPos('North Rows', 'panel')
            south_rows = cv2.getTrackbarPos('South Rows', 'panel')
            left_columns = cv2.getTrackbarPos('Left Columns', 'panel')
            right_columns = cv2.getTrackbarPos('Right Columns', 'panel')

            roi = frame[north_rows: south_rows, left_columns: right_columns]

            high_contrast_red = cv2.getTrackbarPos('High Contrast Red', 'panel')
            low_contrast_red = cv2.getTrackbarPos('Low Contrast Red', 'panel')
            high_contrast_green = cv2.getTrackbarPos('High Contrast Green', 'panel')
            low_contrast_green = cv2.getTrackbarPos('Low Contrast Green', 'panel')
            high_contrast_blue = cv2.getTrackbarPos('High Contrast Blue', 'panel')
            low_contrast_blue = cv2.getTrackbarPos('Low Contrast Blue', 'panel')

            low_contrast = np.array([high_contrast_red, high_contrast_green, high_contrast_blue])
            high_contrast = np.array([low_contrast_red, low_contrast_green, low_contrast_blue])

            mask = cv2.inRange(roi, low_contrast, high_contrast)
            mask_inv = cv2.bitwise_not(mask)

            color_frame = cv2.bitwise_and(roi, roi, mask=mask_inv)
            gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

            #cv2.imshow('Frame', gray_frame)

            #I tried commenting out the panel below, however it still displays when the program is ran
            #cv2.imshow('panel', panel)
            
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
            cv2.imshow('panel', panel)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
