#!/usr/local/bin/python3
import tkinter


class PopUp:
    def __init__(self):
        self.popup = tkinter.Tk()
        self.is_admin = None

        # Window needs to be centered within the screen and should have a title saying Welcome!
        self.center(400, 200, self.popup.winfo_screenwidth(), self.popup.winfo_screenheight())

        self.popup.geometry("400x300+%d+%d" % (self.x, self.y))
        self.popup.wm_title("Welcome!")
        self.popup.protocol("WM_DELETE_WINDOW", self.on_close)

        # Window needs labels asking for administrator info from the user
        label = tkinter.Label(self.popup, text="Welcome to the Non-Verbal Smart Home Recgotintion (NVSHR) Sytem!",
                              font=("Helvetica", 18, "bold"), background="white", wraplength=350)
        label.pack(side="top", fill="x", pady=10)
        label2 = tkinter.Label(self.popup, text="Are you an administrator?", font=("Helvetica", 14), background="white")
        label2.pack(side="top", fill="x", pady=10)

        # Window needs a way to verify if the user is an administrator
        self.value = tkinter.IntVar()
        self.value.set(0)

        choice1 = tkinter.Radiobutton(self.popup, text="Yes, I am an administrator.", variable=self.value, value=1)
        choice1.pack()
        choice2 = tkinter.Radiobutton(self.popup, text="No, I am not an administrator.", variable=self.value, value=2)
        choice2.pack()

        save_button = tkinter.Button(self.popup, text="Enter", command=self.enter_button)
        save_button.pack()

        self.popup.mainloop()

    # Method to calculate the x and y coordinates for the window
    def center(self, width, height, scr_width, scr_hei):
        self.x = (scr_width / 2) - (width / 2)
        self.y = (scr_hei / 2) - (height / 2)

    # Method called to set the current value from the radio button
    def enter_button(self):
        if self.value.get() == 1:
            self.is_admin = True
        else:
            self.is_admin = False

        self.popup.destroy()

    # Method called to send the information to the guiManager
    def send_verification(self):
        return self.is_admin

    # Method called when the user presses the "X" before answering
    def on_close(self):
        self.popup.destroy()
        exit(0)
