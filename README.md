# Non-Verbal Smart Home Recognition (NVSHR) System 

### Environment Set-Up

 If you are using a Windows machine, please check and make sure you are using the current SDK files.
 You can most likely find these files in your C directory (C:\Program Files (x86)\Microsoft SDKs\Windows Kits) or similar directory.
 If the SDKs are missing, you can download them from the official Windows website (https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk) or install the tool kits via Visual Studio Installer.
 *An example image is stored here (https://github.com/codieorberson/NVSHR/blob/master/Src/pics/SDKs.png).*
 
 *If an IDE is being used, ensure that Cmake is installed before installing dlib.*
 
 For Windows machines, please follow these steps to set up your environment for the NVSHR System:

1. Install Python3.7 (https://www.python.org/downloads/)

2. Once Python3.7 has finished downloading, open a command prompt and install the package needed for this project by running the following commands:
   + `pip install numpy`
   + `pip install opencv-python`
   + `pip install Cmake`
   + `pip install dlib`
   
   These libraries are needed for the NVSHR System to properly run on your machine. 

3. Once all the needed libraries are finished downloading, run `environment_test.py` in the root directory.
   The following output indicates that the correct libraries were downloaded (Minor differences in version numbers will not cause issues): 
    + Version of numpy is: 1.17.2
    + Version of OpenCV is: 4.1.1
    + Version of dlib is: 19.17.0
    + Version of imutils is: 0.5.3
    
 For Mac machines, please follow these steps to set up your environment for the NVSHR System:

1. Install Homebrew (https://docs.brew.sh/Installation)

2. Once Homebrew is finished installing, please run the following commands to download the latest version of Python and pip:
   + `brew install python`
   + `sudo easy_install pip`

3. Once Python and pip have finished downloading, open a command prompt and install the packages needed for this project by running the following commands:
   + `pip install numpy`
   + `pip install opencv-python`
   + `pip install Cmake`
   + `pip install dlib`
   
   These libraries are needed for the NVSHR System to properly run on your machine. 

4. Once all the needed libraries are finished downloading, run `environment_test.py` in the root directory.
   The following output indicates that the correct libraries were downloaded (Minor differences in version numbers will not cause issues): 
    + Version of numpy is: 1.17.2
    + Version of OpenCV is: 4.1.1
    + Version of dlib is: 19.17.0
    + Version of imutils is: 0.5.3

### Initializing the NVSHR System

Follow these steps to initialize the NVSHR system on your device: 

1. Run `main.py`. 
    + The default "tick" time is set at 4 seconds. If you wish to initialize this time interval to a custom time, please pass this time increment in as your second argument. *For example: `python main.py 5`* 

2. After running the previous command, a pop-up window will appear with video feedback from the connected camera. Please ensure the camera is placed properly so that the user is within the camera frame. 
    
### Testing the NVSHR System

For unit testing purposes, the NVSHR system will make use of Magic Mock for various tests. 

To run all unit tests:

1. Navigate to `test-files`

2. If a `logfile.txt` file exists within the `test-files` directory, delete it before moving on to step 3. *This file should be deleted after each run of all tests.*

3. Complie and run `main_test.py`. The console will output data based on the test results. Please look through console output to ensure all tests have passed.
