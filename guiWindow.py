#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
from gui_data import gui_data
from guiTab import GuiTab


# An instance of this class represents a window with multiple tabs.
class GuiWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

    def set_initial_ear(self, initial_value):
        self.initial_ear = initial_value

    def set_initial_minimum_time_increment(self, initial_value):
        self.initial_minimum_time_increment = initial_value

    def set_initial_maximum_time_increment(self, initial_value):
        self.initial_maximum_time_increment = initial_value

    def on_ear_change(self, callback):
        self.on_ear_change = callback

    def on_minimum_time_increment_change(self, callback):
        self.on_minimum_time_increment_change = callback

    def on_maximum_time_increment_change(self, callback):
        self.on_maximum_time_increment_change = callback

    def on_new_command(self, callback):
        self.on_new_command_change = callback

    def set_cap(self, cap, settings_manager):
        self.cap = cap
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.debug_tab = self.add_content(gui_data, settings_manager)

        self.notebook.grid(row=0)

    def add_content(self, body, settings_manager):
        for i in range(len(list(body.keys()))):
            page_configuration = body[list(body.keys())[i]]
            tab = GuiTab(self.notebook, self, settings_manager)

            tab.set_initial_ear(self.initial_ear)
            tab.set_initial_minimum_time_increment(self.initial_minimum_time_increment)
            tab.set_initial_maximum_time_increment(self.initial_maximum_time_increment)
            tab.set_cap(self.cap)

            tab.on_ear_change(self.on_ear_change)
            tab.on_minimum_time_increment_change(self.on_minimum_time_increment_change)
            tab.on_maximum_time_increment_change(self.on_maximum_time_increment_change)
            tab.on_new_command(self.on_new_command_change)

            tab.load_data(page_configuration['elements'])
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
            if tab.is_logfile:
                self.log_text = tab

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

    def get_log_page(self):
        return self.log_text

    def withdraw_gui(self):
        self.withdraw()
