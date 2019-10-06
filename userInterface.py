from __future__ import print_function
import tkinter
import threading
import datetime
import imutils
import cv2
import os


class UserInterface:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tkinter.Tk()
        self.panel = None

        btn = tkinter.Button(self.root, text="Set-Up Commands", command=self.setCommands)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("Non-Verbal Smart Home Recognition System Set-Up")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
