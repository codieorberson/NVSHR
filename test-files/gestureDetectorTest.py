import gestureDetector
from gestureDetector import GestureDetector
from timerClass import Timer
from unittest import mock
from unittest.mock import Mock
import dlib

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


# @mock.patch("os.path.getsize")
# def test_gesture_detector_on_tick_check_logfile_exists():



@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_right_wink(mock_detector):
    mock_detector.return_value.has_made_right_wink = True
    mock_detector.return_value.right_wink_callback(print("Right wink callback was called."))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_left_wink(mock_detector):
    mock_detector.return_value.has_made_left_wink = True
    mock_detector.return_value.left_wink_callback(print("Left wink callback was called."))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_palm(mock_detector):
    mock_detector.return_value.has_made_palm = True
    mock_detector.return_value.palm_callback(print("Palm callback was called."))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()


@mock.patch("gestureDetector.GestureDetector")
def test_gesture_detector_on_tick_fist(mock_detector):
    mock_detector.return_value.has_made_fist = True
    mock_detector.return_value.fist_callback(print("Fist callback was called."))

    mock = gestureDetector.GestureDetector(3)
    mock.on_tick()


if __name__ == '__main__':

    test_gesture_detector_init()
    test_gesture_detector_set_blink_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_set_palm_callback()
    # test_gesture_detector_on_tick_right_wink()
    # test_gesture_detector_on_tick_left_wink()
    # test_gesture_detector_on_tick_palm()
    # test_gesture_detector_on_tick_fist()

    print("<=========== GestureDetector tests have passed. ===========>")