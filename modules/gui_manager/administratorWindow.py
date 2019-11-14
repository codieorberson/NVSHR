from tkinter import *
from tkinter import ttk
import tkinter
from tab import Tab
from guiLayout import gui_layout

# An instance of this class represents a window with multiple tabs.
class AdministratorWindow(Tk):
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
        self.debug_tab = self.add_content(gui_layout, cap, 
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
            tab = Tab(self.notebook, self, cap, 
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
