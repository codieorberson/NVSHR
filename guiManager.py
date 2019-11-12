from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
                    "format": "listbox"
                },
                {
                    "format": "logo"
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Welcome to the Non-Verbal Smart Home Recognition (NVSHR) System!",
                            "font": ("Helvetica", 14, "bold"),
                            "justify": "center"
                        }
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "The NVSHR system is a system created with the purpose of using "
                                    "non-verbal communication to control smart "
                                    "home devices with the help of hand gestures and blink detection. As a system "
                                    "administrator there are a few things that need to be initialized before the "
                                    "NVSHR system can be used properly. Please follow the steps below to ensure the "
                                    "user has the best"
                                    " experience using this system.",
                            "width": 100,
                            "height": 4,
                            "wraplength": 900,
                            "justify": "center",
                            "anchor": "w",
                            "font": ("Helevetica", 12, "italic")
                        }
                },
                {
                    "format": "text",
                    "body":
                    {
                        "text": "Before any commands are linked to a specific smart home action, the NVSHR system "
                                "will not "
                                "be able to make any state changes to the users smart home."
                                "However, it will be able to recognize these commands. \nTo link commands with smart "
                                "home actions:"
                                "\n\n"
                                "1. Navigate to the Command tab above."
                                "\n\n"
                                "2. Once in the Command tab, you will see a list of all available commands and their"
                                " descriptions (Please take note of the gesture sequence for each command). You are "
                                "also able to create new commands from this same tab. Instructions for creating these "
                                "new commands is housed within this tab."
                                "\n\n"
                                "3. Choose a smart home device from the drop down menu below each command to link that "
                                "device with the above command. If you do not wish to use a command, please choose the "
                                "None option from the drop down menu. Each smart home device is only able to linked to "
                                "one unique command, so be sure to chose command linking wisely."
                                "\n\n"
                                "Once each command you wish to use has been linked, navigate to the Debug tab above. "
                                "Within this tab "
                                "you will be able to view the live feedback from the connected camera as well as make "
                                "some changes to that feedback for better processing within the system."
                                "\n\n"
                                "1. Each of the sliders lets you configure the system to the right specifications. "
                                "The Eye Aspect Ratio (EAR) slider can be used to set the threshold for blink "
                                "detection. The Low and High Contrast sliders allow you to change the contrast on "
                                "the frame to improve the systems ability to recognize hand gestures if you aren't "
                                "getting the results you expect. You also able to set how long the system should "
                                "wait to register a command and what the shortest amount of time between unique "
                                "gestures should be."
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
                                "commands are being recognized properly as well.",
                        "width": 100,
                        "height": 34,
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
                },
                {
                    "format": "gestures",
                    "body": ["Current Gesture", "blink", "fist", "palm"]
                }
            ]
                 },
    "tab3": {"title": "Commands",
            "elements": [
                {
                    "format": "commands"
                },
                {
                    "format": "listbox"
                },
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
                                    "smart home action. To create a new command, fill out all the fields below "
                                    "and press the ADD button "
                                    "to add it to the list below. Commands may not have the one gesture followed "
                                    "immediately by that same gesture (i.e. FIST, FIST, BLINK is not a valid command). "
                                    "Once it is added, make sure it is linked to the "
                                    "correct smart home device.",
                            "width": 120,
                            "height": 4,
                            "wraplength": 900,
                            "justify": "center"
                        }
                },
                {
                    "format": "new"
                },
                {
                    "format": "field"
                },
                {
                    "format": "option"
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

    def set_initial_ear(self, initial_value):
        self.initial_ear = initial_value

    def set_initial_low_contrast(self, initial_value):
        self.initial_low_contrast = initial_value

    def set_initial_high_contrast(self, initial_value):
        self.initial_high_contrast = initial_value

    def set_initial_minimum_time_increment(self, initial_value):
        self.initial_minimum_time_increment = initial_value

    def set_initial_maximum_time_increment(self, initial_value):
        self.initial_maximum_time_increment = initial_value

    def on_ear_change(self, callback):
        self.on_ear_change = callback

    def on_low_contrast_change(self, callback):
        self.on_low_contrast_change = callback

    def on_high_contrast_change(self, callback):
        self.on_high_contrast_change = callback

    def on_minimum_time_increment_change(self, callback):
        self.on_minimum_time_increment_change = callback

    def on_maximum_time_increment_change(self, callback):
        self.on_maximum_time_increment_change = callback

    def on_new_command(self, callback):
        self.on_new_command_change = callback


    def set_cap(self, cap, settings_manager):
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.debug_tab = self.add_content(_gui_data, cap, 
                self.on_ear_change, self.initial_ear, 
                self.on_low_contrast_change, self.initial_low_contrast,
                self.on_high_contrast_change, self.initial_high_contrast,
                self.on_minimum_time_increment_change, self.initial_minimum_time_increment,
                self.on_maximum_time_increment_change, self.initial_maximum_time_increment,
                self.on_new_command_change, settings_manager)

        self.notebook.grid(row=0)

    def add_content(self, body, cap, on_ear_change, initial_ear,
                    on_low_contrast, initial_low_contrast,
                    on_high_contrast, initial_high_contrast,
                    on_min_time_inc, initial_min_time_inc,
                    on_max_time_inc, initial_max_time_inc,
                    on_new_command, settings_manager):

        for i in range(len(list(body.keys()))):
            page_configuration = body[list(body.keys())[i]]
            tab = Page(self.notebook, self, cap, 
                    on_ear_change, initial_ear, 
                    on_low_contrast, initial_low_contrast,
                    on_high_contrast, initial_high_contrast,
                    on_min_time_inc, initial_min_time_inc,
                    on_max_time_inc, initial_max_time_inc, 
                    on_new_command, page_configuration["elements"], 
                    settings_manager)

            self.notebook.add(tab, text=page_configuration["title"])

            if tab.is_debug:
                debug_tab = tab
            if tab.is_fps:
                self.fps_tab = tab
            if tab.is_fist_label:
                self.fist_label = tab
            if tab.is_palm_label:
                self.palm_label = tab
            if tab.is_blink_label:
                self.blink_label = tab
            if tab.is_command_field:
                self.command_field = tab

        return debug_tab

    def get_debug_tab(self):
        return self.debug_tab

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
    def __init__(self, name, window, cap, 
                on_ear_change, initial_ear, 
                on_low_contrast, initial_low_contrast,
                on_high_contrast, initial_high_contrast, 
                on_min_time_inc, initial_min_time_inc,
                on_max_time_inc, initial_max_time_inc, 
                on_new_command, elements, settings_manager, *args, **kwargs):

        self.event_map = {
            "on_ear_change": on_ear_change,
            "on_low_contrast": on_low_contrast,
            "on_high_contrast": on_high_contrast,
            "on_min_time_inc": on_min_time_inc,
            "on_max_time_inc": on_max_time_inc,
            "on_new_command": on_new_command
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
        self.is_command_field = False
        self.is_command_menu = False
        self.has_list_box = False
        self.gesture_detected = None
        self.current_command_map = {}

        self.command_manager = settings_manager
        self.option = 1
        self.command_index = 0
        self.is_full = 0

        self.command_links = {}
        self.new_command = {}

        self.row_index = 1
        for element in elements:
            if element["format"] == "text":
                column_index = 0
                body_index = list(element.keys()).index("body")
                for body in list(element.keys())[body_index:]:
                    if self.is_command_menu:
                        self.label = Label(self.command_listbox, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        self.name = name
                        column_index += 1
                    elif self.has_list_box:
                        self.label = Label(self.list_box, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=0)
                        self.name = name
                        column_index += 1
                    else:
                        self.label = Label(self, element.get(body))
                        self.label.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                        self.name = name
                        column_index += 1

            elif element["format"] == "logo":
                self.canvas = Canvas(self.list_box, width=100, height=66)
                self.canvas.grid(row=self.row_index, column=0, pady=10)
                image = PIL.ImageTk.PhotoImage(PIL.Image.open("NVSHRLogo.png"))
                self.canvas.create_image(100, 66, anchor="nw", image=image)

            elif element["format"] == "text-cam-status":
                text_var = StringVar()
                self.label = Label(self, textvariable=text_var, font=20)
                text_var.set("Camera On: " + str(cap.isOpened()))
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                self.name = name

            elif element["format"] == "text-cam-fps":
                self.fps_container = StringVar()
                self.label = Label(self, textvariable=self.fps_container, font=20)
                self.fps_container.set("FPS:       " + self.get_cam_fps(cap))
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                self.name = name
                self.is_fps = True

            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.debug_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.debug_canvas = Canvas(self, width=self.debug_width, height=self.debug_height)

                self.debug_canvas.grid(row=self.row_index, column=0, padx=10, pady=10, columnspan=5)
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
                    self.slider.grid(row=self.row_index, column=column_index, padx=10, pady=10)
                    self.name = name
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

            elif element["format"] == "button":
                self.log_button = Button(self, text = 'Click to see contents of the logfile', command = self.open_log_file).pack()
                self.delete_log_file()

            elif element["format"] == "commands":
                self.is_command_menu = True
 
            elif element["format"] == "listbox":
                if self.is_command_menu:
                    self.command_listbox = Listbox(self, bd=0, height=60, width=150)
                    self.command_listbox.grid(row=self.row_index, column=0, pady=10)
                else:
                    self.list_box = Listbox(self, bd=0, height=60, width=150)
                    self.list_box.grid(row=self.row_index, column=0, pady=10)
                    self.has_list_box = True

            elif element["format"] == "field":
                self.field = Entry(self.command_listbox)
                self.field.grid(row = self.row_index, column = 0)
                self.is_command_field = True

            elif element["format"] == "new":
                small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
                for x in range(1, 4):
                    self.gesture_list = ["fist", "palm", "blink"]
                    variable = StringVar()
                    variable.set(" ")
                    self.new_command[self.command_index] = variable
                    gesture = OptionMenu(small_frame, variable, *self.gesture_list, command=self.is_full_command)
                    gesture.grid(row=self.row_index, column=self.command_index, pady=10)
                    self.command_index += 1
                add_button = Button(small_frame, text="Add New Command", command=self.add_new_command)
                add_button.grid(row=self.row_index, column=self.command_index + 1, pady=10)

            elif element["format"] == "option":
                self.option_list = ["Alexa", "Smart Plug"]
                row = self.row_index
                 
                for option in self.command_manager.action:
                    small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                    small_frame.grid(row=row, column=0, padx=10, pady=10)
                    text = {"text": "Command " + str(self.option)}
                    self.label = Label(small_frame, text)
                    self.label.grid(row=row, column=0, padx=10, pady=10)
                    self.name = name
                    variable = StringVar()
                    variable.set(self.command_manager.action[self.option])
                    self.command_links[self.option] = variable
                    self.optionMenu = OptionMenu(small_frame, variable, *self.option_list, command=self.set_value)
                    self.optionMenu.grid(row=row, column=1, padx=10, pady=10, columnspan=100)
                    self.optionMenu.config(width=30)
                    self.option += 1
                    row += 1
                self.row_index = row

            self.row_index += 1

    def __bgr_to_rgb__(self, frame):
        return frame[..., [2, 1, 0]]

    def set_value(self, value):
        self.current_command_map["device_name"] = value
        self
        for x in range(1, 5):
            if value == self.command_manager.action[x] and value != "None":
                messagebox.showerror("Smart Home Device Linked", "This smart home device has already been linked to "
                                                                 "another command. Please chose a different device "
                                                                 "for this command.")
                return
        for x in range(1, 5):
            self.command_manager.write_to_file(x, self.command_links[x].get())

        self.event_map["on_new_command"](
                self.current_command_map['gesture_sequence'],
                self.current_command_map['command_text'],
                self.current_command_map['device_name']
                )

    def is_full_command(self, value):
        self.is_full += 1

    def add_new_command(self):

        if self.is_full >= 3:
            if self.new_command[0].get() != self.new_command[1].get() and self.new_command[1].get() != self.new_command[
                2].get():
                small_frame = LabelFrame(self.command_listbox, width=1000, height=100, bd=0)
                small_frame.grid(row=self.row_index, column=0, padx=10, pady=10)
                text = {"text": "Command " + str(self.option) + " (" + self.new_command[0].get() + ", " +
                                self.new_command[1].get() + ", " + self.new_command[2].get() + ")"}

                self.current_command_map["gesture_sequence"] = [
                        self.new_command[0].get(), 
                        self.new_command[1].get(), 
                        self.new_command[2].get()
                        ]
                self.current_command_map["command_text"] = self.field.get()
                self.label = Label(small_frame, text)
                self.label.grid(row=self.row_index, column=0, padx=10, pady=10)
                variable = StringVar()
                variable.set("None")
                self.command_links[self.option] = variable
                self.optionMenu = OptionMenu(small_frame, variable, *self.option_list, command=self.set_value)
                self.optionMenu.grid(row=self.row_index, column=1, padx=10, pady=10, columnspan=100)
                self.optionMenu.config(width=30)
                self.option += 1
                self.row_index += 1
            else:
                messagebox.showerror("Incorrect Command",
                                     "Commands may not have identical gestures in a successive order.")
        else:
            messagebox.showerror("No Command Created", "Please chose three gestures to create a full command.")

        self.is_full = 0

    def open_log_file(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 10)
        count =1
        file = open('logfile.txt')
        for line in file:
            pdf.cell(200, 10, txt = line, ln = count, align = "Left")
            count +=1
        file.close()
        pdf.output("logfile.pdf")
        subprocess.Popen(["logfile.pdf"], shell = True)
        
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
    def __init__(self, cap, settings_manager):
        self.cap = cap
        self.settings_manager = settings_manager
        self.gui = _App()
        self.gui.title("Non-Verbal Smart Home Recognition System")


    def set_initial_ear(self, initial_value):
        self.gui.set_initial_ear(initial_value)

    def set_initial_low_contrast(self, initial_value):
        self.gui.set_initial_low_contrast(initial_value)

    def set_initial_high_contrast(self, initial_value):
        self.gui.set_initial_high_contrast(initial_value)

    def set_initial_minimum_time_increment(self, initial_value):
        self.gui.set_initial_minimum_time_increment(initial_value)

    def set_initial_maximum_time_increment(self, initial_value):
        self.gui.set_initial_maximum_time_increment(initial_value)


    def on_ear_change(self, callback):
        self.gui.on_ear_change(callback)

    def on_low_contrast_change(self, callback):
        self.gui.on_low_contrast_change(callback)

    def on_high_contrast_change(self, callback):
        self.gui.on_high_contrast_change(callback)

    def on_minimum_time_increment_change(self, callback):
        self.gui.on_minimum_time_increment_change(callback)

    def on_maximum_time_increment_change(self, callback):
        self.gui.on_maximum_time_increment_change(callback)

    def on_new_command(self, callback):
        self.gui.on_new_command(callback)


    def __loop__(self):
        self.loop_callback()
        self.gui.after(1, self.__loop__)

    def start_background_process(self):
        self.gui.set_cap(self.cap, self.settings_manager)
        self.debug_tab = self.gui.get_debug_tab()
        self.fps_tab = self.gui.get_fps_tab()
        self.is_admin = False
        self.gui.withdraw()

    def start_foreground_process(self, loop_callback, close_callback):
        self.blink_label = self.gui.get_blink_label()
        self.fist_label = self.gui.get_fist_label()
        self.palm_label = self.gui.get_palm_label()
        self.is_admin = True
        self.gui.deiconify()
        self.loop_callback = loop_callback
        self.close_callback = close_callback
        self.gui.protocol("WM_DELETE_WINDOW", close_callback)
        self.gui.after(1, self.__loop__)
        self.gui.mainloop()

    def set_debug_frame(self, frame):
        self.debug_tab.set_debug_frame(frame)

    def set_gesture_background(self, gesture_detected):
        if self.is_admin:
            self.blink_label.set_gesture_background(gesture_detected)
            self.fist_label.set_gesture_background(gesture_detected)
            self.palm_label.set_gesture_background(gesture_detected)

    def set_fps(self, fps):
        self.fps_tab.set_fps(fps)

    def destroy_gui(self):
        self.gui.destroy()
