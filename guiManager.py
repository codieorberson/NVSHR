#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther, Justin Culbertson-Faegre, Danielle Bode
DETAILED DESCRIPTION:
    This file manages the administrator GUI. It is here that the GUI window is created and titled. It also creates an
    interface for setting the initial configuration values of the system as well as adding in callbacks for the changing
    of the various configurations. The GUI loop is also set and started here after all initial configurations have been
    set. The GUI Manager also calls the needed functions to create and maintain changes to the various tabs within the
    administrator GUI. It is also here that the GUI can be destroyed when the system terminates. More detailed
    information is available in section 3.2.2 in the SDD
REQUIREMENTS ADDRESSED:
    FR.5, FR.7, NFR.5, EIR.1
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

from guiWindow import GuiWindow
from framesPerSecondMeter import FramesPerSecondMeter
from tkinter import *

class GuiManager:
    def __init__(self, cap, settings_manager, is_admin, valid_webcam):
        self.cap = cap
        self.settings_manager = settings_manager
        self.gui = GuiWindow()
        self.gui.title("Non-Verbal Smart Home Recognition System")
        self.is_admin = is_admin
        self.valid_webcam = valid_webcam

    def check_configurations(self):
        if not self.is_admin:
            self.gui.withdraw()
        if not self.cap.isOpened():
            messagebox.showerror("Camera maufunction", "There is no camera connected or it is malfunctioning, please check it.")
            sys.exit()
        if not self.valid_webcam:
            messagebox.showwarning("Warning", "Your camera is not 720p. A camera of 720p or higher is "
                                              "recommended for optimal performance")

    def set_initial_ear(self, initial_value):
        self.gui.set_initial_ear(initial_value)

    def set_initial_minimum_time_increment(self, initial_value):
        self.gui.set_initial_minimum_time_increment(initial_value)

    def set_initial_maximum_time_increment(self, initial_value):
        self.gui.set_initial_maximum_time_increment(initial_value)

    def on_ear_change(self, callback):
        self.gui.on_ear_change(callback)
        
    def on_minimum_time_increment_change(self, callback):
        self.gui.on_minimum_time_increment_change(callback)

    def on_maximum_time_increment_change(self, callback):
        self.gui.on_maximum_time_increment_change(callback)

    def on_new_command(self, callback):
        self.gui.on_new_command(callback)

    def __loop__(self):
        self.loop_callback()
        self.fps_tab.set_fps(self.frames_per_second_meter.cycle())
        self.gui.after(1, self.__loop__)

    def start(self, loop_callback, close_callback):
        self.frames_per_second_meter = FramesPerSecondMeter()
        self.gui.set_cap(self.cap, self.settings_manager)
        self.debug_tab = self.gui.get_debug_tab()
        self.fps_tab = self.gui.get_fps_tab()
        self.blink_label = self.gui.get_blink_label()
        self.fist_label = self.gui.get_fist_label()
        self.palm_label = self.gui.get_palm_label()
   
        self.log_page = self.gui.get_log_page()

        self.loop_callback = loop_callback
        self.close_callback = close_callback
        self.gui.protocol("WM_DELETE_WINDOW", close_callback)
        self.check_configurations()
        self.gui.after(1, self.__loop__)
        self.gui.mainloop()

    def set_debug_frame(self, frame):
        self.debug_tab.set_debug_frame(frame)

    def display_error_message(self, title, text):
        self.gui.messagebox.showerror(title, text)

    def set_gesture_background(self, gesture_detected):
        self.blink_label.set_gesture_background(gesture_detected)
        self.fist_label.set_gesture_background(gesture_detected)
        self.palm_label.set_gesture_background(gesture_detected)

    def update_log_text(self, content):
        self.log_page.log_text.config(state=NORMAL)
        self.log_page.log_text.insert(INSERT, content)
        self.log_page.log_text.config(state=DISABLED)
        self.log_page.log_text.see(END)
    
    def destroy_gui(self):
        self.gui.destroy()
