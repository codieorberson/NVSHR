from blinkDetector import BlinkDetector


def test_init():
    detector = BlinkDetector.__init__()
    assert detector.source is None, "blinkDetector.source was not initialized correctly"
    assert detector.blinks is None, "blinkDetector.blink was not initialized correctly"
    assert detector.ear is None, "blinkDetector.ear was not initialized correctly"
    assert detector.ear_consec_frame == 2, "blinkDetector.ear_consec_frame was not initialized correctly"
    assert detector.ear_thresh == 0.2, "blinkDetector.ear_thresh was not initialized correctly"
    assert detector.detector is not None, "blinkDetector.detector was not initialized correctly"
    assert detector.predictor is not None, "blinkDetector.predictor was not initialized correctly"


def test_detect():
    detect = BlinkDetector.detect()
    assert detect is not None, "blinkDetector.detector was not initialized correctly"
