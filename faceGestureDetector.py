import cv2
from processManager import ProcessManager
from gesture import Gesture


class FaceGestureDetector():
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('face.xml')
        self.eye_cascade = cv2.CascadeClassifier('eye.xml')

    def __adjust_perimeter__(self, eye_position, face_position):
        return (face_position[0] + eye_position[0],
                face_position[1] + eye_position[1],
                eye_position[2],
                eye_position[3])

    def detect(self, frame, cap, face_perimeter,
               left_eye_perimeter, right_eye_perimeter):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        center_pixel = cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2
        center_face = None

        for (x, y, w, h) in faces:
            center_offset = center_pixel - (x + (w / 2))
            if not center_face or abs(center_offset) - abs(center_face[4]) > 0:
                center_face = (x, y, w, h, center_offset)

        if center_face:
            x = center_face[0]
            y = center_face[1]
            w = center_face[2]
            h = center_face[3]
            center_of_face = x + (w / 2)

            face_perimeter.set(center_face)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 1:
                if (x + eyes[0][0] + (eyes[0][2] / 2)) < center_of_face:
                    right_eye_perimeter.set(
                        self.__adjust_perimeter__(eyes[0], center_face))
                else:
                    left_eye_perimeter.set(
                        self.__adjust_perimeter__(eyes[0], center_face))

            elif len(eyes) > 1:
                left_eye_perimeter.set(
                    self.__adjust_perimeter__(eyes[0], center_face))
                right_eye_perimeter.set(
                    self.__adjust_perimeter__(eyes[1], center_face))
