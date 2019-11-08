import pywemo
import os
import ouimeaux
from smartHomeProcessManager import ProcessManager
import threading

class Wemo():
    def __init__(self):
        self.status = False
        self.process_manager = ProcessManager()

    def connect(self):
        try:
            device=pywemo.discover_devices()
            print(device)
        except:
            address = "192.168.1.195"  # Address for wemo is 10.22.22.1
            port = pywemo.ouimeaux_device.probe_wemo(address)  # Usually 49153
            print(port)
            url = 'http://%s:%i/setup.xml' % (address, port)
            device = pywemo.discovery.device_from_description(url, None)
            print(device)

    def turn_on(self, device):
        if(self.status == False):
            os.system('wemo switch ' + device + ' on')
            self.status = True

    def turn_off(self, device):
        if(self.status == True):
            os.system('wemo switch ' + device + ' off')
            self.status = False

    def turn_on_timer(self, device):
        self.process_manager.add_process(self.turn_on, device)
        self.process_manager.on_done()

    def turn_off_timer(self, device):
        self.process_manager.add_process(self.turn_off, device)
        self.process_manager.on_done()

    # Checking the speed at how fast the turn_on/turn_off functions will run
    def on_off_loop(self, device):
        i = 0
        while (i < 20):
            if self.status == False:
                self.turn_on(device)
                i = i+1
            else:
                self.turn_off(device)
                i = i+1

    def check_status(self, device):
        return self.status