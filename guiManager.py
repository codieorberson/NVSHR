#!/usr/local/bin/python3
from tkinter import *
from guiWindow import GuiWindow
from framesPerSecondMeter import FramesPerSecondMeter

class GuiManager():
    def __init__(self, cap, is_admin):
        self.cap = cap
        self.gui = GuiWindow()
        self.gui.title("Non-Verbal Smart Home Recognition System")

        if is_admin == False:
            self.gui.withdraw()

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

    def set_initial_log(self, logged_lines):
        logged_lines.reverse()
        self.gui.set_initial_log(logged_lines)

    def set_initial_commands(self, commands):
        self.gui.set_initial_commands(commands)

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
        self.fps_tab.set_fps(self.frames_per_second_meter.cycle())
        self.gui.after(1, self.__loop__)

    def start(self, loop_callback, close_callback):
        self.frames_per_second_meter = FramesPerSecondMeter()
        self.gui.set_cap(self.cap)
        self.debug_tab = self.gui.get_debug_tab()
        self.fps_tab = self.gui.get_fps_tab()
        self.blink_label = self.gui.get_blink_label()
        self.fist_label = self.gui.get_fist_label()
        self.palm_label = self.gui.get_palm_label()
        self.log_page = self.gui.get_log_page()

        self.loop_callback = loop_callback
        self.close_callback = close_callback
        self.gui.protocol("WM_DELETE_WINDOW", close_callback)
        self.gui.after(1, self.__loop__)
        self.gui.mainloop()

    def set_debug_frame(self, frame):
        self.debug_tab.set_debug_frame(frame)

    def set_gesture_background(self, gestures_detected):
       
        self.blink_label.set_gesture_background(gestures_detected)
        self.fist_label.set_gesture_background(gestures_detected)
        self.palm_label.set_gesture_background(gestures_detected)

    def update_log_text(self, content):
        self.log_page.log_text.config(state = NORMAL)
        
        self.log_page.log_text.insert("1.0", content)
        self.log_page.log_text.config(state = DISABLED)
        self.log_page.log_text.see(CURRENT)

    def destroy_gui(self):
        self.gui.destroy()
