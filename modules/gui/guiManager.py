from administratorWindow import AdministratorWindow

class GuiManager():
    def __init__(self, cap, settings_manager):
        self.cap = cap
        self.settings_manager = settings_manager
        self.gui = AdministratorWindow()
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
