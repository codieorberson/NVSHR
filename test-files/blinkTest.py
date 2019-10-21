import Blink
from Blink import Blink
from unittest import mock
from unittest.mock import Mock
import dlib
import os

detector = Blink(detector=dlib.get_frontal_face_detector(),
                 predictor=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'), ear_thresh=0.2,
                 ear_consec_frame=2, ear=None, blinks=None, source=None)


def test_blink_init():
    assert detector.blinks is None, "blink.blinks was not initialized correctly"
    assert detector.ear is None, "blink.ear was not initialized correctly"
    assert detector.ear_consec_frame is 2, "blink.ear_consec_frame was not initialized correctly"
    assert detector.ear_thresh == 0.2, "blink.ear_thresh was not initialized correctly"
    assert detector.source is None, "blink.sources was not initialized correctly"

    print("test_blink_init() passed.")


if __name__ == '__main__':
    test_blink_init()

    print("<================ Blink class tests passed. ===============>")
