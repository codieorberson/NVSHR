from datetime import datetime
from gestureDetector import GestureDetector
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector
from unittest.mock import Mock, MagicMock

detector = GestureDetector()


def test_gesture_detector_init():
    assert isinstance(detector.process_manager, ProcessManager), "gestureDetector.process_manager was not initialized correctly."
    assert isinstance(detector.hand_gesture_detector, HandGestureDetector), "gestureDetector.hand_gesture_detector was not initialized correctly."
    assert isinstance(detector.blink_detector, BlinkDetector), "gestureDetector.blink_detector was not initialized correctly."

    assert detector.fist_event is None, "gestureDetector.fist_event was not initialized correctly."
    assert detector.palm_event is None, "gestureDetector.palm_event was not initialized correctly."
    assert detector.blink_event is None, "gestureDetector.blink_event was not initialized correctly."

    print("test_gesture_detector_init() passed.")


def test_gesture_detector_set_blink_callback():
    mock_callback = Mock()

    detector.on_blink(mock_callback);

    assert detector.blink_event is not None
    assert detector.blink_event is mock_callback

    print("test_gesture_detector_set_blink_callback() passed.")


def test_gesture_detector_set_palm_callback():
    mock_callback = Mock()

    detector.on_palm(mock_callback);

    assert detector.palm_event is not None
    assert detector.palm_event is mock_callback

    print("test_gesture_detector_set_palm_callback() passed.")


def test_gesture_detector_set_fist_callback():
    mock_callback = Mock()

    detector.on_fist(mock_callback);

    assert detector.fist_event is not None
    assert detector.fist_event is mock_callback

    print("test_gesture_detector_set_fist_callback() passed.")


def test_gesture_detector_detect():
    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter()
    timestamp = datetime.now()

    detector.process_manager.add_process = MagicMock()
    detector.process_manager.on_done = MagicMock()

    detector.detect("frame", timestamp, 4, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    assert detector.process_manager.add_process.called, "detector.process_manger.add_process was not called."
    assert detector.process_manager.on_done.called, "detector.on_done.add_process was not called."

    print("test_gesture_detector_detect() passed.")


def test_gesture_detector_set_frame_contrast():
    colors = GestureDetector.set_frame_contrast(100, 200, 250)

    assert colors[0] is 100, "detector.set_frame_contrast did not return the correct red value."
    assert colors[1] is 200, "detector.set_frame_contrast did not return the correct green value."
    assert colors[2] is 250, "detector.set_frame_contrast did not return the correct blue value."

    print("test_gesture_detector_set_frame_contrast() passed.")


def test_gesture_detector_trigger_events_fist():

    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter()
    timestamp = datetime.now()

    fist_perimeter.is_set = MagicMock()
    fist_perimeter.is_set.return_value = True
    detector.fist_event = MagicMock()

    detector.trigger_events(timestamp, 4, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    assert detector.fist_event.called, "detector.trigger_events() did not call the fist callback."

    print("test_gesture_detector_trigger_events_fist() passed.")


def test_gesture_detector_trigger_events_palm():

    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter()
    timestamp = datetime.now()

    palm_perimeter.is_set = MagicMock()
    palm_perimeter.is_set.return_value = True
    detector.palm_event = MagicMock()

    detector.trigger_events(timestamp, 4, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    assert detector.palm_event.called, "detector.trigger_events() did not call the palm callback."

    print("test_gesture_detector_trigger_events_palm() passed.")


def test_gesture_detector_trigger_events_blink():

    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter()
    timestamp = datetime.now()

    left_eye_perimeter.is_set = MagicMock()
    left_eye_perimeter.is_set.return_value = True
    left_eye_perimeter.get_ratio = MagicMock()
    left_eye_perimeter.get_ratio.return_value = 1

    right_eye_perimeter.is_set = MagicMock()
    right_eye_perimeter.is_set.return_value = True
    right_eye_perimeter.get_ratio = MagicMock()
    right_eye_perimeter.get_ratio.return_value = 1

    detector.blink_event = MagicMock()

    detector.trigger_events(timestamp, 400, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    assert detector.blink_event.called, "detector.trigger_events() did not call the blink callback."

    print("test_gesture_detector_trigger_events_blink() passed.")


if __name__ == '__main__':

    test_gesture_detector_init()
    test_gesture_detector_set_blink_callback()
    test_gesture_detector_set_palm_callback()
    test_gesture_detector_set_fist_callback()
    test_gesture_detector_detect()
    test_gesture_detector_trigger_events_fist()
    test_gesture_detector_trigger_events_palm()
    test_gesture_detector_trigger_events_blink()
    #test_gesture_detector_set_frame_contrast()

    print("<=========== GestureDetector tests have passed. ===========>")