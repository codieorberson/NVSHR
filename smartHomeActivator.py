#import homeassistant


import pyttsx3
#^^^If testing on windows, install both pyttsx3 and pypiwin32; on linux, python-espeak must be installed (through the system package manager or from source, not from pip3).

_text_to_speech_engine = pyttsx3.init()

def _text_to_wav(text):
    _text_to_speech_engine.say(text)
    _text_to_speech_engine.runAndWait()


def _connect_to_home_assistant():
    try:
    # After installing homeassistant, go to localhost:8123 in your browser, then
    # set up a profile (name and password can be whatevs) and go to 
    # localhost:8123/profile and scroll down to the bottom of the page where 
    # they let you generate a key. Copy that key and paste it into an otherwise
    # blank text file. Save that file in the project directory as 
    # homeassistant.key
    # (To get to the profile page the first time, you might need to go through 
    # an options menu on the left side of the homeassistant UI -- we should 
    # script this if we have time.)
        with open('homeassistant.key') as file:
            _homeassistant_key = file.readline()[:-1]
    except:
        _homeassistant_key = None
        print('Warning: Homeassistant key not found. No commands will be sent to homeassistant.\n')

    try:
        url = "http://172.30.32.1:8123/api/"
        headers = {
            'Authorization': 'Bearer ' + _homeassistant_key,
            'content-type': 'application/json',
        }
        from requests import get
        response = get(url, headers=headers)
        if response.text != '{"message": "API running."}':
            raise Exception()
    except:
        response = None
        print('Warning: Could not connect to homeassistant. No commands will be sent to homeassisant')

    if response and response.text == '{"message": "API running."}':
        connection = response
    else:
        connection = None

    return connection

class SmartHomeActivator():
    def __init__(self):

       self.connection = _connect_to_home_assistant()
       self.is_connected = bool(self.connection)

    def activate(self, smartHomeAction, device):
        if self.is_connected:
            print('"' + smartHomeAction + '" sent to ' + device + '. ' +
                    "<--(This is a lie, but you are connected to " +
                    "homeassistant.)\n")
            #This needs to actually trigger API calls that use TTS middleware.
        else:
            print('"' + smartHomeAction + '" not actually sent to ' + device +
                    '.\n')
