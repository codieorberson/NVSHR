from datetime import datetime
from gestureParser import GestureParser
from logger import Logger
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector
from unittest.mock import Mock, MagicMock


class TestClass():

    def __init__(self):
        self.called = False

    def set_called(self, value):
        self.called = value


logger = Logger()
parser = GestureParser(logger)
test = TestClass()


def testing_add_pattern():
    test.called = True
    print("Testing add pattern.")


def test_gesture_parser_init():
    assert parser.logger is logger, "parser.logger was not initialized correctly."
    assert parser.gesture_pattern_map is not None, "parser.gesture_pattern_map was not initialized correctly."

    print("test_gesture_parser_init() passed.")


def test_gesture_parser_add_pattern():
    parser.add_pattern(['fist', 'palm', 'blink'], lambda: testing_add_pattern())

    assert len(parser.gesture_pattern_map) is 1, "parser.add_pattern did not correctly add gesture pattern."

    print("test_gesture_parser_add_pattern() passed.")


def test_gesture_parser_parse_pattern():
    timestamp = datetime.now()

    logger.log_gesture_sequence = MagicMock()

    parser.parse_pattern(['fist', 'palm', 'blink'], timestamp)

    assert logger.log_gesture_sequence.called, "parser.parse_pattern did not log the gesture to logger."
    assert test.called is True, "parser.parse_pattern did not call the related event for the gesture pattern."

    print("test_gesture_parser_parse_pattern() passed.")


def test_gesture_parser_parse_patterns():
    timestamp = datetime.now()

    patterns = [['fist', 'palm'], ['fist', 'palm', 'blink']]

    parser.parse_pattern = MagicMock()

    parser.parse_patterns(patterns, timestamp)

    assert parser.parse_pattern.called

    print("test_gesture_parser_parse_patterns() passed.")


if __name__ == '__main__':
    test_gesture_parser_init()
    test_gesture_parser_add_pattern()
    test_gesture_parser_parse_pattern()
    test_gesture_parser_parse_patterns()

    print("<=========== GesturePrser tests have passed. ==============>")
