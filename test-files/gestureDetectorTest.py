import gestureDetector
from gestureDetector import GestureDetector
from timerClass import Timer
from unittest import mock
from unittest.mock import Mock

detector = GestureDetector(3)


def test_gesture_detector_init():
    assert detector.time_increment is 3
    assert detector.timer is not None
    assert detector.has_made_blink is False
    assert detector.has_made_palm is False
    assert detector.has_made_fist is False
    assert detector.blink_callback is None
    assert detector.palm_callback is None
    assert detector.fist_callback is None
    assert detector.source = None



def test_gesture_detector_set_right_wink_callback():
    mock_callback = Mock()

    detector.on_right_wink(mock_callback);

    assert detector.right_wink_callback is not None
    assert detector.right_wink_callback is mock_callback


def test_gesture_detector_set_left_wink_callback():
    mock_callback = Mock()

    detector.on_left_wink(mock_callback);

    assert detector.left_wink_callback is not None
    assert detector.left_wink_callback is mock_callback


def test_gesture_detector_set_palm_callback():
    mock_callback = Mock()

    detector.on_palm(mock_callback);

    assert detector.palm_callback is not None
    assert detector.palm_callback is mock_callback


def test_gesture_detector_set_fist_callback():
    mock_callback = Mock()

    detector.on_fist(mock_callback);

    assert detector.fist_callback is not None
    assert detector.fist_callback is mock_callback


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
    test_gesture_detector_set_right_wink_callback()
    test_gesture_detector_set_left_wink_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_on_tick_right_wink()
    test_gesture_detector_on_tick_left_wink()
    test_gesture_detector_on_tick_palm()
    test_gesture_detector_on_tick_fist()

    print("<=========== GestureDetector tests have passed. ===========>")