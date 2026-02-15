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


#8. the function is going to accept an id
def search_data(id):
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Shadowfax@01",
        port="5432",
    )
    cur = conn.cursor()
    # we are going to execute a query to search for the data in the database using the id provided by the user
    # %s means substitute the value of id in the query
    query = '''SELECT * \
               FROM students \
               WHERE id = %s;'''
    cur.execute(query, (id,))
    result = cur.fetchone()
    #10.    then call this function here after creating the listbox
    display_search_result(result)
    conn.commit()
    cur.close()
    conn.close()
    #9. listbox is used to display the result of the search box on the window, we are defining a function for it
def display_search_result(result):
    listbox = Listbox(frame,width=25,height=7)
    listbox.grid(row=9, column=1)
    listbox.insert(END, result)
    #11. this element will display all the result
def display_all():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Shadowfax@01",
        port="5432",
    )
    cur = conn.cursor()
    query = '''SELECT * FROM students;'''
    cur.execute(query)
    results = cur.fetchall()
    listbox = Listbox(frame,width=25,height=7)
    listbox.grid(row=10, column=1)
    #12.    the for loop helps us loop from each row of the RESULT one after the other, like the entire list
    # from the "results = cur.fetchall()"
    for result in results:
        listbox.insert(END, result)
    conn.commit()
    cur.close()
    conn.close()


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

#7. creating a label for searching through the database
label = Label(frame, text="Search Data: ")
label.grid(row=5, column=1)

label = Label(frame, text="Search by ID: ")
label.grid(row=6, column=0)

entry_search_id = Entry(frame)
entry_search_id.grid(row=6, column=1)

button = Button(frame, text="Search", command=lambda: search_data(entry_search_id.get()))
button.grid(row=6, column=2)

#13.    then call the function
display_all()



root.mainloop()