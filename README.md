# NVSHR

# Environment Set up
1. Make sure you have SDK files if you are using Windows machine.
   It most likely appear at C:\Program Files (x86)\Microsoft SDKs\Windows Kits or slimilar directory.
   If the SDKs are missing, you can download it from official website of Windows
   https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk
   or install the tool kits via Visual Studio Installer
   see image Src\pics\SDKs.png

2. Install Python3.7 
   https://www.python.org/downloads/

3. Open a command prompt
   install the package needed for this project
   pip install numpy
   pip install opencv-python
   pip install Cmake
   pip install dlib

   These are the libaraies we are using mainly, might involve more later.

4. Test the environment.
   Run the enviornment_test.py in the root directory.
   The following output indicating you are good to go. (minor difference on the version would be fine)
    Version of numpy is: 1.17.2
    Version of OpenCV is: 4.1.1
    Version of dlib is: 19.17.0
    Version of imutils is: 0.5.3

    

Pass an argument into main.py to set the number of seconds between ticks (default is 3).

Everything is sketchy and broken right now, but it does run. Logs "tick" every tick, "fist" if it detected a fist in the last tick, "palm" if it detected a palm with spread out fingers in the last tick, and "wink" if it detected exactly one eye at any point during the last tick. It's WAAAAY too trigger-happy about claiming to see winks, since the eye detection in general is still sketch.

GestureDetector has a bunch of repeating code in it, and we obvious need to abstract that stuff out into a separate class called Gesture.
