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
gui_data = {
        "tab1": {"title": "Instructions",
            "elements": [
                {
                    "format": "text",
                    "body": "This is where instructional text goes."
                },
                {
                    "format": "text",
                    "body": "This is another paragraph."
                },
                {
                    "format": "video"
                },
#This is another 'nother paragraph, added as an element after the video -- note that this actually shows up above the video. In fact, while multiple tabs can be added to this data structure for text content any video content will show up on every tab. I don't understand if this is a problem in my code (i.e. me understanging Tk well enough but typing something incorrectly), or if I need to do something special to format canvases in Tkinter. My current plan is to just leave the debug window at the bottom of the interface for now and revisit this issue if time permits:
                {
                    "format": "text",
                    "body": "The only command currently registered is fist-palm-fist, but we should add a GUI interface for making new commands."
                }

            ]
        }
}

#An instance of this class represents a window with (potentially) multiple tabs.
class App(Tk):
    def __init__(self, *args,**kwargs):
        Tk.__init__(self,*args,**kwargs)

    def set_cap_and_get_debug_tab(self, cap):
        self.notebook = ttk.Notebook()
        self.debug_tab = self.add_content(gui_data, cap)
        self.notebook.grid(row=0)
        return self.debug_tab

    def add_content(self, body, cap):
        for i in range(len(list(body.keys()))):
            page_configuration = body[list(body.keys())[i]]
            tab = Page(self.notebook, self, cap, page_configuration["elements"])
            self.notebook.add(tab, text = page_configuration["title"], )
            if tab.is_debug:
                debug_tab = tab

        return debug_tab

#An instance of this class represents a tab.
#Note that the current version only has one tab, due to the canvas element
#showing up on every tab.
class Page(Frame):
    def __init__(self, name, window, cap, elements, *args,**kwargs):
        Frame.__init__(self,*args,**kwargs)
        self.is_debug = False
        row_index = 1
        for element in elements:
            if element["format"] == "text":
                self.label = Label(self, text=element["body"])
                self.label.grid(row=row_index, column=0, padx=10, pady=10)
                self.name = name
            elif element["format"] == "video":
                self.is_debug = True
                self.debug_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.debug_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.debug_canvas = Canvas(window, width = self.debug_width, height = self.debug_height)
                self.debug_canvas.grid(row = row_index, column = 0, padx = 10, pady = 10)
            row_index += 1
           
    def set_debug_frame(self, frame):
        #Translate BGR colors from OpenCV to RBG colors for PIL
        frame = frame[...,[2,1,0]]
        #Convert to an image that Tkinter can display
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        #display image
        self.debug_canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

#This is the only class which is meant to be accessed from other files. It 
#provides a high level interface for starting the gui, defining what logic
#should be executed between refresh cycles and before closing down, and moving
#data to and from the GUI (e.g. when drawing a new frame for the debug screen).
class GuiManager():
    def __init__(self, cap):
        self.gui = App()
        self.debug_tab = self.gui.set_cap_and_get_debug_tab(cap)

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
