#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Codie Orberson, Landan Ginther, Justin Culbertson-Faegre, Yutang Li
DETAILED DESCRIPTION:
    This file creates the needed content for each tab within the GUI. This file begins by loading all the needed data
    from gui_data and creating each individual item to be displayed on each tab (using the initial configuration values
    if needed) and sets all needed callbacks for buttons and option lists as well as sets the callbacks for various
    configuration changes. This file is where a majority of the error message calls live. Most of the error messages
    deal with the creation of new commands. This is also were the call for the GUI window to withdraw once the system is
    configured is housed. This file also creates functions for checking the new values of the configuration sliders
    and ensures there is not any errors made. The camera feedback is also displayed using this module. More detailed
    information is available in section 3.2.2 in the SDD
REQUIREMENTS ADDRESSED:
    FR.5, FR.7, FR.12, NFR.5, EIR.1
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

from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import cv2


class GuiTab(Frame):
    def __init__(self, name, window, database_manager, *args, **kwargs):
        self.event_map = {}
        self.initial_value_map = {}

        self.window = window

        Frame.__init__(self, *args, **kwargs)
        self.is_debug = False
        self.is_fps = False
        self.is_blink_label = False
        self.is_fist_label = False
        self.is_palm_label = False
        self.is_logfile = False
        self.is_command_menu = False
        self.has_list_box = False
        self.name = name

        self.database_manager = database_manager
        self.option = 1
        self.command_index = 0
        self.is_full = 0

        self.command_links = {}
        self.new_command = {}

    def set_initial_ear(self, initial_value):
        self.initial_value_map['on_ear_change'] = initial_value

    def set_initial_minimum_time_increment(self, initial_value):
        self.initial_value_map['on_min_time_inc'] = initial_value

    def set_initial_maximum_time_increment(self, initial_value):
        self.initial_value_map['on_max_time_inc'] = initial_value

    def set_cap(self, cap):
        self.cap = cap

    def on_ear_change(self, callback):
        self.event_map['on_ear_change'] = callback

    def on_minimum_time_increment_change(self, callback):
        self.event_map['on_min_time_inc'] = callback

    def on_maximum_time_increment_change(self, callback):
        self.event_map['on_max_time_inc'] = callback

    def on_new_command(self, callback):
        self.on_new_command_change = callback

    def update_mininum_time_increment(self, val):
        val = int(val)
        if self.minimum_time_slider.get() >= val:
            self.minimum_time_slider.set(val - 1)
            self.update_slider_command(self.minimum_time_slider.get(), val)
        else:
            self.update_slider_command(None, val)

    def update_maximum_time_increment(self, val):
        val = int(val)
        if self.maximum_time_slider.get() <= val:
            self.maximum_time_slider.set(val + 1)
            self.update_slider_command(val, self.maximum_time_slider.get())
        else:
            self.update_slider_command(val, None)

    def update_slider_command(self, min_time_value, max_time_value):
        self.min_time_inc_slider_command = self.event_map["on_min_time_inc"]
        self.max_time_inc_slider_command = self.event_map["on_max_time_inc"]
        if min_time_value == None:
            self.max_time_inc_slider_command(max_time_value)
        elif max_time_value == None:
            self.min_time_inc_slider_command(min_time_value)
        else:
            self.min_time_inc_slider_command(min_time_value)
            self.max_time_inc_slider_command(max_time_value)

    def load_data(self, tab_elements):
        self.row_index = 1

        for element in tab_elements:
            if element["format"] == "text":
                column_index = 0
                body_index = list(element.keys()).index("body")
                for body in list(element.keys())[body_index:]:
                    if self.is_command_menu:
                        self.label = Label(self.command_listbox, element.get(body), bg="White")
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        column_index += 1
                    elif self.has_list_box:
                        self.label = Label(self.list_box, element.get(body), bg="White")
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=0)
                        column_index += 1
                    else:
                        self.label = Label(self, element.get(body), bg="White")
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        column_index += 1

            elif element["format"] == "text-cam-status":
                text_var = StringVar()
                self.label = Label(self, textvariable=text_var, font=16, bg="White")
                text_var.set("Camera On: " + str(self.cap.isOpened()))
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)

            elif element["format"] == "text-cam-fps":
                self.fps_container = StringVar()
                self.label = Label(self, textvariable=self.fps_container, font=16, bg="White")
                try:
                    self.fps_container.set("FPS:       " + self.get_cam_fps(self.cap))
                except:
                    self.fps_container.set("FPS:       " + "0")
                    self.display_error_message("Camera maufunction", "There is no camera connected or it is malfunctioning, please check it.")
                    sys.exit()
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                self.is_fps = True

            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = 600
                self.debug_height = 400
                self.debug_canvas = Canvas(self, width=self.debug_width, height=self.debug_height)

                self.debug_canvas.grid(row=self.row_index, column=0, padx=10, pady=10, columnspan=5)

            elif element["format"] == "slider":
                column_index = 0
                for event in element["events"]:
                    event_name = event
                    self.slider_command = self.event_map[event_name]
                    if event_name == "on_ear_change":
                        self.ear_slider = Scale(self, orient='horizontal', from_=0, to=100, command=self.slider_command)
                        self.ear_slider.set(self.initial_value_map[event_name])  # initial_ear * 100
                        self.ear_slider.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                    elif event_name == "on_min_time_inc":
                        self.minimum_time_slider = Scale(self, orient='horizontal', from_=0, to=14, command=self.update_maximum_time_increment)
                        self.minimum_time_slider.set(self.initial_value_map[event_name])
                        self.minimum_time_slider.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                    elif event_name == "on_max_time_inc":
                        self.maximum_time_slider = Scale(self, orient='horizontal', from_=1, to=15, command=self.update_mininum_time_increment)
                        self.maximum_time_slider.set(self.initial_value_map[event_name])
                        self.maximum_time_slider.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                    
                    column_index += 1

            elif element["format"] == "gestures":
                self.gesturename = Label(self, text=element["body"][0], font=16, bg="White")
                self.gesturename.grid(row=self.row_index, column=0, padx=10, pady=10)

                self.is_blink_label = True
                self.blink_label = Label(self, text=element["body"][1], font=16, fg="Blue")
                self.blink_label.grid(row=self.row_index, column=1, padx=10, pady=10)

                self.is_fist_label = True
                self.fist_label = Label(self, text=element["body"][2], font=16, fg="Blue")
                self.fist_label.grid(row=self.row_index, column=2, padx=10, pady=10)

                self.is_palm_label = True
                self.palm_label = Label(self, text=element["body"][3], font=16, fg="Blue")
                self.palm_label.grid(row=self.row_index, column=3, padx=10, pady=10)

            elif element["format"] == "commands":
                self.is_command_menu = True

            elif element["format"] == "option":
                self.option_list = ["None", "Lights", "Smart Plug", "Heater", "Air Conditioning", "Fan"]
                for option in self.database_manager.get_commands():
                    self.add_device_list_to_gui(option["gesture_sequence"][0], option["gesture_sequence"][1],
                                                option["gesture_sequence"][2], option["command_text"])

            elif element["format"] == "new":
                small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0, bg="White")
                small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
                for x in range(1, 4):
                    self.gesture_list = ["None", "Fist", "Palm", "Blink"]
                    variable = StringVar()
                    variable.set("None")
                    self.new_command[self.command_index] = variable
                    gesture = OptionMenu(small_frame, variable, *self.gesture_list,command=self.is_full_command)
                    gesture.grid(row=self.row_index, column=self.command_index, pady=10)
                    self.command_index += 1
                add_button = Button(small_frame, text="Add New Command", command=self.add_new_command, bg="White")
                add_button.grid(row=self.row_index, column=self.command_index + 1, pady=10)

            elif element["format"] == "logfile":
                self.is_logfile = True
                self.scroll = Scrollbar(self)
                self.scroll.grid(row=self.row_index, column=1, sticky=N + E + S + W)
                self.log_text = Text(self, font=16, height=30, width=60, yscrollcommand=self.scroll.set)
                with open("./log.csv") as logfile:
                    content = logfile.readlines()
                    for line in content:
                        self.log_text.insert(INSERT, line)
                self.log_text.config(state=DISABLED)
                self.log_text.grid(row=self.row_index, column=0, padx=10, pady=10)
                self.log_text.see(END)
                self.scroll.config(command=self.log_text.yview)

            elif element["format"] == "listbox":
                if self.is_command_menu:
                    self.command_listbox = Listbox(self, bd=0, height=60, width=150)
                    self.command_listbox.grid(row=self.row_index, column=0, pady=10)
                else:
                    self.list_box = Listbox(self, bd=0, height=60, width=150)
                    self.list_box.grid(row=self.row_index, column=0, pady=10)
                    self.has_list_box = True

            elif element["format"] == "close_gui_button":
                self.close_button = Button(self.list_box, text="Close Administrator Window",
                                           command=self.close_gui_window)
                self.close_button.grid(row=self.row_index, column=0)

            self.row_index += 1

    def __bgr_to_rgb__(self, frame):
        return frame[..., [2, 1, 0]]

    def add_device_list_to_gui(self, gesture1, gesture2, gesture3, command):
        small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0, bg="White")
        small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
        text = {"text": "Command " + str(self.option) + " (" + gesture1.capitalize() + ", " +
                        gesture2.capitalize() + ", " + gesture3.capitalize() + ")"}
        self.label = Label(small_frame, text, bg="White")
        self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
        variable = StringVar()
        variable.set(command)
        self.command_links[self.option] = variable
        self.optionMenu = OptionMenu(small_frame, variable, *self.option_list, command=self.set_value)
        self.optionMenu.grid(row=self.row_index, column=1, padx=10, pady=10, columnspan=100)
        self.optionMenu.config(width=30)
        self.option += 1
        self.row_index += 1

    def set_value(self, value):
        for option in self.database_manager.get_commands():
            if value == option["command_text"] and value != "None":
                self.display_error_message("Smart Home Device Linked",
                                           "This smart home device has already been linked to "
                                                                 "another command. Please chose a different device "
                                                                 "for this command.")
                return

        count = 1
        for option in self.database_manager.get_commands():
            device = None

            if self.command_links[count].get() == "Heater" or self.command_links[count].get() == "Air Conditioning":
                device = "Nest"
            else:
                device = "Alexa"

            self.database_manager.set_command([option["gesture_sequence"][0], option["gesture_sequence"][1],
                                               option["gesture_sequence"][2]], self.command_links[count].get(), device)
            count += 1

    def is_full_command(self, value):
        if value != "None":
            self.is_full += 1

    def add_new_command(self):
        does_not_exist = self.check_new_command()
        if self.option > 8:
            self.display_error_message("Command Maximum Reached", "The system can only house 8 commands. "
                                                                  "You have reached the maximum allowed commands.")
            return

        if self.is_full >= 3:
            if does_not_exist:
                if self.new_command[0].get() != self.new_command[1].get() and self.new_command[1].get() != \
                        self.new_command[2].get():
                    self.add_device_list_to_gui(self.new_command[0].get(), self.new_command[1].get(),
                                                self.new_command[2].get(), "None")
                    self.database_manager.set_command(
                        [self.new_command[0].get().lower(), self.new_command[1].get().lower(),
                         self.new_command[2].get().lower()], "None", "None")
                else:
                    self.display_error_message("Incorrect Command",
                                               "Commands may not have identical gestures in a successive order.")
        else:
            self.display_error_message("No Command Created", "Please chose three gestures to create a full command.")

        self.is_full = 0

    def check_new_command(self):
        is_not_equal = True
        for option in self.database_manager.get_commands():
            if "".join(option["gesture_sequence"]) == "".join((self.new_command[0].get().lower(),
                                                               self.new_command[1].get().lower(),
                                                               self.new_command[2].get().lower())):
                is_not_equal = False

        if not is_not_equal:
            self.display_error_message("Command Exists", "This command is already created "
                                                         "within the system. Please create a new, unique command.")

        return is_not_equal

    def set_fps(self, fps):
        self.fps_container.set("FPS:       " + str(fps))

    def __frame_to_image__(self, frame):
        return PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    def __display_image__(self, image):
        self.image = image
        self.debug_canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

    def set_debug_frame(self, frame):
        self.__display_image__(self.__frame_to_image__(self.__bgr_to_rgb__(frame)))

    def get_cam_fps(self, cap):
        while cap.isOpened():
            return str(cap.get(cv2.CAP_PROP_FPS))

    def display_error_message(self, title, text):
        messagebox.showerror(title, text)

    # This code, as written, cannot display two simultaneous gestures.
    def set_gesture_background(self, gesture_detected):
        if gesture_detected == "fist":
            self.fist_label.configure(bg="Black")
            self.palm_label.configure(bg="White")
            self.blink_label.configure(bg="White")
        elif gesture_detected == "palm":
            self.palm_label.configure(bg="Black")
            self.fist_label.configure(bg="White")
            self.blink_label.configure(bg="White")
        elif gesture_detected == "blink":
            self.blink_label.configure(bg="Black")
            self.fist_label.configure(bg="White")
            self.palm_label.configure(bg="White")
        else:
            self.fist_label.configure(bg="White")
            self.palm_label.configure(bg="White")
            self.blink_label.configure(bg="White")

    def close_gui_window(self):
        self.window.withdraw_gui()
