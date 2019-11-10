from pyHS100 import SmartPlug, SmartBulb
from pprint import pformat
import time

#Need to install pyHS100 library (pip install pyhs100)
class TPLinkDevice():
    def __init__(self):
        self.light_Plug = SmartPlug("192.168.1.197")
        time.sleep(1.2)
        self.fan_Plug = SmartPlug("192.168.1.198")

    def turn_on_off(self, gesture_sequence):
        if gesture_sequence == ['fist']: #Change gesture sequence to default value
            if self.light_Plug.state == "OFF":
                self.light_Plug.turn_on()
            else:
                self.light_Plug.turn_off()
        if gesture_sequence == ['fist','blink']: #Change gesture sequence to default value
            if self.fan_Plug.state == "OFF":
                self.fan_Plug.turn_on()
            else:
                self.fan_Plug.turn_off()

    def check_status(self):
        return self.plug.state