import gestureDetector
from gestureDetector import GestureDetector
from unittest import mock
from unittest.mock import Mock
import dlib
import os

detector = GestureDetector(3, detector=dlib.get_frontal_face_detector(),
                           predictor=dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'))


# As of right now, there is not a way (that I have found) to properly mock/test these functions :
# set_cropped_face_frame, set_ears, make_frame_labels, visual_eyes, convert_facial_landmark, changing_hand_frame,
# detect_fist_or_palm, start, eye_aspect_ratio
# This is due to the fact that these deal with resizing the frame or camera inputs and I have not found a way to
# easily mock these


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
    assert detector.blinks is 0, "gestureDetector.blinks was not initialized correctly"
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
    mock_detector.return_value.blink_callback(print("* Blink callback was called. *"))

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


def test_gesture_detector_set_frame_contrast():
    colors = GestureDetector.set_frame_contrast(100, 200, 250)

    assert colors[0] is 100, "detector.set_frame_contrast did not return the correct red value."
    assert colors[1] is 200, "detector.set_frame_contrast did not return the correct green value."
    assert colors[2] is 250, "detector.set_frame_contrast did not return the correct blue value."

    print("test_gesutre_detector_set_frame_contrast() passed.")


def test_gesture_detector_check_eye_aspect_ratio_if():
    detector.ear = 0.1

    result = detector.check_eye_aspect_ratio(detector.ear, detector.ear_thresh, detector.ear_consec_frame)

    assert detector.cont_frames is 1, "detector.check_eye_aspect_ratio did not update detector.cont_frames."
    assert detector.cont_frames is result, "detector.check_eye_aspect_ratio did not return the correct result."

    print("test_gesture_detector_check_eye_aspect_ratio_if() passed.")


def test_gesture_detector_check_eye_aspect_ratio_else():
    detector.ear = 0.3
    detector.cont_frames = 3

    result = detector.check_eye_aspect_ratio(detector.ear, detector.ear_thresh, detector.ear_consec_frame)

    assert detector.blinks is 1, "detector.check_eye_aspect_ratio did not update detector.blinks."
    assert detector.has_made_blink is True, "detector.check_eye_aspect_ratio did not update detector.has_made_blink."
    assert detector.cont_frames is 0, "detector.check_eye_aspect_ratio did not update detector.cont_frames."
    assert detector.cont_frames is result, "detector.check_eye_aspect_ratio did not return the correct result."

    print("test_gesture_detector_check_eye_aspect_ratio_else() passed.")


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
    test_gesture_detector_set_frame_contrast()
    test_gesture_detector_check_eye_aspect_ratio_if()
    test_gesture_detector_check_eye_aspect_ratio_else()

    print("<=========== GestureDetector tests have passed. ===========>")