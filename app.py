import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import csv

# -----------------------------
# DATABASE CONFIG
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Shadowfax@01",
    "port": "5432"
}

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# -----------------------------
# CRUD FUNCTIONS
# -----------------------------
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    address = entry_address.get()

    if not name or not age:
        messagebox.showwarning("Input Error", "Name and Age are required!")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, address) VALUES (%s, %s, %s)",
        (name, age, address)
    )
    conn.commit()
    cur.close()
    conn.close()

    clear_entries()
    display_all()


def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Select a student to update")
        return

    student_id = tree.item(selected)["values"][0]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s, age=%s, address=%s WHERE id=%s",
        (entry_name.get(), entry_age.get(), entry_address.get(), student_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    display_all()


def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Record", "Select a student to delete")
        return

    student_id = tree.item(selected)["values"][0]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    cur.close()
    conn.close()

    display_all()


def search_by_name():
    name = entry_search.get()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE name ILIKE %s", ('%' + name + '%',))
    results = cur.fetchall()

    tree.delete(*tree.get_children())
    for row in results:
        tree.insert("", "end", values=row)

    cur.close()
    conn.close()


def display_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    results = cur.fetchall()

    tree.delete(*tree.get_children())
    for row in results:
        tree.insert("", "end", values=row)

    cur.close()
    conn.close()


def export_to_csv():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    results = cur.fetchall()

    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Age", "Address"])
            writer.writerows(results)

    cur.close()
    conn.close()


def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_address.delete(0, tk.END)


def select_record(event):
    selected = tree.focus()
    values = tree.item(selected)["values"]
    if values:
        clear_entries()
        entry_name.insert(0, values[1])
        entry_age.insert(0, values[2])
        entry_address.insert(0, values[3])


# -----------------------------
# GUI SETUP
# -----------------------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x500")
root.configure(bg="#f4f6f9")

style = ttk.Style()
style.theme_use("clam")

# -----------------------------
# FORM FRAME
# -----------------------------
form_frame = ttk.LabelFrame(root, text="Student Details", padding=20)
form_frame.pack(fill="x", padx=20, pady=10)

ttk.Label(form_frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
entry_name = ttk.Entry(form_frame)
entry_name.grid(row=0, column=1, padx=10)

ttk.Label(form_frame, text="Age").grid(row=1, column=0, padx=10, pady=5)
entry_age = ttk.Entry(form_frame)
entry_age.grid(row=1, column=1, padx=10)

ttk.Label(form_frame, text="Address").grid(row=2, column=0, padx=10, pady=5)
entry_address = ttk.Entry(form_frame)
entry_address.grid(row=2, column=1, padx=10)

# Buttons
ttk.Button(form_frame, text="Add", command=add_student).grid(row=0, column=2, padx=10)
ttk.Button(form_frame, text="Update", command=update_student).grid(row=1, column=2, padx=10)
ttk.Button(form_frame, text="Delete", command=delete_student).grid(row=2, column=2, padx=10)
ttk.Button(form_frame, text="Export CSV", command=export_to_csv).grid(row=3, column=2, padx=10)

# -----------------------------
# SEARCH FRAME
# -----------------------------
search_frame = ttk.LabelFrame(root, text="Search", padding=10)
search_frame.pack(fill="x", padx=20, pady=5)

entry_search = ttk.Entry(search_frame)
entry_search.pack(side="left", padx=10)

ttk.Button(search_frame, text="Search by Name", command=search_by_name).pack(side="left")

# -----------------------------
# TABLE FRAME
# -----------------------------
table_frame = ttk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("ID", "Name", "Age", "Address")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)

tree.bind("<ButtonRelease-1>", select_record)

display_all()
root.mainloop()
