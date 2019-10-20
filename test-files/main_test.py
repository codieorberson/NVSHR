from subprocess import call


if __name__ == '__main__':
    call(["python", "gestureTest.py"])
    call(["python", "gestureLexerTest.py"])
    call(["python", "gestureParserTest.py"])
    call(["python", "gestureDetectorTest.py"])
