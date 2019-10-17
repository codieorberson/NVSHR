class SmartHomeActivator:
    def activate(self, smartHomeAction, device):
        print('"' + smartHomeAction + '" sent to ' + device + '.')
        #This needs to actually trigger the hass.io interface.