#!/usr/bin/python

import tkinter as tk
import os

w = 800  # width for the Tk root
h = 100  # height for the Tk root


def sh_escape(s):
    return s.replace("(", "\\(").replace(")", "\\)").replace(" ", "\\ ")

def gui_input(prompt):
    def play_and_close():
        root.destroy()

    root = tk.Tk()
    w = 480  # width for the Tk root
    h = 150  # keep the original height

    # Get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = 20
    y = 20

    # Set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # This will contain the entered string, and will still exist after the window is destroyed
    var = tk.StringVar()

    # Create the GUI
    label = tk.Label(root, text=prompt)
    entry = tk.Entry(root, textvariable=var)

    # Create a frame to hold the widgets
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Place the label and entry within the frame
    label.pack(side="left", padx=(20, 0), pady=20)
    entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)

    # Create and place the play button at the bottom
    play_button = tk.Button(frame, text="Şifrelenmiş Sesi Çal", font=("Helvetica", 16), command=play_and_close)
    play_button.pack(side="bottom", pady=10)

    # Let the user press the return key to destroy the gui 
    entry.bind("<Return>", lambda event: root.destroy())

    # This will block until the window is destroyed
    root.mainloop()

    # After the window has been destroyed, we can't access the entry widget,
    # but we _can_ access the associated variable
    value = var.get()
    return value

mesaj = gui_input("Sifrelenecek Mesaj")
print(mesaj)
