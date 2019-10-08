from timerClass import Timer
from unittest import mock
from unittest.mock import Mock
import time

timer = Timer(3)


def test_timer_init():
    assert timer.time_increment is 3
    assert timer.callback is None

    print("test_timer_init() passed.")


def test_timer_set_time():
    timer.set_time(4)

    assert timer.time_increment is 4

    print("test_timer_set_time() passed.")


@mock.patch("timerClass.Timer")
def test_timer_on_time(mock_timer):
    mock_timer.return_value.on_time(print("* On time was called. *"))

    timer.on_time(timer.set_time(6))

    assert timer.callback is timer.set_time(6)

    print("test_timer_on_time() passed.")


def test_timer_check_time():
    timer.check_time()

    assert timer.time_increment is 6
    print("* Check time was called, callback was called. *")
    print("test_timer_check_time() passed.")


if __name__ == '__main__':
    test_timer_init()
    test_timer_set_time()
    test_timer_on_time()
    test_timer_check_time()

    print("<================ Timer class tests passed. ===============>")
