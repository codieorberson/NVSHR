from subprocess import call


if __name__ == '__main__':
#It's not clear to me if the next line should be merged or not,
#the tests still don't run on my machine so I'm leaving it up to
#somebody else to uncomment this or delete it:
#    call(["python", "blinkDetectorTest.py"])
    call(["python", "gestureTest.py"])
    call(["python", "gestureLexerTest.py"])
    call(["python", "gestureParserTest.py"])
    call(["python", "gestureDetectorTest.py"])
