#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther, Justin Culbertson-Faegre
DETAILED DESCRIPTION:
    This file creates an interface between the NVSHR system and the TPLink devices. This is where the system actually
    determines if the device is physically connected to the device and outputs a warning/message to the console in
    to inform the user no state change will be observed. This is also where the confirmation and failure noises will be
    called. More detail information can be found in Section 3.2.3 within the SDD.
REQUIREMENTS ADDRESSED:
    FR.5, FR.7, FR.10, FR.12, EIR.3
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

from TPLink import TPLinkDevice
from soundPlayer import SoundPlayer


class SmartHomeActivator:
    def __init__(self):
        self.sound_player = SoundPlayer()
        self.tp_Link_Devices = TPLinkDevice()

    def set_commands(self, commands):
        self.commands = commands

    def set_log_manager(self, log_manager, logger):
        self.log_manager = log_manager
        self.logger = logger
        self.tp_Link_Devices.set_log_manager(log_manager, logger)

    def activate(self, gesture_sequence, was_recognized):
        if was_recognized:
            try:
                Sound.success()
                self.turn_on_off_TpLink_Device(gesture_sequence)
            except:
                self.log_manager.set_gesture_sequence_error("Unable to connect command to requested smart home device.")
                self.logger.log("Unable to connect command to requested smart home device.")
        else:
            self.sound_player.play_failure_sound()

    # Iterating through the command dictionary and performing smart home action linked
    # with the given gesture sequence
    def turn_on_off_TpLink_Device(self, gesture_sequence):
        index = 0
        while index < len(self.commands):
            for key in self.commands[index]:
                if gesture_sequence == self.commands[index]['gesture_sequence']:
                    self.tp_Link_Devices.turn_on_off(self.commands[index]['command_text'])
                index += 1
