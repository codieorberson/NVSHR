import tkinter
from tkinter import *

root = tkinter.Tk()
root.geometry("400x400")
fr = Frame(root)
fr.pack()

sbr = Scrollbar(
    fr,
)

sbr.pack(side=RIGHT, fill="y")
lbx = Listbox(
    fr,
    font=("Verdana", 16),

)

lbx.pack(side=LEFT, fill="both", expand=True)

for data in range(100):
    lbx.insert(data, "Sample Data " + str(data + 1))

sbr.config(command=lbx.yview)
lbx.config(yscrollcommand=sbr.set)

root.mainloop()
