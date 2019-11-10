import pyttsx3
#^^^If testing on windows, install both pyttsx3 and pypiwin32; on linux, python-espeak and PyAudio must be installed (through the system package manager or from source, not from pip3). Further Linux instructions available here: https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error
from processManager import ProcessManager
from sys import argv

command = argv[1]
engine = pyttsx3.init()

def onWord(name, location, length):
    pass
engine = pyttsx3.init()
engine.connect('started-word', onWord)
engine.say(command)
engine.runAndWait()

