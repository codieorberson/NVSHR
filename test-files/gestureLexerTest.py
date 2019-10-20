from datetime import datetime
import gestureDetector
from gestureLexer import GestureLexer
from logger import Logger
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from handGestureDetector import HandGestureDetector
from blinkDetector import BlinkDetector
from unittest import mock
from unittest.mock import Mock, MagicMock
import dlib
import os

logger = Logger()
lexer = GestureLexer(logger)

def test_gesture_lexer_init():
    assert lexer.logger is logger, "gestureLexer.logger was not initialized correctly."
    assert lexer.gestures is not None, "gestureLexer.gestures was not initialized correctly."
    assert lexer.gesture_patterns is not None, "gestureLexer.gesture_patterns was not initialized correctly."

    print("test_gesture_lexer_init() passed.")


def test_gesture_lexer_add():
    logger.log_gesture = MagicMock()
    timestamp = datetime.now()

    lexer.add("gesture", timestamp)

    assert logger.log_gesture.called, "gestureLexer.add did not log into the file."
    assert lexer.gestures[0] is not None, "gestureLexer.add did not append gesture in lexer.gestures"

    print("test_gesture_lexer_add() passed.")


if __name__ == '__main__':

    test_gesture_lexer_init()
    test_gesture_lexer_add()

    print("<=========== GestureLexer tests have passed. ===========>")