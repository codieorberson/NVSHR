#!/usr/local/bin/python3
from guiWindow import GuiWindow

class GuiManager():
    def __init__(self, cap, on_ear_change,
                 initial_ear, on_low_contrast, initial_low_contrast,
                 on_high_contrast, initial_high_contrast,
                 on_min_time_inc, initial_min_time_inc,
                 on_max_time_inc, initial_max_time_inc,
                 gesture_detected, is_admin, database_manager):
        self.gui = GuiWindow()
        self.gui.title("Non-Verbal Smart Home Recognition System")
        self.debug_tab = self.gui.set_cap_and_get_debug_tab(cap, on_ear_change, initial_ear,
                                                            on_low_contrast, initial_low_contrast,
                                                            on_high_contrast, initial_high_contrast,
                                                            on_min_time_inc, initial_min_time_inc,
                                                            on_max_time_inc, initial_max_time_inc,
                                                            gesture_detected, database_manager)
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
