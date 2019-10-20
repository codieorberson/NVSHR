from gesture import Gesture

gest = Gesture("fist.xml")


def test_gesture_init():
    assert gest.haar_cascade is not None, "gest.haar_cascade was not set when initialized."
    assert gest.debug_color is not None, "gest.debug_color was not set when initialized."
    assert gest.detection_check is not None, "gest.detection_check was not set when initialized."

    print("test_gesture_init() passed.")


def test_gesture_set_rgb_tuple():
    gest.set_debug_color(255)

    assert gest.debug_color is 255, "gest.set_debug_color did not properly set the debug color."

    print("test_gesture_set_rgb_tuple() passed.")


def test_gesture_set_detection_check():
    gest.set_detection_criteria(None)

    assert gest.detection_check is None

    print("test_gesture_set_detection_check() passed.")


if __name__ == '__main__':
    test_gesture_init()
    test_gesture_set_rgb_tuple()
    test_gesture_set_detection_check()

    print("<============= Gesture tests have passed. ==============>")
