#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
import os

# Define the elements to be laid out on each tab
_gui_data = {
        "tab1": {"title": "Instructions",
            "elements": [
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Welcome to the Non-Verbal Smart Home Recognition (NVSHR) System!",
                            "font": ("Helvetica", 16, "bold"),
                            "justify": "center"
                        }
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "The NVSHR system is a system used to use non-verbal communication to control smart "
                                    "home devices with the help of hand gestures and blink detection. As a system "
                                    "administrator there are a few things that need to be initialized before the NVSHR syst"
                                    "em can be used properly. Please follow the steps below to ensure the user has the best"
                                    " experience using this system.",
                            "width": 100,
                            "height": 4,
                            "wraplength": 900,
                            "justify": "center",
                            "anchor": "w",
                            "font": ("Helevetica", 14, "italic")
                        }
                },
                {
                    "format": "text",
                    "body":
                    {
                        "text": "Before any commands are linked to a specific smart home action, the NVSHR system will "
                                "be able to recognize these commands, but will not illustrate any changes within the smart "
                                "home. To link commands with smart home actions:"
                                "\n\n"
                                "1. Navigate to the Command tab above."
                                "\n\n"
                                "2. Once in the Command tab, you will see a list of all available commands and their"
                                " descriptions. Please take note of the gesture sequence for each command."
                                "\n\n"
                                "3. Choose a smart home device from the drop down menu below each command to link that "
                                "device with the above command. If you do not wish to use a command, please choose the "
                                "None option from the drop down menu."
                                "\n\n"
                                "Once each command has been linked, navigate to the Debug tab above. Within this menu "
                                "you will be able to view the live feedback from the connected camera as well as make "
                                "some changes to that feedback for better processing within the system."
                                "\n\n"
                                "1. The Eye Aspect Ratio (EAR) slider can be used to set the threshold for blink detection."
                                "\n\n"
                                "2. The Frames Per Second (FPS) provides information about the number of frames being processed "
                                "within the system per second."
                                "\n\n"
                                "3. If the connected camera can be reached by the system, the Camera value will be set to true. "
                                "If there is no feedback or this value is false, the connected camera is not being used properly "
                                "by the system."
                                "\n\n"
                                "4. This page will also display the current gesture being processed. Please use this feature to "
                                "ensure all gestures can be recognized by the system. This tab can also be used to test the "
                                "previously linked commands."
                                "\n\n"
                                "Once all of the previous steps have been completed, the system will be ready for the user. "
                                "If at anytime the system is not properly recognizing commands, the Log tab can be used to "
                                "view previous gestures and commands. Feel free to use this tab to ensure that the linked "
                                "commands are being recognized properly.",
                        "width": 100,
                        "height": 30,
                        "wraplength": 800,
                        "justify": "left",
                        "anchor": "w",
                        "font": ("Helevetica", 12)
                    }
                },
                {
                    "format": "text",
                    "body":
                    {
                        "text": "Thank you for using the Non-Verbal Smart Home Recognition (NVSHR) System!",
                        "width": 100,
                        "height": 2,
                        "wraplength": 900,
                        "justify": "center",
                        "anchor": "center",
                        "font": ("Helevetica", 14, "italic")
                    }
                },
                {
                    "format": "text",
                    "body":
                    {
                        "text": "If there are any issues or bugs within the system please log a ticket "
                                "at: https://github.com/codieorberson/NVSHR/issues/new",
                        "width": 100,
                        "height": 3,
                        "wraplength": 900,
                        "justify": "center",
                        "anchor": "w",
                        "font": ("Helevetica", 10, "italic")
                    }
                }
            ]
        },
        "tab2": {"title": "Debug",
            "elements": [
                {
                    "format": "video"
                },
                {
                    "format": "text",
                    "multicolumn" : "true",
                    "body": {"text" : "Set the EAR:"},
                    "body2": {"text": "Set the Low Contrast:"},
                    "body3": {"text": "Set the High Contrast:"},
                    "body4": {"text": "Set the Minimum Time:"},
                    "body5": {"text": "Set the Maximum Time:"}
                },
                {
                    "format": "slider",

                    "events": ["on_ear_change", "on_low_contrast",
                               "on_high_contrast", "on_min_time_inc",  "on_max_time_inc"]

                },
                {
                    "format": "text-cam-status"
                },
                {
                    "format": "text-cam-fps",
                    # Note that FPS is only being
                    # calculated on initial
                    # execution, but we should
                    # really make a hook to update
                    # this value as the program
                    # executes because FPS will
                    # probably drop as we execute
                    # other code in between frame
                    # capture events:
                },
                {
                    "format": "gestures",
                    "body": ["Current Gesture", "Blink", "Fist", "Palm"]
                }
            ]
                 },
    "tab3": {"title": "Commands",
            "elements": [
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Menu",
                            "wraplength": 1000,
                            "justify": "center",
                            "font": ("Helvetica", 20, "bold")
                        }
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "The following commands have been created for initial use and are ready to be "
                                    "used within the system. Before you use them, please link them to the desired "
                                    "smart home action.",
                            "width": 120,
                            "height": 4,
                            "wraplength": 900,
                            "justify": "center"
                        }
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command One (Fist, Palm, Blink)",
                            "justify": "center"
                        }
                },
                {
                    "format": "option",
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Two (Palm, Fist, Blink)",
                            "justify": "center"
                        }
                },
                {
                    "format": "option",
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Three (Fist, Blink, Palm)",
                            "justify": "center"
                        }
                },
                {
                    "format": "option",
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Four (Palm, Blink, Fist)",
                            "justify": "center"
                        }
                },
                {
                    "format": "option",
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "To create a new command, fill out all the fields below and press the Add button "
                                    "to add it the list above. Once it is added, make sure to link it to a smart "
                                    "home device.",
                            "width": 120,
                            "height": 4,
                            "wraplength": 900,
                            "justify": "center"
                        }
                },
                {
                    "format": "new"
                }
            ]
        },
    "tab4": {"title": "Log",
             "elements": [
                 {
                     "format": "button",
                 }
             ]
             }
}


# An instance of this class represents a window with multiple tabs.
class _App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

    def set_cap_and_get_debug_tab(self, cap, on_ear_change, initial_ear,
                                  on_low_contrast, initial_low_contrast,
                                  on_high_contrast, initial_high_contrast,
                                  on_min_time_inc, initial_min_time_inc,
                                  on_max_time_inc, initial_max_time_inc,
                                  gesture_detected, settings_manager):
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.debug_tab = self.add_content(_gui_data, cap, on_ear_change, initial_ear, on_low_contrast,
                                          initial_low_contrast,
                                          on_high_contrast, initial_high_contrast,
                                          on_min_time_inc, initial_min_time_inc,
                                          on_max_time_inc, initial_max_time_inc,
                                          gesture_detected, settings_manager)

        self.notebook.grid(row=0)
        return self.debug_tab

    def add_content(self, body, cap, on_ear_change, initial_ear,
                    on_low_contrast, initial_low_contrast,
                    on_high_contrast, initial_high_contrast,
                    on_min_time_inc, initial_min_time_inc,
                    on_max_time_inc, initial_max_time_inc,
                    gesture_detected, settings_manager):
        for i in range(len(list(body.keys()))):
            page_configuration = body[list(body.keys())[i]]
            tab = Page(self.notebook, self, cap, on_ear_change, initial_ear, on_low_contrast, initial_low_contrast,
                       on_high_contrast, initial_high_contrast,
                       on_min_time_inc, initial_min_time_inc,
                       on_max_time_inc, initial_max_time_inc, gesture_detected, page_configuration["elements"],
                       settings_manager)
            self.notebook.add(tab, text=page_configuration["title"])
            if tab.is_debug:
                debug_tab = tab
            if tab.is_fps:
                self.fps_tab = tab
            if tab.is_blink_label:
                self.blink_label = tab
            if tab.is_fist_label:
                self.fist_label = tab
            if tab.is_palm_label:
                self.palm_label = tab

        return debug_tab

    def get_fps_tab(self):
        return self.fps_tab

    def get_blink_label(self):
        return self.blink_label

    def get_fist_label(self):
        return self.fist_label

    def get_palm_label(self):
        return self.palm_label

# An instance of this class represents a tab.
class Page(Frame):
    def __init__(self, name, window, cap, on_ear_change, initial_ear, on_low_contrast, initial_low_contrast,
                 on_high_contrast, initial_high_contrast, on_min_time_inc, initial_min_time_inc,
                 on_max_time_inc, initial_max_time_inc, gesture_detected, elements, settings_manager, *args, **kwargs):
        self.event_map = {
            "on_ear_change": on_ear_change,
            "on_low_contrast": on_low_contrast,
            "on_high_contrast": on_high_contrast,
            "on_min_time_inc": on_min_time_inc,
            "on_max_time_inc": on_max_time_inc
        }

        self.initial_value_map = {
            "on_ear_change": initial_ear,
            "on_low_contrast": initial_low_contrast,
            "on_high_contrast": initial_high_contrast,
            "on_min_time_inc": initial_min_time_inc,
            "on_max_time_inc": initial_max_time_inc
        }

        Frame.__init__(self, *args, **kwargs)
        self.is_debug = False
        self.is_fps = False
        self.is_blink_label = False
        self.is_fist_label = False
        self.is_palm_label = False
        self.gesture_detected = gesture_detected

        self.optionsManager = settings_manager
        self.option = 1
        self.command_index = 0

        self.command_links = {}
        self.new_command = {}

        row_index = 1
        for element in elements:
            if element["format"] == "text":
                column_index = 0
                body_index = list(element.keys()).index("body")
                for body in list(element.keys())[body_index:]:
                    self.label = Label(self, element.get(body))
                    self.label.grid(row=row_index, column=column_index, padx=10, pady=10)
                    self.name = name
                    column_index += 1

            elif element["format"] == "text-cam-status":
                text_var = StringVar()
                self.label = Label(self, textvariable=text_var, font=20)
                text_var.set("Camera On: " + str(cap.isOpened()))
                self.label.grid(row=row_index, column=0, padx=10, pady=10)
                self.name = name

            elif element["format"] == "text-cam-fps":
                self.fps_container = StringVar()
                self.label = Label(self, textvariable=self.fps_container, font=20)
                self.fps_container.set("FPS:       " + self.get_cam_fps(cap))
                self.label.grid(row=row_index, column=0, padx=10, pady=10)
                self.name = name
                self.is_fps = True

            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.debug_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.debug_canvas = Canvas(self, width=self.debug_width, height=self.debug_height)

                self.debug_canvas.grid(row=row_index, column=0, padx=10, pady=10, columnspan=5)
                self.name = name

            elif element["format"] == "slider":
                column_index = 0
                for event in element["events"]:
                    event_name = event
                    self.slider_command = self.event_map[event_name]
                    if event_name == "on_ear_change":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=10, command=self.slider_command)
                    elif event_name == "on_low_contrast" or event_name == "on_high_contrast":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=255, command=self.slider_command)
                    elif event_name == "on_min_time_inc" or "on_max_time_inc":
                        self.slider = Scale(self, orient='horizontal', from_=0, to=15, command=self.slider_command)

                    self.slider.set(self.initial_value_map[event_name])  # initial_ear * 100
                    self.slider.grid(row=row_index, column=column_index, padx=10, pady=10)
                    self.name = name
                    column_index += 1

            elif element["format"] == "gestures":
                self.gesturename = Label(self, text=element["body"][0], font=20, bg="White")
                self.gesturename.grid(row=row_index, column=0, padx=10, pady=10)

                self.is_blink_label = True
                self.blink_label = Label(self, text=element["body"][1], font=20, fg="Blue")
                self.blink_label.grid(row=row_index, column=1, padx=10, pady=10)

                self.is_fist_label = True
                self.fist_label = Label(self, text=element["body"][2], font=20, fg="Blue")
                self.fist_label.grid(row=row_index, column=2, padx=10, pady=10)

                self.is_palm_label = True
                self.palm_label = Label(self, text=element["body"][3], font=20, fg="Blue")
                self.palm_label.grid(row=row_index, column=3, padx=10, pady=10)

            elif element["format"] == "option":
                self.option_list = ["None", "Lights", "Smart Plug", "Heater", "Air Conditioning"]
                variable = StringVar()
                variable.set(self.optionsManager.action[self.option])
                self.command_links[self.option] = variable
                self.optionMenu = OptionMenu(self, variable, *self.option_list, command=self.set_value)
                self.optionMenu.grid(row=row_index, column=0, padx=10, pady=10, columnspan=100)
                self.optionMenu.config(width=30)
                self.option += 1

            elif element["format"] == "button":
                self.log_button = Button(self, text='Click to see contents of the logfile',
                                         command=self.open_log_file).pack()

            elif element["format"] == "new":
                small_frame = LabelFrame(self, width=1000, height=100, bd=0)
                small_frame.grid(row=row_index, column=0, padx=10, pady=10)
                for x in range(1, 4):
                    self.gesture_list = ["Fist", "Palm", "Blink"]
                    variable = StringVar()
                    variable.set("")
                    self.new_command[self.command_index] = variable
                    gesture = OptionMenu(small_frame, variable, *self.gesture_list)
                    gesture.grid(row=row_index, column=self.command_index, pady=10)
                    self.command_index += 1
                add_button = Button(small_frame, text="Add New Command", command=self.add_new_command)
                add_button.grid(row=row_index, column=self.command_index + 1, pady=10)

            row_index += 1

    def __bgr_to_rgb__(self, frame):
        return frame[..., [2, 1, 0]]

    def set_value(self, value):
        for x in range(1, 5):
            self.optionsManager.write_to_file(x, self.command_links[x].get())
            print("Command" + str(x) + ": " + self.command_links[x].get())

    def add_new_command(self):
        print("hey girl")

    def open_log_file(self):
        file = "notepad.exe logfile.txt"
        os.system(file)

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


class GuiManager():
    def __init__(self, cap, on_ear_change,
                 initial_ear, on_low_contrast, initial_low_contrast,
                 on_high_contrast, initial_high_contrast,
                 on_min_time_inc, initial_min_time_inc,
                 on_max_time_inc, initial_max_time_inc,
                 gesture_detected, is_admin, settings_manager):
        self.gui = _App()
        self.gui.title("Non-Verbal Smart Home Recognition System")
        self.debug_tab = self.gui.set_cap_and_get_debug_tab(cap, on_ear_change, initial_ear,
                                                            on_low_contrast, initial_low_contrast,
                                                            on_high_contrast, initial_high_contrast,
                                                            on_min_time_inc, initial_min_time_inc,
                                                            on_max_time_inc, initial_max_time_inc,
                                                            gesture_detected, settings_manager)
        self.fps_tab = self.gui.get_fps_tab()
        self.blink_label = self.gui.get_blink_label()
        self.fist_label = self.gui.get_fist_label()
        self.palm_label = self.gui.get_palm_label()

        if is_admin == False:
            self.gui.withdraw()

    def __loop__(self):
        self.loop_callback()
        self.gui.after(1, self.__loop__)

    def start(self, loop_callback, close_callback):
        self.loop_callback = loop_callback
        self.close_callback = close_callback
        self.gui.protocol("WM_DELETE_WINDOW", close_callback)
        self.gui.after(1, self.__loop__)
        self.gui.mainloop()

    def set_debug_frame(self, frame):
        self.debug_tab.set_debug_frame(frame)

    def set_gesture_background(self, gesture_detected):
        self.blink_label.set_gesture_background(gesture_detected)
        self.fist_label.set_gesture_background(gesture_detected)
        self.palm_label.set_gesture_background(gesture_detected)

    def set_fps(self, fps):
        self.fps_tab.set_fps(fps)

    def destroy_gui(self):
        self.gui.destroy()
