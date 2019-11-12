from speaker import Speaker
import sys
from TPLink import TPLinkDevice

class SmartHomeActivator():
    def __init__(self):
       self.speaker = Speaker()
       self.Tp_Link_Devices = TPLinkDevice()

    def activate(self, smartHomeAction, device):
        if device == "Smart Plug":
            ip_address = smartHomeAction
            self.Tp_Link_Devices.turn_on_off(ip_address)
            speaker.speak("Smart Plug " + ip_address + " toggled.")
            self.subprocess_executor.execute('./modules/smart_home/sound.py', './static_data/success.wav')
        elif device == 'Alexa':
            self.speaker.speak(smartHomeAction)

        print('"' + smartHomeAction + '" sent to ' + device + '.\n')
