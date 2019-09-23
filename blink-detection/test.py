import dlib
from Blink import Blink
blink_detector = Blink(detector = dlib.get_frontal_face_detector(),
                     predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat'))

blink_detector.detect()
