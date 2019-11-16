from TPLink import TPLinkDevice
from soundPlayer import SoundPlayer

class SmartHomeActivator():
    def __init__(self):
        self.sound_player = SoundPlayer()
        self.tp_Link_Devices = TPLinkDevice()

    def set_commands(self, commands):
        self.commands = commands

    def activate(self, gesture_sequence, was_recognized):
        if was_recognized:
            try:
                self.turn_on_off_TpLink_Device(gesture_sequence)
                self.sound_player.play_success_sound()
            except:
                print("Unable to connect command to requested smart home device")
        else:
            self.sound_player.play_failure_sound()

    #Iterating through the command dictionary and performing smart home action linked
    #with the given gesture sequence
    def turn_on_off_TpLink_Device(self, gesture_sequence):
        index = 0
        while(index < len(self.commands)):
            for key in self.commands[index]:
                if(gesture_sequence == self.commands[index]['gesture_sequence']):
                    self.tp_Link_Devices.turn_on_off(self.commands[index]['command_text'])
                index += 1
