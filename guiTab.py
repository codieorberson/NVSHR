from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import cv2
import os
import subprocess
from fpdf import FPDF

class GuiTab(Frame):
    def __init__(self, name, window, *args, **kwargs):
        self.event_map = {}
        self.initial_value_map = {}

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

        self.option = 1
        self.command_index = 0
        self.is_full = 0

        self.command_links = {}
        self.new_command = {}

    def set_initial_ear(self, initial_value):
        self.initial_value_map['on_ear_change'] = initial_value

    def set_initial_low_contrast(self, initial_value):
        self.initial_value_map['on_low_contrast'] = initial_value

    def set_initial_high_contrast(self, initial_value):
        self.initial_value_map['on_high_contrast'] = initial_value

    def set_initial_minimum_time_increment(self, initial_value):
        self.initial_value_map['on_min_time_inc'] = initial_value

    def set_initial_maximum_time_increment(self, initial_value):
        self.initial_value_map['on_max_time_inc'] = initial_value

    def set_initial_log(self, logged_lines):
        self.initial_value_map['logged_lines'] = logged_lines
        
    def set_initial_commands(self, commands):
        self.initial_value_map['initial_commands'] = commands

    def set_cap(self, cap):
        self.cap = cap

    def on_ear_change(self, callback):
        self.event_map['on_ear_change'] = callback

    def on_low_contrast_change(self, callback):
        self.event_map['on_low_contrast'] = callback

    def on_high_contrast_change(self, callback):
        self.event_map['on_high_contrast'] = callback

    def on_minimum_time_increment_change(self, callback):
        self.event_map['on_min_time_inc'] = callback

    def on_maximum_time_increment_change(self, callback):
        self.event_map['on_max_time_inc'] = callback

    def on_new_command(self, callback):
        self.event_map['on_new_command'] = callback

    def load_data(self, tab_elements):
        self.row_index = 1

        for element in tab_elements:
            if element["format"] == "text":
                column_index = 0
                body_index = list(element.keys()).index("body")
                for body in list(element.keys())[body_index:]:
                    if self.is_command_menu:
                        self.label = Label(self.command_listbox, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        column_index += 1
                    elif self.has_list_box:
                        self.label = Label(self.list_box, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=0)
                        column_index += 1
                    else:
                        self.label = Label(self, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        column_index += 1

            elif element["format"] == "text-cam-status":
                text_var = StringVar()
                self.label = Label(self, textvariable=text_var, font=20)
                if self.cap.isOpened == False:
                    messagebox.showerror("No Camera Connected", "The system cannot recognize the connected "
                                                                "camera and is not taking in any data. Please "
                                                                "ensure your camera is connected properly.")
                text_var.set("Camera On: " + str(self.cap.isOpened()))
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)

            elif element["format"] == "text-cam-fps":
                self.fps_container = StringVar()
                self.label = Label(self, textvariable=self.fps_container, font=20)
                self.fps_container.set("FPS:       " + self.get_cam_fps(self.cap))
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                self.is_fps = True

            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.debug_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.debug_canvas = Canvas(self, width=self.debug_width, height=self.debug_height)

                self.debug_canvas.grid(row=self.row_index, column=0, padx=10, pady=10, columnspan=5)

            elif element["format"] == "slider":
                column_index = 0
                for event in element["events"]:
                    event_name = event
                    self.slider_command = self.event_map[event_name]
                    if event_name == "on_ear_change":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=100, command=self.slider_command)
                    elif event_name == "on_low_contrast" or event_name == "on_high_contrast":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=255, command=self.slider_command)
                    elif event_name == "on_min_time_inc" or "on_max_time_inc":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=15, command=self.slider_command)

                    self.slider.set(self.initial_value_map[event_name])  # initial_ear * 100
                    self.slider.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                    column_index += 1

            elif element["format"] == "gestures":
                self.gesturename = Label(self, text=element["body"][0], font=20, bg="White")
                self.gesturename.grid(row=self.row_index, column=0, padx=10, pady=10)

                self.is_blink_label = True
                self.blink_label = Label(self, text=element["body"][1], font=20, fg="Blue")
                self.blink_label.grid(row=self.row_index, column=1, padx=10, pady=10)

                self.is_fist_label = True
                self.fist_label = Label(self, text=element["body"][2], font=20, fg="Blue")
                self.fist_label.grid(row=self.row_index, column=2, padx=10, pady=10)

                self.is_palm_label = True
                self.palm_label = Label(self, text=element["body"][3], font=20, fg="Blue")
                self.palm_label.grid(row=self.row_index, column=3, padx=10, pady=10)

            elif element["format"] == "commands":
                self.is_command_menu = True

            elif element["format"] == "option":
                self.option_list = ["None", "Lights", "Smart Plug", "Heater", "Air Conditioning", "Fan"]
                row = self.row_index
                for option in self.initial_value_map['initial_commands']:
                    small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                    small_frame.grid(row=row, column=0, padx=10, pady=10)
                    text = {"text": "Command " + str(self.option) + " (" + option["gesture_sequence"][
                        0].capitalize() + ", " +
                                    option["gesture_sequence"][1].capitalize() + ", " + option["gesture_sequence"][
                                        2].capitalize() + ")"}
                    self.label = Label(small_frame, text)
                    self.label.grid(row=row, column=0, padx=10, pady=10)
                    variable = StringVar()
                    variable.set(option["command_text"])
                    self.command_links[self.option] = variable
                    self.optionMenu = OptionMenu(small_frame, self.command_links[self.option], *self.option_list,
                                                 command=self.set_value)
                    self.optionMenu.grid(row=row, column=1, padx=10, pady=10, columnspan=100)
                    self.optionMenu.config(width=30)
                    self.option += 1
                    row += 1
                self.row_index = row

            elif element["format"] == "new":
                small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
                for x in range(1, 4):
                    self.gesture_list = ["Fist", "Palm", "Blink"]
                    variable = StringVar()
                    variable.set(" ")
                    self.new_command[self.command_index] = variable
                    gesture = OptionMenu(small_frame, variable, *self.gesture_list, command=self.is_full_command)
                    gesture.grid(row=self.row_index, column=self.command_index, pady=10)
                    self.command_index += 1
                add_button = Button(small_frame, text="Add New Command", command=self.add_new_command)
                add_button.grid(row=self.row_index, column=self.command_index + 1, pady=10)

            elif element["format"] == "logfile":
                self.is_logfile = True
                self.scro = Scrollbar(self)
                self.scro.grid(row = self.row_index, column = 1, sticky=N+E+S+W)
                self.log_text = Text(self, font = 20, height = 30, width = 60, yscrollcommand = self.scro.set)
              
                for line in self.initial_value_map['logged_lines']:
                    self.log_text.insert(INSERT,line)
                self.log_text.config(state = DISABLED)
                self.log_text.grid(row=self.row_index, column = 0, padx = 10, pady = 10)
                self.scro.set(0, 0)
                self.scro.config(command = self.log_text.yview)

            elif element["format"] == "listbox":
                if self.is_command_menu:
                    self.command_listbox = Listbox(self, bd=0, height=60, width=150)
                    self.command_listbox.grid(row=self.row_index, column=0, pady=10)
                else:
                    self.list_box = Listbox(self, bd=0, height=60, width=150)
                    self.list_box.grid(row=self.row_index, column=0, pady=10)
                    self.has_list_box = True

            elif element["format"] == "logo":
                self.canvas = Canvas(self.list_box, width=100, height=66)
                self.canvas.grid(row=self.row_index, column=0, pady=10)
                image = PIL.ImageTk.PhotoImage(PIL.Image.open("NVSHRLogo.png"))
                self.canvas.create_image(100, 66, anchor="nw", image=image)

            self.row_index += 1

    def __bgr_to_rgb__(self, frame):
        return frame[..., [2, 1, 0]]

    def set_value(self, value):
        for option in self.initial_value_map['initial_commands']:
            if value == option["command_text"] and value != "None":
                messagebox.showerror("Smart Home Device Linked", "This smart home device has already been linked to "
                                                                 "another command. Please chose a different device "
                                                                 "for this command.")
                return

        count = 1
        for option in self.initial_value_map['initial_commands']:
            device = None

            if self.command_links[count].get() == "Heater" or self.command_links[count].get() == "Air Conditioning":
                device = "Nest"
            else:
                device = "Alexa"

            self.event_map['on_new_command']([option["gesture_sequence"][0], 
                    option["gesture_sequence"][1],
                    option["gesture_sequence"][2]], 
                    self.command_links[count].get(), 
                    device)

            count += 1

    def is_full_command(self, value):
        self.is_full += 1

    def add_new_command(self):
        if self.is_full >= 3:
            if self.new_command[0].get() != self.new_command[1].get() and self.new_command[1].get() != \
                    self.new_command[2].get():
                small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
                text = {"text": "Command " + str(self.option) + " (" + self.new_command[0].get().capitalize() + ", " +
                                self.new_command[1].get().capitalize() + ", " + self.new_command[
                                    2].get().capitalize() + ")"}
                self.label = Label(small_frame, text)
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                variable = StringVar()
                variable.set("None")
                self.command_links[self.option] = variable
                self.optionMenu = OptionMenu(small_frame, variable, *self.option_list, command=self.set_value)
                self.optionMenu.grid(row=self.row_index, column=1, padx=10, pady=10, columnspan=100)
                self.optionMenu.config(width=30)
                self.event_map['on_new_command']([self.new_command[0].get().lower(), 
                        self.new_command[1].get().lower(), 
                        self.new_command[2].get().lower()], 
                        "None", 
                        "None")

                self.option += 1
                self.row_index += 1
            else:
                messagebox.showerror("Incorrect Command",
                                     "Commands may not have identical gestures in a successive order.")
        else:
            messagebox.showerror("No Command Created", "Please chose three gestures to create a full command.")

        self.is_full = 0

    def open_log_file(self):
        if os.path.exists("logfile.pdf"):
            self.delete_log_file()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 10)
        count =1
        file = open('logfile.txt')
        for line in file:
            pdf.cell(200, 10, txt=line, ln=count, align="Left")
            count +=1
        file.close()
        pdf.output("logfile.pdf")
        subprocess.call(["open", "logfile.pdf"])

    def delete_log_file(self):
        if os.path.exists("logfile.pdf"):
            os.remove("logfile.pdf")

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

    # This code, as written, cannot display two simultaneous gestures.
    def set_gesture_background(self, gestures_detected):
        self.fist_label.configure(bg="White")
        self.palm_label.configure(bg="White")
        self.blink_label.configure(bg="White")
 
        for gesture_detected in gestures_detected:
            if gesture_detected == "fist":
                self.fist_label.configure(bg="Black")
            elif gesture_detected == "palm":
                self.palm_label.configure(bg="Black")
            elif gesture_detected == "blink":
                self.blink_label.configure(bg="Black")