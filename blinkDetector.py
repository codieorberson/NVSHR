#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther, Justin Culbertson-Faegre, Danielle Bode, Yutang Li
DETAILED DESCRIPTION:
    This file is responsible for detecting eye blinks. This file loads the eye.dat file used for facial recognition into
    the system. This file also calculates the eye aspect ratio used to set the sensitivity for detecting eye blinks.
    This file is also responsible for setting the perimeters for the rectangles on the eyes within the Debug tab. More
    detailed information is available in section 3.2.9 in the SDD
REQUIREMENTS ADDRESSED:
    FR.1, FR.3, FR.8, FR.14, NFR.2, NFR.8, NFR.6, OR.1
LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 4
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import cv2
import dlib
from imutils import face_utils


class BlinkDetector:

    def __init__(self, ear_thresh=0.2, ear_consec_frame=2, ear=None):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('eye.dat')
        self.ear_thresh = ear_thresh
        self.ear_consec_frame = ear_consec_frame
        self.ear = ear

    def detect(self, frame, left_eye_perimeter, right_eye_perimeter):
        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        faces = self.detector(gray, 0)
        try:
            # loop over the face detections
            for face in faces:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, face)
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

        except:
            # handle event when eyes are close to the edge of the screen
            left_eye_perimeter.set((0, 0, 0, 0))
            right_eye_perimeter.set((0, 0, 0, 0))
