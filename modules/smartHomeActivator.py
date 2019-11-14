from smartPlugManager import SmartPlugManager
from soundPlayer import SoundPlayer

class SmartHomeActivator():
    def __init__(self):
       self.smart_plug_manager = SmartPlugManager()
       self.sound_player = SoundPlayer()

    def activate(self, smartHomeAction, device):
        if device == "Smart Plug":
            ip_address = smartHomeAction
            is_playing_sound = False
            try:
                self.smart_plug_manager.turn_on_off(ip_address)
                is_playing_sound = True
            except: 
                self.sound_player.speak("Unable to communicate with Smart Plug at " + ip_address)

            if is_playing_sound:
                self.sound_player.play_success_sound()
                #I feel like this would be a better action to do on success of a
                #plug activation, let me know what you guys think:
#                self.speaker.speak("Smart Plug " + ip_address + " toggled.")

        elif device == 'Alexa':
            self.sound_player.speak(smartHomeAction)
            print('"' + smartHomeAction + '" sent to ' + device + '.\n')
