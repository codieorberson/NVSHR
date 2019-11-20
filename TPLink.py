from pyHS100 import SmartPlug
import time


class TPLinkDevice():
    def __init__(self):
        self.light_Plug = SmartPlug("192.168.1.197")
        time.sleep(1.2)
        self.fan_Plug = SmartPlug("192.168.1.198")

    def turn_on_off(self, device):
        if device == 'Lights':  # Change gesture sequence to default value
            if self.light_Plug.state == "OFF":
                self.light_Plug.turn_on()
            else:
                self.light_Plug.turn_off()
            print("Lights are now " + self.light_Plug.state.lower() + ".")

        elif device == 'Smart Plug':  # Change gesture sequence to default value
            if self.fan_Plug.state == "OFF":
                self.fan_Plug.turn_on()
            else:
                self.fan_Plug.turn_off()
            print("Smart Plug is now " + self.fan_Plug.state.lower() + ".")

        else:
            print(device + " is not linked to system. No state change will be observed.")

    def check_status(self, smart_plug):
        return smart_plug.state
