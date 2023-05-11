import datetime
import tkinter as tk
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Check if employee data file exists, otherwise create a new one
if not os.path.isfile('emp_data.xlsx'):
    pd.DataFrame(columns=['ID', 'Name', 'Email']).to_excel('emp_data.xlsx', index=False)

# Check if attendance data file exists, otherwise create a new one
if not os.path.isfile('attendance_data.xlsx'):
    pd.DataFrame(columns=['ID', 'Entry Time', 'Exit Time']).to_excel('attendance_data.xlsx', index=False)

# Read employee data from Excel
df = pd.read_excel('emp_data.xlsx')

# Create an empty dataframe for attendance records
attendance_df = pd.DataFrame(columns=['ID', 'Entry Time', 'Exit Time'])


# Function to handle the login process
def login():
    emp_id = id_entry.get()
    if emp_id in df['ID'].values:
        entry_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_df.loc[len(attendance_df)] = [emp_id, entry_time, '']
        attendance_df.to_excel('attendance_data.xlsx', index=False)
        status_label.config(text="Logged in successfully.")
        logout_button.config(state=tk.NORMAL)
    else:
        status_label.config(text="Invalid ID.")


# Function to handle the logout process
def logout():
    emp_id = id_entry.get()
    if emp_id in df['ID'].values:
        exit_time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_df.loc[(attendance_df['ID'] == emp_id) & (attendance_df['Exit Time'] == ''), 'Exit Time'] = exit_time
        attendance_df.to_excel('attendance_data.xlsx', index=False)
        status_label.config(text="Logged out successfully.")
        logout_button.config(state=tk.DISABLED)
    else:
        status_label.config(text="Invalid ID.")


# Function to open the administrator panel
def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Administrator Panel")

    # Function to handle adding a new employee
    def add_employee():
        emp_id = id_entry.get()
        emp_name = name_entry.get()
        emp_email = email_entry.get()

        if emp_id in df['ID'].values:
            status_label.config(text="Employee ID already exists.")
        else:
            df.loc[len(df)] = [emp_id, emp_name, emp_email]
            df.to_excel('emp_data.xlsx', index=False)
            status_label.config(text="Employee added successfully.")
            clear_entries()

    def show_latecomers():
        today = dt.date.today()
        attendance_df = pd.read_excel('attendance_data.xlsx')
        latecomers_df = attendance_df[
            pd.to_datetime(attendance_df['Entry Time']).dt.time > pd.to_datetime('09:00:00').time()]
        latecomers_df['Late Duration'] = pd.to_datetime(latecomers_df['Entry Time']).dt.time.apply(
            lambda x: (pd.to_datetime(x) - pd.to_datetime('09:00:00')).seconds // 60)
        if len(latecomers_df) > 0:
            latecomers_window = tk.Toplevel(admin_window)
            latecomers_window.title("Latecomers")
            table = tk.Label(latecomers_window, text=latecomers_df.to_string(index=False))
            table.pack()
        else:
            status_label.config(text="No latecomers found.")

    import datetime

    # Rest of your code...

    def show_statistics():
        # Read the attendance data from Excel
        attendance_data = pd.read_excel('attendance_data.xlsx')

        # Convert 'Entry Time' column to datetime type
        attendance_data['Entry Time'] = pd.to_datetime(attendance_data['Entry Time'])

        # Calculate the statistics
        total_employees = len(attendance_data['ID'].unique())
        today = pd.Timestamp.now().floor('D')
        today_attendance = attendance_data[attendance_data['Entry Time'].dt.date == today.date()]
        present_employees = len(today_attendance['ID'].unique())
        absent_employees = total_employees - present_employees

        latecomers = today_attendance[today_attendance['Entry Time'].dt.time > datetime.time(9, 0)]
        if len(latecomers) > 0:
            latecomers['Late Duration'] = (latecomers['Entry Time'].dt.time - datetime.time(9, 0)).astype(
                'timedelta64[m]')
            max_latecomer_duration = latecomers['Late Duration'].max()
        else:
            max_latecomer_duration = 0

        # Create the statistics window
        statistics_window = tk.Toplevel()
        statistics_window.title("Attendance Statistics")

        # Display the statistics
        total_employees_label = tk.Label(statistics_window, text="Total Employees: {}".format(total_employees))
        total_employees_label.pack()

        present_employees_label = tk.Label(statistics_window,
                                           text="Present Employees Today: {}".format(present_employees))
        present_employees_label.pack()

        absent_employees_label = tk.Label(statistics_window, text="Absent Employees Today: {}".format(absent_employees))
        absent_employees_label.pack()

        max_latecomer_duration_label = tk.Label(statistics_window, text="Maximum Latecomer Duration: {} minutes".format(
            max_latecomer_duration))
        max_latecomer_duration_label.pack()

        # Run the statistics window
        statistics_window.mainloop()

    # Rest of your code...

    def clear_entries():
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    # Create the administrator panel window
    admin_window = tk.Tk()
    admin_window.title("Administrator Panel")

    # Create GUI elements
    id_label = tk.Label(admin_window, text="ID:")
    id_label.grid(row=0, column=0, padx=10, pady=10)

    name_label = tk.Label(admin_window, text="Name:")
    name_label.grid(row=1, column=0, padx=10, pady=10)

    email_label = tk.Label(admin_window, text="Email:")
    email_label.grid(row=2, column=0, padx=10, pady=10)

    id_entry = tk.Entry(admin_window)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    name_entry = tk.Entry(admin_window)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    email_entry = tk.Entry(admin_window)
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    add_button = tk.Button(admin_window, text="Add Employee", command=add_employee)
    add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    status_label = tk.Label(admin_window, text="")
    status_label.grid(row=4, column=0, columnspan=2)

    statistics_button = tk.Button(admin_window, text="View Statistics", command=show_statistics)
    statistics_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    latecomers_button = tk.Button(admin_window, text="View Latecomers", command=show_latecomers)
    latecomers_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


# Create the main window
root = tk.Tk()
root.title("Attendance System")
root.attributes('-fullscreen', True)  # Maximize the screen

# Create GUI elements
id_label = tk.Label(root, text="ID:")
id_label.pack()

id_entry = tk.Entry(root)
id_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

logout_button = tk.Button(root, text="Logout", command=logout, state=tk.DISABLED)
logout_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

admin_button = tk.Button(root, text="Administrator Panel", command=open_admin_panel)
admin_button.pack()

# Start the GUI event loop
root.mainloop()
