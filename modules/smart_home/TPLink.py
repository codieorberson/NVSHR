from pyHS100 import SmartPlug
from speaker import Speaker
import time

#Need to install pyHS100 library (pip install pyhs100)
class TPLinkDevice():
    def __init__(self):
        self.speaker = Speaker()
        self.smart_plug_map = {}

    def turn_on_off(self, ip_address):
        try:
            self.__toggle_smart_plug__(self.__get_smart_plug__(ip_address))
        except:
            self.speaker.speak("Unable to communicate with Smart Plug at " + ip_address)

    def __get_smart_plug__(self, ip_address):
        if not ip_address in self.smart_plug_map:
            self.smart_plug_map[ip_address] = SmartPlug(ip_address)
            time.sleep(1.2)
        return self.smart_plug_map[ip_address]

    def __toggle_smart_plug__(self, smart_plug): 
        if smart_plug.state == "OFF":
            smart_plug.turn_on()
        else:
            smart_plug.turn_off()
