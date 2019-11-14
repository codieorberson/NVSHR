from pyHS100 import SmartPlug # pip3 insrtall pyhs100
import time

class SmartPlugManager():
    def __init__(self):
        self.smart_plug_map = {}

    def turn_on_off(self, ip_address):
        self.__toggle_smart_plug__(self.__get_smart_plug__(ip_address))

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
