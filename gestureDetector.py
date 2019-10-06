import cv2
from timerClass import Timer
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import datetime
import dlib
import os


class GestureDetector():
    def __init__(self, time_increment, detector, predictor):
        self.time_increment = time_increment  # time increment used by the system to check for gestures/blinks
        self.timer = Timer(self.time_increment)
        self.has_made_fist = False
        self.has_made_palm = False
        self.has_made_blink = False
        self.fist_callback = None
        self.palm_callback = None
        self.blink_callback = None
        self.fist = None
        self.palm = None
        self.source = None
        self.detector = detector
        self.predictor = predictor
        self.ear_thresh = 0.2
        self.ear_consec_frame = 2
        self.ear = None  # eye aspect ratio
        self.blinks = 0
        self.cont_frames = 0
        self.file = None

    def on_fist(self, callback):
        self.fist_callback = callback

    def on_palm(self, callback):
        self.palm_callback = callback

    def on_blink(self, callback):
        self.blink_callback = callback

    def on_tick(self):
        file_exists = os.path.exists("logfile.txt")
        if file_exists == False:
            self.file = open("logfile.txt", 'w+')
            self.file.write("   Date        Time     Command\n")
        else:
            self.file = open("logfile.txt", "a+")
        now = datetime.datetime.now()

        print("tick")  # used for debugging purposes

        if self.has_made_fist and self.fist_callback:
            self.fist_callback()
            self.has_made_fist = False
            fist_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                          12:19], "    ", "fist", " \n")
            fist_text = ''.join(fist_tuple)
            self.file.write(fist_text)

        if self.has_made_palm and self.palm_callback:
            self.palm_callback()
            self.has_made_palm = False
            palm_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                          12:19], "    ", "palm", "\n")
            palm_text = ''.join(palm_tuple)
            self.file.write(palm_text)

        if self.has_made_blink and self.blink_callback:
            self.blink_callback()
            self.has_made_blink = False
            blink_tuple = (now.isoformat()[:10], "    ", now.isoformat()[
                12:19], "    ", "blink", "\n")
            blink_text = ''.join(blink_tuple)
            self.file.write(blink_text)

        self.file.close()

    def set_frame_contrast(Red, Green, Blue):  # used for creating contrast within the frame to detect hand gestures
        # more clearly
        redContrast = Red
        greenContrast = Green
        blueContrast = Blue
        return [redContrast, greenContrast, blueContrast]

    def set_cropped_face_frame(self, rects, frame, color_frame):
        rects = self.detector(color_frame, 0)
        for rect in rects:
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            face = frame[y: y + h, x: x + w]
            face = imutils.resize(face, width=400)
            cv2.imshow("Cropped Blink Frame", face)

    def set_ears(self, leftEye, rightEye):
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        self.ear = (leftEAR + rightEAR) / 2.0

    # check to see if the eye aspect ratio is below the blink
    # threshold, and if so, increment the blink frame counter
    def check_eye_aspect_ratio(self, ear, ear_thresh, ear_consec_frame):
        if ear < ear_thresh:
            self.cont_frames += 1
        # otherwise, the eye aspect ratio is not below the blink
        # threshold
        else:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            if self.cont_frames >= self.ear_consec_frame:
                self.blinks += 1  # This is where its printing out all the blinks in total
                self.has_made_blink = True
                # reset the eye frame counter
                self.cont_frames = 0
        return self.cont_frames

    # draw the total number of blinks on the frame along with
    # the computed eye aspect ratio for the frame
    def make_frame_labels(self, frame):
        cv2.putText(frame, "Blinks: {}".format(self.blinks), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(self.ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return frame

    # compute the convex hull for the left and right eye, then
    # visualize each of the eyes
    def visualize_eyes(self, leftEye, rightEye, frame):
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    def convert_facial_landmark(self, shape, rect, frame_color):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        return leftEye, rightEye

    def changing_hand_frame(self, frame, low_cont, high_cont):
        mask = cv2.inRange(frame, low_cont, high_cont)
        mask_inv = cv2.bitwise_not(mask)
        color_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def detect_fist_or_palm(self, frame):
        fist_cascade = cv2.CascadeClassifier('fist.xml')
        palm_cascade = cv2.CascadeClassifier('palm.xml')
        self.fist = fist_cascade.detectMultiScale(frame, 1.3, 5)
        self.palm = palm_cascade.detectMultiScale(frame, 1.3, 5)

        if len(self.fist) > 0:
            self.has_made_fist = True
        if len(self.palm) > 0:
            self.has_made_palm = True

        for (x, y, w, h) in self.fist:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        for (x, y, w, h) in self.palm:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    def start(self):
        self.timer.on_time(self.on_tick)

        self.source = VideoStream(src=0).start()

        while True:

            blink_frame = self.source.read()
            cropped_blink_frame = imutils.resize(self.source.read(), width=800)
            gray = cv2.cvtColor(cropped_blink_frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale blink_frame
            rects = self.detector(gray, 0)

            # loop over the face detections
            for rect in rects:

                shape = self.predictor(gray, rect)
                leftEye, rightEye = GestureDetector.convert_facial_landmark(
                    self, shape, rect, gray)
                # average the eye aspect ratio together for both eyes
                GestureDetector.set_ears(
                    self, leftEye, rightEye)
                GestureDetector.visualize_eyes(
                    self, leftEye, rightEye, cropped_blink_frame)
                GestureDetector.check_eye_aspect_ratio(
                    self, self.ear, self.ear_thresh, self.ear_consec_frame)
                GestureDetector.make_frame_labels(self, blink_frame)
                GestureDetector.set_cropped_face_frame(
                    self, rects, cropped_blink_frame, gray)

            hand_frame = self.source.read()
            low_contrast = np.array(GestureDetector.set_frame_contrast(0, 0, 0))
            high_contrast = np.array(
                GestureDetector.set_frame_contrast(132, 255, 255))

            gray_frame = GestureDetector.changing_hand_frame(
                self, hand_frame, low_contrast, high_contrast)


            GestureDetector.detect_fist_or_palm(self, gray_frame)

            self.timer.check_time()
            cv2.imshow("Blink Frame", blink_frame)
            cv2.imshow('Hand Gesture Frame', gray_frame)

            key = cv2.waitKey(1) & 0xff
            if key == ord('q'):
                self.file = open("logfile.txt", "w+")
                self.file.seek(0)
                self.file.truncate()
                self.file.close()
                break

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear
