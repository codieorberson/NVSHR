#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
from gui_data import gui_data
from guiTab import GuiTab

# An instance of this class represents a window with multiple tabs.
class GuiWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

    def set_cap_and_get_debug_tab(self, cap, on_ear_change, initial_ear,
                                  on_low_contrast, initial_low_contrast,
                                  on_high_contrast, initial_high_contrast,
                                  on_min_time_inc, initial_min_time_inc,
                                  on_max_time_inc, initial_max_time_inc,
                                  gesture_detected, settings_manager):
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.debug_tab = self.add_content(gui_data, cap, on_ear_change, initial_ear, on_low_contrast,
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
            tab = GuiTab(self.notebook, self, cap, on_ear_change, initial_ear, on_low_contrast, initial_low_contrast,
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
