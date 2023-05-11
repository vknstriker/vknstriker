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
login_frame = tk.LabelFrame(root, text="Login")
login_frame.pack(fill="both", expand=True)

# Create the ID entry
id_label = tk.Label(login_frame, text="ID:")
id_label.pack()
id_entry = tk.Entry(login_frame)
id_entry.pack()

# Create the login button
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

# Create the admin frame
admin_frame = tk.LabelFrame(root, text="Administrator")
admin_frame.pack(fill="both", expand=True)

# Create the new employee frame
new_employee_frame = tk.LabelFrame(admin_frame, text="Add New Employee")
new_employee_frame.pack(fill="both", expand=True)

# Create the new ID entry
new_id_label = tk.Label(new_employee_frame, text="ID:")
new_id_label.pack()
new_id_entry = tk.Entry(new_employee_frame)
new_id_entry.pack()

# Create the new name entry
new_name_label = tk.Label(new_employee_frame, text="Name:")
new_name_label.pack()
new_name_entry = tk.Entry(new_employee_frame)
new_name_entry.pack()

# Create the new email entry
new_email_label = tk.Label(new_employee_frame, text="Email:")
new_email_label.pack()
new_email_entry = tk.Entry(new_employee_frame)
new_email_entry.pack()

# Create the add employee button
add_employee_button = tk.Button(new_employee_frame, text="Add Employee", command=add_employee)
add_employee_button.pack()

root.mainloop()
