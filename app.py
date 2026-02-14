from tkinter import *
import tkinter as tk
root = Tk()

#1. creating an object canvas(used for drawing shapes and graphics) and placing it in the main window
canvas = tk.Canvas(root, width=500, height=600)
canvas.pack()

#2. A frame is a rectangular container used to group and organize other widgets
frame = Frame(root)
#3  we are placing the frame in the center of the canvas using the place geometry manager
frame.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5, anchor='center')

#4. placing a label inside the frame with the text "Hello, Student!"
label = Label(frame, text="Add Data: ")
label.grid(row=0, column=1)



root.mainloop()