#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

#This data structure defines the elements which are to be laid out on the 
#screen. The logic of the layout is implemented below. I think this data
#structure probably deserves a separate file, but crudely dumping it here was
#quick and easy. Feel free to move it.
_gui_data = {
        "tab1": {"title": "Instructions",
            "elements": [
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Welcome to the Non-Verbal Smart Home Recgonition (NVSHR) System!",
                            "font": ("Helvetica", 25, "bold"),
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
                            "justify": "center"
                        }
                }
            ]
        },
        "tab2": {"title": "Debug",
            "elements": [
                {
                    "format": "text",
                    "body": {"text": "Camera on: " + str(cv2.VideoCapture(0).isOpened()),
                             "font": "20",
                             "justify": "left"}
                },
                {
                    "format": "text",
                                                  #Note that FPS is only being 
                                                  #calculated on initial 
                                                  #execution, but we should 
                                                  #really make a hook to update
                                                  #this value as the program 
                                                  #executes because FPS will
                                                  #probably drop as we execute
                                                  #other code in between frame
                                                  #capture events:
                    "body": {"text": "FPS: " + str(cv2.VideoCapture(0).get(cv2.CAP_PROP_FPS)),
                             "font": "20",
                             "justify": "left"}
                },
                {
                    "format": "text",
                    "body": {"text": "Current Gesture: " + "Want to show current gesture being detected here",
                             "font": "20"}
                },
                {
                    "format": "video"
                },
                {
                    "format": "text",
                    "body": {"text" : "Set the EAR:"}
                },
                {
                    "format": "slider",
                    "event_name": "on_ear_change"
                
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
                            "font": ("Helvetica", 30, "bold")
                        }
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "The following commands can be used to control smart home devices using the NVSHR system"
                                    ". Please make sure to link the commands with the various devices connected to the system.",
                            "width": 100,
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
                            "justify": "left"
                        }
                },
                {
                    "format": "option",
                    "option1": "None",
                    "option2": "Lights",
                    "option3": "Smart Plug",
                    "option4": "Heater",
                    "option5": "Air Conditioning"
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Two (Palm, Fist, Blink)",
                            "justify": "left"
                        }
                },
                {
                    "format": "option",
                    "option1": "None",
                    "option2": "Lights",
                    "option3": "Smart Plug",
                    "option4": "Heater",
                    "option5": "Air Conditioning"
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Three (Fist, Blink, Palm)",
                            "justify": "left"
                        }
                },
                {
                    "format": "option",
                    "option1": "None",
                    "option2": "Lights",
                    "option3": "Smart Plug",
                    "option4": "Heater",
                    "option5": "Air Conditioning"
                },
                {
                    "format": "text",
                    "body":
                        {
                            "text": "Command Four (Palm, Blink, Fist)",
                            "justify": "left"
                        }
                },
                {
                    "format": "option",
                    "option1": "None",
                    "option2": "Lights",
                    "option3": "Smart Plug",
                    "option4": "Heater",
                    "option5": "Air Conditioning"
                }
            ]
        },
        "tab4": {"title": "Log",
            "elements": [
                {
                    "format": "text",
                    "body": {"text" : "To view the log, open logfile.txt in a text editor."}
                },
                {
                    "format": "text",
                    "body": {"text" : "We should really display it in the GUI, though."}
                }
            ]
        }      
}

#An instance of this class represents a window with (potentially) multiple tabs.
class _App(Tk):
    def __init__(self, *args,**kwargs):
        Tk.__init__(self,*args,**kwargs)

    def set_cap_and_get_debug_tab(self, cap, on_ear_change, initial_ear):
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.notebook.pack(expand=True)
        self.debug_tab = self.add_content(_gui_data, cap, on_ear_change, initial_ear)
        self.notebook.grid(row=0)
        return self.debug_tab

    def add_content(self, body, cap, on_ear_change, initial_ear):
        for i in range(len(list(body.keys()))):
            page_configuration = body[list(body.keys())[i]]
            tab = Page(self.notebook, self, cap, on_ear_change, initial_ear, page_configuration["elements"])
            self.notebook.add(tab, text=page_configuration["title"])
            if tab.is_debug:
                debug_tab = tab

        return debug_tab

#An instance of this class represents a tab.
#Note that the current version only has one tab, due to the canvas element
#showing up on every tab.
class Page(Frame):
    def __init__(self, name, window, cap, on_ear_change, initial_ear, elements, *args,**kwargs):

        self.event_map = {
                "on_ear_change" : on_ear_change
                }

        Frame.__init__(self,*args,**kwargs)
        self.is_debug = False
        row_index = 1
        for element in elements:
            if element["format"] == "text":
                self.label = Label(self, element["body"])
                self.label.grid(row=row_index, column=0, padx=10, pady=10)
                self.name = name
            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.debug_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.debug_canvas = Canvas(self, width = self.debug_width, height = self.debug_height)
                self.debug_canvas.grid(row = row_index, column = 0, padx = 10, pady = 10)
                self.name = name
            elif element["format"] == "slider":
                event_name = element["event_name"]
                self.slider_command = self.event_map[event_name]
                self.slider = Scale(self, orient='horizontal', from_=0, to=100, command=self.slider_command)
                self.slider.set(initial_ear * 100)
                self.slider.grid(row = row_index, column = 0, padx = 10, pady = 10)
                self.name = name
            elif element["format"] == "option":
                OPTIONLIST = [element["option1"], element["option2"], element["option3"], element["option4"],
                              element["option5"]]
                self.option = StringVar()
                self.option.set(element["option1"])
                self.optionMenu = OptionMenu(self, self.option, *OPTIONLIST, command=self.set_value)
                self.optionMenu.pack()
                self.optionMenu.grid(row=row_index, column=0, padx=10, pady=10, columnspan=100)
                self.optionMenu.config(width=30)
                
            row_index += 1

    def __bgr_to_rgb__(self, frame):
        return frame[..., [2, 1, 0]]

    def set_value(self, value):
        self.option.set(value)
        print(value)

    def __frame_to_image__(self, frame):
        return PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

    def __display_image__(self, image):
        self.image = image
        self.debug_canvas.create_image(0, 0, image = self.image, anchor = tkinter.NW)
           
    def set_debug_frame(self, frame):
        self.__display_image__(self.__frame_to_image__(self.__bgr_to_rgb__(frame)))

#This is the only class which is meant to be accessed from other files. It 
#provides a high level interface for starting the gui, defining what logic
#should be executed between refresh cycles and before closing down, and moving
#data to and from the GUI (e.g. when drawing a new frame for the debug screen).
class GuiManager():
    def __init__(self, cap, on_ear_change, initial_ear):
        self.gui = _App()
        self.gui.title("NVSHR")
        self.debug_tab = self.gui.set_cap_and_get_debug_tab(cap, on_ear_change, initial_ear)

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

    def destroy_gui(self):
        self.gui.destroy()
