from gestureDetector import GestureDetector
from unittest.mock import Mock

detector = GestureDetector(3)


def test_gesture_detector_init():
    assert detector.time_increment is 3
    assert detector.has_made_right_wink is False
    assert detector.has_made_left_wink is False
    assert detector.has_made_palm is False
    assert detector.has_made_fist is False
    assert detector.right_wink_callback is None
    assert detector.left_wink_callback is None
    assert detector.palm_callback is None
    assert detector.fist_callback is None


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


def test_gesture_detector_on_tick_right_wink():
    mock_detector = Mock(detector)
    mock_detector.on_left_wink(lambda: print("Passed."))
    mock_detector.has_made_right_wink = True




if __name__ == '__main__':

    test_gesture_detector_init()
    test_gesture_detector_set_right_wink_callback()
    test_gesture_detector_set_left_wink_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_set_palm_callback()

    print("<=========== GestureDetector tests have passed. ===========>")