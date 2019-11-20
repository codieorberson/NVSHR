from TPLink import TPLinkDevice
from soundPlayer import SoundPlayer


class SmartHomeActivator():
    def __init__(self):
        self.sound_player = SoundPlayer()
        self.tp_Link_Devices = TPLinkDevice()

    def set_commands(self, commands):
        self.commands = commands

    def set_log_manager(self, log_manager, logger):
        self.log_manager = log_manager
        self.logger = logger
        self.tp_Link_Devices.set_log_manager(log_manager, logger)

    def activate(self, gesture_sequence, was_recognized):
        if was_recognized:
            try:
                self.sound_player.play_success_sound()
                self.turn_on_off_TpLink_Device(gesture_sequence)
            except:
                self.log_manager.set_gesture_sequence_error("Unable to connect command to requested smart home device.")
                self.logger.log("Unable to connect command to requested smart home device.")
        else:
            self.sound_player.play_failure_sound()

    # Iterating through the command dictionary and performing smart home action linked
    # with the given gesture sequence
    def turn_on_off_TpLink_Device(self, gesture_sequence):
        index = 0
        while(index < len(self.commands)):
            for key in self.commands[index]:
                if gesture_sequence == self.commands[index]['gesture_sequence']:
                    self.tp_Link_Devices.turn_on_off(self.commands[index]['command_text'])
                index += 1
