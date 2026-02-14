from tkinter import *
import tkinter as tk
import psycopg2
root = Tk()
#6. creating the function for the submit button
def entry_data(name, age, address):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Shadowfax@01",
        port="5432",
    )
    cur = conn.cursor()
    query = '''INSERT INTO students(name, age, address) VALUES (%s, %s, %s);'''
    cur.execute(query,(name, age, address))
    print(f"Inserted: {name}, {age}, {address}")
    conn.commit()
    cur.close()
    display_all()

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

label = Label(frame, text="Name: ")
label.grid(row=1, column=0)

entry_name = Entry(frame)
entry_name.grid(row=1, column=1)

label = Label(frame, text="Age: ")
label.grid(row=2, column=0)

entry_age = Entry(frame)
entry_age.grid(row=2, column=1)

label = Label(frame, text="Address: ")
label.grid(row=3, column=0)

entry_address = Entry(frame)
entry_address.grid(row=3, column=1)

#5. we are going to execute using lambda fuction when the button is clicked bcos it executes
#5. at runtime and not at the time of button creation
button = Button(frame, text="Submit", command=lambda: entry_data(entry_name.get(),entry_age.get(),entry_address.get()))
button.grid(row=4, column=1)



root.mainloop()