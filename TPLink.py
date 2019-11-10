from pyHS100 import SmartPlug, SmartBulb
from pprint import pformat

#Need to install pyHS100 library (pip install pyhs100)
class TPLinkDevice():
    def __init__(self, ipAddress):
        self.deviceIpAddress = ipAddress
        self.connect()

    def connect(self):
        self.plug = SmartPlug(self.deviceIpAddress)

    def turn_on(self):
        if self.plug.state == "OFF":
            self.plug.turn_on()

    def turn_off(self):
        if self.plug.state == "ON":
            self.plug.turn_off()

    def check_status(self):
        return self.plug.state