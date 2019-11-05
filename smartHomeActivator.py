import homeassistant

def _connect_to_home_assistant():
    1/0#Throw division by zero exception, since this isn't implemented yet.

class SmartHomeActivator():

    def __init__(self):
        try: 
            connection = _connection_to_home_assistant()
            print('hmm')
            self.is_connected = True
        except:
            print("Warning: NVSHR is not connected to a home assistant and" +
                    " commands issued during this session will not be" +
                    " activated.\n")
            self.is_connected = False

    def activate(self, smartHomeAction, device):
        if self.is_connected:
            print('"' + smartHomeAction + '" sent to ' + device + '.')
            #This needs to actually trigger the hass.io interface.
        else:
            print('"' + smartHomeAction + '" not actually sent to ' + device +
                    '.')
