#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file creates an interface between the NVSHR system and the TPLink smart plugs. (The IP Addresses are hard coded
    within the system currently.) This module has the ability to check the status of the smart plug (whether it is on
    or off) and changes that state based on the command inputted by the user. If the current device is not 'Lights' or
    'Smart Plug' it simply logs the output to the console. More detail information can be found in Section 3.2.3 within
    the SDD.
REQUIREMENTS ADDRESSED:
    FR.5, FR.7, FR.10, FR.12
LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 4
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from pyHS100 import SmartPlug
from datetime import datetime
import time


class TPLinkDevice():
    def __init__(self):
        self.light_Plug = SmartPlug("192.168.43.236")
        time.sleep(1.2)
        self.fan_Plug = SmartPlug("192.168.43.37")
        self.logger = None
        self.log_manager = None

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

    @staticmethod
    def check_status(smart_plug):
        return smart_plug.state
