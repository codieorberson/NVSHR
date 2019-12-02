from pyHS100 import SmartPlug
from datetime import datetime
import time


class TPLinkDevice():
    def __init__(self):
        self.light_Plug = SmartPlug("192.168.43.236")
        time.sleep(1.2)
        self.fan_Plug = SmartPlug("192.168.43.37")

    def set_log_manager(self, log_manager, logger):
        self.log_manager = log_manager
        self.logger = logger

    def turn_on_off(self, device):
        if device == 'Lights':  # Change gesture sequence to default value
            if self.light_Plug.state == "OFF":
                self.light_Plug.turn_on()
            else:
                self.light_Plug.turn_off()
            self.log_manager.set_gesture_sequence_link("Lights", True, self.light_Plug.state.lower(), datetime.utcnow())
            self.logger.log_device_state_change("Lights", True, self.light_Plug.state.lower(), datetime.utcnow())

        elif device == 'Smart Plug':  # Change gesture sequence to default value
            if self.fan_Plug.state == "OFF":
                self.fan_Plug.turn_on()
            else:
                self.fan_Plug.turn_off()
            self.log_manager.set_gesture_sequence_link("Smart Plug", True, self.light_Plug.state.lower(),
                                                       datetime.utcnow())
            self.logger.log_device_state_change("Smart Plug", True, self.light_Plug.state.lower(), datetime.utcnow())

        else:
            self.log_manager.set_gesture_sequence_link(device, False, "off",
                                                       datetime.utcnow())
            self.logger.log_device_state_change(device, False, "off", datetime.utcnow())

    def check_status(self, smart_plug):
        return smart_plug.state
