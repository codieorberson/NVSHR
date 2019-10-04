import gestureDetector
from gestureDetector import GestureDetector
from timerClass import Timer
from unittest import mock
from unittest.mock import Mock
import dlib
import os

detector = GestureDetector(3, detector=dlib.get_frontal_face_detector(),
                           predictor=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'))


def test_gesture_detector_init():
    assert detector.time_increment is 3, "gestureDetector.time_increment was not initialized correctly."
    assert detector.timer is not None, "gestureDetector.timer was not created correctly"
    assert detector.has_made_blink is False, "gestureDetector.has_made_blink was not initialized correctly"
    assert detector.has_made_palm is False, "gestureDetector.has_made_palm was not initialized correctly"
    assert detector.has_made_fist is False, "gestureDetector.has_made_fist was not initialized correctly"
    assert detector.blink_callback is None, "gestureDetector.blink_callback was not initialized correctly"
    assert detector.palm_callback is None, "gestureDetector.palm_callback was not initialized correctly"
    assert detector.fist_callback is None, "gestureDetector.fist_callback was not initialized correctly"
    assert detector.source is None, "gestureDetector.source was not initialized correctly"
    assert detector.detector is not None, "gestureDetector.detector was not initialized correctly"
    assert detector.predictor is not None, "gestureDetector.predictor was not initialized correctly"
    assert detector.ear_thresh == 0.2, "gestureDetector.ear_thresh was not initialized correctly"
    assert detector.ear_consec_frame is 2, "gestureDetector.ear_consec_frame was not initialized correctly"
    assert detector.ear is None, "gestureDetector.ear was not initialized correctly"
    assert detector.blinks is None, "gestureDetector.blinks was not initialized correctly"
    assert detector.cont_frames is 0, "gestureDetector.cont_frames was not initialized correctly"
    assert detector.file is None, "gestureDetector.file was not initialized correctly"

    print("test_gesture_detector_init() passed.")


def test_gesture_detector_set_blink_callback():
    mock_callback = Mock()

    detector.on_blink(mock_callback);

    assert detector.blink_callback is not None
    assert detector.blink_callback is mock_callback

    print("test_gesture_detector_set_blink_callback() passed.")


def test_gesture_detector_set_palm_callback():
    mock_callback = Mock()

    detector.on_palm(mock_callback);

    assert detector.palm_callback is not None
    assert detector.palm_callback is mock_callback

    print("test_gesture_detector_set_palm_callback() passed.")


def test_gesture_detector_set_fist_callback():
    mock_callback = Mock()

    detector.on_fist(mock_callback);

    assert detector.fist_callback is not None
    assert detector.fist_callback is mock_callback

    print("test_gesture_detector_set_fist_callback() passed.")


@mock.patch("os.path.getsize", return_value=0)
def test_gesture_detector_on_tick_check_logfile_not_exists(log_location):
    detector.on_tick()

    assert detector.file is not None, "gestureDetector.file was not created and opened for writing."
    assert os.stat("logfile.txt").st_size is not 0, "gestureDetector.file header was not written"

    print("test_gesture_on_tick_check_logfile_not_exists() passed.")


def test_gesture_detector_on_tick_check_logfile_exists():
    detector.on_tick()

    assert detector.file is not None, "gestureDetector.file was not opened for writing."

    print("test_gesture_on_tick_check_logfile_exists() passed.")


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_blink(mock_detector):
    mock_detector.return_value.has_made_blink = True
    mock_detector.return_value.right_blink(print("* Blink callback was called. *"))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()

    print("test_gesture_detector_on_tick_blink() passed.")


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_palm(mock_detector):
    mock_detector.return_value.has_made_palm = True
    mock_detector.return_value.palm_callback(print("* Palm callback was called. *"))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()

    print("test_gesture_detector_on_tick_palm() passed.")


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_fist(mock_detector):
    mock_detector.return_value.has_made_fist = True
    mock_detector.return_value.fist_callback(print("* Fist callback was called. *"))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()

    print("test_gesture_detector_on_tick_fist() passed.")


if __name__ == '__main__':

    test_gesture_detector_init()
    test_gesture_detector_set_blink_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_on_tick_check_logfile_not_exists()
    test_gesture_detector_on_tick_check_logfile_exists()
    test_gesture_detector_on_tick_blink()
    test_gesture_detector_on_tick_palm()
    test_gesture_detector_on_tick_fist()

    print("<=========== GestureDetector tests have passed. ===========>")