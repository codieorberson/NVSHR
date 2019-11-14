from smartPlugManager import SmartPlugManager
from speaker import Speaker

class SmartHomeActivator():
    def __init__(self):
       self.speaker = Speaker()
       self.smart_plug_manager = SmartPlugManager()

    def activate(self, smartHomeAction, device):
        if device == "Smart Plug":
            ip_address = smartHomeAction
            self.smart_plug_manager.turn_on_off(ip_address)
            speaker.speak("Smart Plug " + ip_address + " toggled.")
            self.subprocess_executor.execute('./modules/smart_home/sound.py', 
                    './static_data/success.wav')
        elif device == 'Alexa':
            self.speaker.speak(smartHomeAction)

        print('"' + smartHomeAction + '" sent to ' + device + '.\n')
