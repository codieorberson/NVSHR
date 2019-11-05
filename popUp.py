#!/usr/local/bin/python3
import tkinter as tkinter

def _swallow_exception(exception, value, traceback):
    #This is an EXCEPTIONALLY bad practice, but I'm not sure how else to avoid
    #barfing up errors to the console when we switch windows.
    pass

class PopUp:
    def __init__(self, loop_callback, admin_callback, close_callback):
        self.popup = tkinter.Tk()
        self.popup.report_callback_exception = _swallow_exception

        self.is_admin = None

        self.loop_callback = loop_callback
        self.admin_callback = admin_callback
        self.close_callback = close_callback

        # Window needs to be centered within the screen and should have a title saying Welcome!
        self.center(400, 300, self.popup.winfo_screenwidth(), self.popup.winfo_screenheight())

        self.popup.geometry("400x250+%d+%d" % (self.x, self.y))
        self.popup.wm_title("Welcome!")
        self.popup.protocol("WM_DELETE_WINDOW", self.close)

        # Window needs labels asking for administrator info from the user
        label = tkinter.Label(self.popup, text="Welcome to the Non-Verbal Smart Home Recgotintion (NVSHR) Sytem!",
                              font=("Helvetica", 18, "bold"), background="white", wraplength=350)
        label.pack(side="top", fill="x", pady=10)
        label2 = tkinter.Label(self.popup, text="Are you an administrator?", font=("Helvetica", 14), background="white")
        label2.pack(side="top", fill="x", pady=10)

        # Window needs a way to verify if the user is an administrator
        self.value = tkinter.IntVar()
        self.value.set(0)

        save_button = tkinter.Button(self.popup, text="Display Admin Settings", command=self.enter_button)
        save_button.pack()

        self.popup.after(1, self.__loop__)

    def start(self):
         self.popup.mainloop()       

    def __loop__(self):
        if not self.is_admin:
            self.loop_callback()
            self.popup.after(1, self.__loop__)
            self.popup.mainloop()
        else:
            self.admin_callback()

    # Method to calculate the x and y coordinates for the window
    def center(self, width, height, scr_width, scr_hei):
        self.x = (scr_width / 2) - (width / 2)
        self.y = (scr_hei / 2) - (height / 2)

    # Method called to set the current value from the radio button
    def enter_button(self):
        self.is_admin = True
        self.close()

    # Method called to send the information to the guiManager
    def send_verification(self):
        return self.is_admin

    # Method called when the user presses the "X" before answering
    def close(self):
        if self.is_admin:
            self.popup.withdraw()
            self.close_pop_up()
        else:
            self.close_system()

    def close_pop_up(self):
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            self.popup.destroy()
            self.admin_callback()

    def close_system(self):
        self.close_callback()
        self.popup.destroy()
        exit(0)
