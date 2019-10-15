from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2

class BlinkDetector:

    def __init__(self, ear_thresh = 0.2, ear_consec_frame = 2,ear= None, blinks = None, source=None ):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 
        self.source = source
        self.ear_thresh = ear_thresh
        self.ear_consec_frame = ear_consec_frame
        self.ear = ear
        self.blinks = blinks

    def detect(self, frame, left_eye_perimeter, right_eye_perimeter):
        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

            # loop over the face detections
        for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            x = int(leftEyeHull[3][0][0])
            width = int(leftEyeHull[0][0][0]) - x
            y = int((leftEyeHull[1][0][1] + leftEyeHull[2][0][1]) / 2)

            if len(leftEyeHull) > 5:
                height = y - int((leftEyeHull[4][0][1] + leftEyeHull[5][0][1]) / 2)
            else:
                height = 0
                
            y = y - height
            left_eye_perimeter.set((x, y, width, height))
                
            x = int(rightEyeHull[3][0][0])
            width = int(rightEyeHull[0][0][0]) - x
            y = int((rightEyeHull[1][0][1] + rightEyeHull[2][0][1]) / 2)

            if len(rightEyeHull) > 5:
                height = y - int((rightEyeHull[4][0][1] + rightEyeHull[5][0][1]) / 2)
            else:
                height = 0
 
            y = y - height
            right_eye_perimeter.set((x, y, width, height))
