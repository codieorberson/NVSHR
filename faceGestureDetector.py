import cv2
from gesture import Gesture

class FaceGestureDetector():
    def __init__(self):
        self.has_made_left_wink = False
        self.has_made_right_wink = False

        self.left_wink_callback = None
        self.right_wink_callback = None

        self.face_cascade = cv2.CascadeClassifier('face.xml')
        self.eye_cascade = cv2.CascadeClassifier('eye.xml')

        self.eye = Gesture("eye.xml")

#        self.left_wink = Gesture("eye.xml")
#        self.right_wink = Gesture("eye.xml")
#        self.fist.set_debug_color((0, 0, 255))
#        self.palm.set_debug_color((0, 255, 255))

    def on_left_wink(self, callback):
        self.left_wink_callback = callback

    def on_right_wink(self, callback):
        self.right_wink_callback = callback

    def detect(self, frame, cap):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        center_pixel = cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2
        center_face = None

        for (x,y,w,h) in faces:
            center_offset = center_pixel - (x + (w / 2))
            if not center_face or abs(center_offset) - abs(center_face[4]) > 0:
                center_face = (x, y, w, h, center_offset)

        if center_face:
            x = center_face[0]
            y = center_face[1]
            w = center_face[2]
            h = center_face[3]
            center_of_face = x + (w / 2)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 1:
                if (x + eyes[0][0] + (eyes[0][2] / 2)) < center_of_face:
                    self.has_made_left_wink = True
                else:
                    self.has_made_right_wink = True

            for (ex,ey,ew,eh) in eyes:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
    def cycle(self):

        if self.has_made_left_wink and self.left_wink_callback:
            self.left_wink_callback()
            self.has_made_left_wink = False

        if self.has_made_right_wink and self.right_wink_callback:
            self.right_wink_callback()
            self.has_made_right_wink = False
