import sys
import cv2
from datetime import datetime
from multithreadedPerimeter import MultithreadedPerimeter
from processManager import ProcessManager
from logger import Logger
from gestureDetector import GestureDetector
from gestureLexer import GestureLexer
from gestureParser import GestureParser

logger = Logger()
gesture_detector = GestureDetector()
gesture_lexer = GestureLexer(logger)
gesture_parser = GestureParser(logger)

#The first command line argument determines the minimum time needed between
#identical gestures for them to be considered separate gestures in a pattern.
if len(sys.argv) > 1:
    min_increment = float(sys.argv[1])
else:
    min_increment = 2

#The second command line argument determines the maximum time that can lapse
#without a gesture before gestures are collected into a gesture pattern.
if len(sys.argv) > 2:
    max_increment = float(sys.argv[2])
else:
    max_increment = 5

#The third command line argument determines the EAR at which blinks and winks
#are detected.
if len(sys.argv) > 3:
    open_eye_threshold = float(sys.argv[3])
else:
    open_eye_threshold = 0.2

#Add three callbacks to gesture_detector. These anonymous functions (also known
#as lambdas) take a timestamp and tell gesture_lexer to record a gesture at
#that time. The particular sort of gesture passed is indicated by a string.
#These anonymous functions will not actually pass any values into
#gesture_lexer.add right now, the lambdas will only execute when
#when gesture_detector tells them to.
gesture_detector.on_fist(lambda timestamp: gesture_lexer.add("fist", timestamp))
gesture_detector.on_palm(lambda timestamp: gesture_lexer.add("palm", timestamp))
gesture_detector.on_blink(lambda timestamp: gesture_lexer.add("blink", timestamp))

#This is a test pattern to find in a gesture sequence. The gesture sequence 
#being detected as a pattern must be made up of strings which correspond to the
#strings passed into gesture_lexer.add in the anonymous lambdas above.
gesture_parser.add_pattern(['fist', 'palm', 'fist'], lambda: print("fist-palm-fist event has fired -- this message is not logged, only printed."))

should_continue = True
cap = cv2.VideoCapture(0)

#This process manager is what spawns child processes and returns control to the
#parent process when they all finish. All of the multithreaded logic is
#contained in ProcessManager and MultithreadedPerimeter. You'll see a
#demonstration of them being used together shortly.
process_manager = ProcessManager()

while should_continue:

    ret, frame = cap.read()
    timestamp = datetime.now()
    
    #These multithreaded perimeters are the only objects which hold values that
    #are shared between threads. The frame, for example, is copied for each 
    #core in the processor, and drawing on a frame inside of a child process
    #will not affect the original frame in the parent process. Checking for
    #changes in the values held by multithreaded perimeters is the only way
    #that the code currently communicates from a child process to a parent
    #process (besides returning control via ProcessManager).
    fist_perimeter = MultithreadedPerimeter()
    palm_perimeter = MultithreadedPerimeter()
    left_eye_perimeter = MultithreadedPerimeter()
    right_eye_perimeter = MultithreadedPerimeter() 

    #This line aggregates gestures into gesture sequences.
    gesture_sequences = gesture_lexer.lex(timestamp, min_increment, max_increment)

    #This line creates a child process to check for predefined patterns of
    #gestures in the list of gesture sequences we just aggregated. The child
    #process gets added to the thread pool, but we don't know exactly when it
    #will start executing.
    process_manager.add_process(gesture_parser.parse_patterns, 
            (gesture_sequences, timestamp))

    #This line spawns another child process, this time telling gesture_detector
    #to find gestures in the current frame. We pass the frame in for detection,
    #but we won't be drawing to it in GestureDetector. GestureDetector will
    #spawn a bunch of child processes of it's own, and those will be passed
    #the MultithreadedPerimeters. Those grandchild (and great-grandchild) 
    #processes will set the values contained in the multithreaded perimeter if
    #they detect the relevant gestures. 
    #(Side note -- if we want to display the frame using the same filters used
    #for detection, we should apply those filters before this point. Currently
    #that is done in GestureDetector, and we display the frame as captured.)
    process_manager.add_process(gesture_detector.detect, 
            (frame, timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, 
            left_eye_perimeter, right_eye_perimeter))

    #The child processes may or may not have started by now. Calling on_done
    #will make the current process cede control until all of the subprocesses
    #are finished executing.
    process_manager.on_done()
    #Now we are gauranteed that those subprocesses are finished operating on
    #the MultithreadedPerimeter instances.

    #I separated out the callback triggers so that they could be run 
    #synchronously after the subprocess were finished. This allows lots of
    #relatively big and awkward data, like lists of strings and datestamps, to
    #be passed around without worrying about accessing them between cores.
    #As is we're only storing 16 unsigned integers between cores, and adding
    #arrays of strings would be a whole mess. I think it's more efficient to do
    #this bit synchronously, but that doesn't mean I like how it is cureently
    #written. This is where gesture_detector actually executes the lambdas that
    #were defined near the beginning of this file, if the perimeters passed are
    #defined (and in the case of the eye perimeters, if they additionally have
    #an average EAR below the threshold value).
    gesture_detector.trigger_events(timestamp, open_eye_threshold, fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter)

    #Now we're gonna draw all those beautiful rectangles based on the top and
    #bottom corners of those MultithreadedPerimeter instances. 
    #MultithreadedPerimeter's interface returns (x, y) coordinate tuples,
    #because that is what OpenCV wants to draw rectangles based on.
    for perimeter in [fist_perimeter, palm_perimeter, left_eye_perimeter, right_eye_perimeter]:
        #Currently they're all red, because that was easy. I think we should
        #display eyes below the EAR threshold differently than eyes above that
        #threshold, though. Different hand colors would be good, too. I'm
        #honestly unsure where the EAR check belongs, it would ideally be 
        #implemented in one place. I think there may be a need for some
        #container class that manages two MultithreadedPerimeter instances that
        #represent a pair of eyes.
        if perimeter.is_set():
            cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)

    #Display the frame, flipping it to look like a mirror. I have way too much
    #trouble orienting my body to get gestures detected without doing this.
    #It's pretty embarassing.
    cv2.imshow('NVSHR', cv2.flip(frame, 1))
    
    #Break the loop, in theory.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        should_continue = False

#Close down OpenCV.
cap.release()
cv2.destroyAllWindows()

#Close log file.
logger.close()
