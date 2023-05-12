import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

# Create the main window
root = tk.Tk()
root.title("Attendance System")

# Create the employee data file if it doesn't exist
try:
    emp_data = pd.read_excel("emp_data.xlsx")
except FileNotFoundError:
    emp_data = pd.DataFrame(columns=["ID", "Name", "Email"])
    emp_data.to_excel("emp_data.xlsx", index=False)

# Create the attendance file if it doesn't exist
try:
    attendance = pd.read_excel("attendance.xlsx")
except FileNotFoundError:
    attendance = pd.DataFrame(columns=["ID", "Date", "Entry Time", "Exit Time"])
    attendance.to_excel("attendance.xlsx", index=False)


def login():
    # Get the entered ID
    id = id_entry.get()

    # Check if the ID is in the employee data
    if id in emp_data["ID"].values:
        # Check if the employee has already logged in today
        if (attendance["ID"] == id) & (attendance["Date"] == datetime.now().strftime("%Y-%m-%d")) & (
        pd.isnull(attendance["Exit Time"])).any():
            # Ask if the employee wants to log out
            if messagebox.askyesno("Log Out", "Do you want to log out?"):
                # Record the exit time
                attendance.loc[(attendance["ID"] == id) & (attendance["Date"] == datetime.now().strftime(
                    "%Y-%m-%d")), "Exit Time"] = datetime.now().strftime("%H:%M:%S")
                attendance.to_excel("attendance.xlsx", index=False)
                messagebox.showinfo("Logged Out", "You have been logged out.")
        else:
            # Record the entry time
            attendance.loc[len(attendance)] = [id, datetime.now().strftime("%Y-%m-%d"),
                                               datetime.now().strftime("%H:%M:%S"), None]
            attendance.to_excel("attendance.xlsx", index=False)
            messagebox.showinfo("Logged In", "You have been logged in.")
    else:
        messagebox.showerror("Error", "ID not found.")


def add_employee():
    # Get the entered data
    id = new_id_entry.get()
    name = new_name_entry.get()
    email = new_email_entry.get()

    # Check if the ID already exists
    if id in emp_data["ID"].values:
        messagebox.showerror("Error", "ID already exists.")
    else:
        # Add the new employee to the employee data
        emp_data.loc[len(emp_data)] = [id, name, email]
        emp_data.to_excel("emp_data.xlsx", index=False)
        messagebox.showinfo("Employee Added", "The new employee has been added.")


# Create the login frame
from tkinter import*
from PIL import Image, ImageTk


root = Tk()

# Adjust size
root.geometry("400x400")

# Add image file
bg = PhotoImage(file="mainbg.png")

# Create Canvas
canvas1 = Canvas(root, width=400, height=400)





logadmin_frame = tk.LabelFrame(root)
logadmin_frame.pack(side='right', fill="both", expand=True)
logadmin_frame.configure(bg='#90EE90')


canvas = Canvas(logadmin_frame, width = 200, height = 100)
canvas.pack(anchor='n')
canvas.pack()
img = (Image.open("WorkTrack.png"))
resized_image = img.resize((200,100), Image.ANTIALIAS)
new_image=ImageTk.PhotoImage(resized_image)
canvas.create_image(1,1,anchor='nw', image=new_image)


login_frame = tk.LabelFrame(logadmin_frame, text="Employee Login")
login_frame.pack(side='top',fill="both", expand=True, padx=450, pady=200)
login_frame.configure(bg='#CBD18F')


# Create the ID entry
id_label = tk.Label(login_frame, text="Enter ID:", font=("Courier",15,'bold'), bg='#CBD18F')
id_label.pack()
id_entry = tk.Entry(login_frame, bg='#A7BEAE')
id_entry.pack()

# Create the login button
login_button = tk.Button(login_frame, text="Login", command=login, bg='#2BAE66', fg='#031B33' )

login_button.pack()

# Create the admin frame
admin_frame = tk.LabelFrame(root, text="Administrator")
admin_frame.pack(fill="both", expand=True)
admin_frame.configure(bg='#8AAAE5')

# Create the new employee frame
new_employee_frame = tk.LabelFrame(admin_frame, text="Add New Employee")
new_employee_frame.pack(fill="both", expand=True,padx=10, pady=250)
new_employee_frame.configure(bg='teal')

# Create the new ID entry
new_id_label = tk.Label(new_employee_frame, text="ID:", bg='teal')
new_id_label.pack()
new_id_entry = tk.Entry(new_employee_frame, bg='#A7BEAE')
new_id_entry.pack()

# Create the new name entry
new_name_label = tk.Label(new_employee_frame, text="Name:", bg='teal')
new_name_label.pack()
new_name_entry = tk.Entry(new_employee_frame, bg='#A7BEAE')
new_name_entry.pack()

# Create the new email entry
new_email_label = tk.Label(new_employee_frame, text="Email:",bg='teal')
new_email_label.pack()
new_email_entry = tk.Entry(new_employee_frame, bg='#A7BEAE')
new_email_entry.pack()

# Create the add employee button
add_employee_button = tk.Button(new_employee_frame, text="Add Employee", command=add_employee, bg='#E2D1F9',)
add_employee_button.pack()

root.mainloop()
