#!/usr/local/bin/python3
from tkinter import *
from tkinter import ttk
from gui_data import gui_data
from guiTab import GuiTab

# An instance of this class represents a window with multiple tabs.
class GuiWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.notebook = ttk.Notebook(width=1000, height=800)
        self.notebook.grid(row=0)
        self.page_configurations = []
        self.tabs = []
        self.tab_indices = range(len(list(gui_data.keys())))

        for i in self.tab_indices:
            self.page_configurations.append(gui_data[list(gui_data.keys())[i]])
            self.tabs.append(GuiTab(self.notebook, self))

    def set_up_ear(self, initial_value, callback):
        for tab in self.tabs:
            tab.set_up_ear(initial_value, callback)

    def set_up_low_contrast(self, initial_value, callback):
        for tab in self.tabs:
            tab.set_up_low_contrast(initial_value, callback)

    def set_up_high_contrast(self, initial_value, callback):
        for tab in self.tabs:
            tab.set_up_high_contrast(initial_value, callback)

    def set_up_minimum_time_increment(self, initial_value, callback):
        for tab in self.tabs:
            tab.set_up_minimum_time_increment(initial_value, callback)

    def set_up_maximum_time_increment(self, initial_value, callback):
        for tab in self.tabs:
            tab.set_up_maximum_time_increment(initial_value, callback)

    def set_up_commands(self, commands, callback):
        for tab in self.tabs:
            tab.set_up_commands(commands, callback)

    def set_initial_log(self, logged_lines):
        for tab in self.tabs:
            tab.set_initial_log(logged_lines)

    def set_cap(self, cap):
        for tab in self.tabs:
            tab.set_cap(cap)

    def set_up_tabs(self):
        for i in self.tab_indices:
            tab = self.tabs[i]
            page_configuration = self.page_configurations[i]

            tab.load_data(page_configuration['elements'])
            self.notebook.add(tab, text=page_configuration["title"])

            if tab.is_debug:
                self.debug_tab = tab
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
            if tab.is_low_contrast:
                self.low_contrast = tab
            if tab.is_high_contrast:
                self.high_contrast = tab

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

    def get_low_contrast(self):
        return self.low_contrast

    def get_high_contrast(self):
        return self.high_contrast
