import pywemo
import os, sys, time
import numpy as np
import matplotlib.pyplot as plt
import ouimeaux
import subprocess

devices = pywemo.discover_devices()
print(devices)

class Wemo():
    def __init__(self):
        self.status = False

    def setup(self):
        try:
            device=pywemo.discover_devices()
            print(devices)
        except:
            address = "192.168.100.193"
            port = pywemo.ouimeaux_device.probe_wemo(address)
            url = 'http://%s:%i/setup.xml' % (address, port)
            device = pywemo.discovery.device_from_description(url, None)
            print(device)

    def turn_on(self, device):
        if(self.status == False):
            os.system('wemo switch ' + device + ' on')
            self.status == True

    def turn_off(self, device):
        if(self.status == True):
            os.system('wemo switch ' + device + ' off')
            self.status == False

    def check_status(self, device):
        return self.status


