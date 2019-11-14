import cv2
import dlib
from imutils import face_utils


class BlinkDetector:

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('./static_data/eye.dat')

    def detect(self, frame, left_eye_perimeter, right_eye_perimeter):
        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (left_eye_start, left_eye_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (right_eye_start, right_eye_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscala0dwe frame
        faces = self.detector(gray, 0)
        try:
            # loop over the face detections
            for face in faces:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, face)
                shape = face_utils.shape_to_np(shape)
                
                self.__set_eye__(left_eye_perimeter, shape[left_eye_start:left_eye_end])
                self.__set_eye__(right_eye_perimeter, shape[right_eye_start:right_eye_end])

        except:
            # Sometimes we're getting out of range errors when trying to access
            # the six points on the eyes, particularly when they move off
            # screen. This should make our program not barf when that happens.
            left_eye_perimeter.set((0, 0, 0, 0))
            right_eye_perimeter.set((0, 0, 0, 0))

    def __set_eye__(self, perimeter, eye_shape):
        eye_hull = cv2.convexHull(eye_shape)

        x = int(eye_hull[3][0][0])
        width = int(eye_hull[0][0][0]) - x
        y = int((eye_hull[1][0][1] + eye_hull[2][0][1]) / 2)

        if len(eye_hull) > 5:
            height = y - int((eye_hull[4][0][1] + eye_hull[5][0][1]) / 2)
        else:
            height = 0

        y = y - height
        perimeter.set((x, y, width, height))
