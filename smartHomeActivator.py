from TPLink import TPLinkDevice
from sound import Sound

class SmartHomeActivator():
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.tp_Link_Devices = TPLinkDevice()
        self.commands = self.database_manager.get_commands()

    def activate(self, gesture_sequence, was_recognized):
        if was_recognized:
            self.turn_On_Off_TpLink_Device(gesture_sequence)
            self.gesture_pattern_map[joined_gesture_sequence]()
            Sound.success()
        else:
            Sound.failure()

    #Iterating through the command dictionary and performing smart home action linked
    #with the given gesture sequence
    def turn_On_Off_TpLink_Device(self, gesture_sequence):
        index = 0
        while(index < len(self.commands)):
            for key in self.commands[index]:
                if(gesture_sequence == self.commands[index]['gesture_sequence']):
                    self.tp_Link_Devices.turn_on_off(self.commands[index]['command_text'])
                index += 1