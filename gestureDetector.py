import cv2
from timerClass import Timer


class GestureDetector():
    def __init__(self, time_increment):
        self.time_increment = time_increment
        self.timer = Timer(self.time_increment)
        self.has_made_fist = False
        self.has_made_palm = False
        self.has_made_left_wink = False
        self.has_made_right_wink = False
        self.fist_callback = None
        self.palm_callback = None
        self.left_wink_callback = None
        self.right_wink_callback = None

    def on_fist(self, callback):
        self.fist_callback = callback

    def on_palm(self, callback):
        self.palm_callback = callback

    def on_left_wink(self, callback):
        self.left_wink_callback = callback

    def on_right_wink(self, callback):
        self.right_wink_callback = callback

    def on_tick(self):
        #The next line is just for debugging, we need to remove it eventually.
        print("tick")

        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False

        if self.has_made_left_wink and self.left_wink_callback:
            self.left_wink_callback()
            self.has_made_left_wink = False

        if self.has_made_right_wink and self.right_wink_callback:
            self.right_wink_callback()
            self.has_made_right_wink = False

    def start(self):
        self.timer.on_time(self.on_tick)

        cap = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier('face.xml')
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

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
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
                eyes = eye_cascade.detectMultiScale(roi_gray)

                if len(eyes) == 1:
                    if (x + eyes[0][0] + (eyes[0][2] / 2)) < center_of_face:
                        self.has_made_left_wink = True
                    else:
                        self.has_made_right_wink = True

                for (ex,ey,ew,eh) in eyes:
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            self.timer.check_time()
            cv2.imshow('insaneInTheFrame', cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

        cap.release()
        cv2.destroyAllWindows()
