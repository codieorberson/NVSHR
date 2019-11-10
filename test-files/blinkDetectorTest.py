from blinkDetector import BlinkDetector


# sys.modules['cv2'] = MagicMock()


# Can't mock frame to test the detect method. If time, will re-visit.

def test_init():
    detector = BlinkDetector()
    # assert detector.source is None, "blinkDetector.source was not initialized correctly"
    # assert detector.blinks is None, "blinkDetector.blink was not initialized correctly"
    assert detector.ear is None, "blinkDetector.ear was not initialized correctly"
    assert detector.ear_consec_frame == 2, "blinkDetector.ear_consec_frame was not initialized correctly"
    assert detector.ear_thresh == 0.2, "blinkDetector.ear_thresh was not initialized correctly"
    assert detector.detector is not None, "blinkDetector.detector was not initialized correctly"
    assert detector.predictor is not None, "blinkDetector.predictor was not initialized correctly"
    print("<=========== test_init() passed. ===========>")


# def test_detect(self=None, frame=None, left_eye_perimeter=None, right_eye_perimeter=None):
#     left_eye_perimeter = 2
#     right_eye_perimeter = 2
#     detect = BlinkDetector.detect(self, frame, left_eye_perimeter, right_eye_perimeter)
#     assert detect.called, "blinkDetector.detector was not initialized correctly"


if __name__ == '__main__':
    test_init()
    print("<=========== blinkDetector tests have passed. ===========>")
