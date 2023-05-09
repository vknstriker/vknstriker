import pandas as pd
import datetime
import tkinter as tk
from tkinter import messagebox
import geocoder

# Create a pandas dataframe to store the attendance data
attendance_df = pd.DataFrame(columns=['Email', 'Start Time', 'End Time', 'Location'])




# Define a function to record the start time of the employee and their location
def record_start_time():
    # Get the current system time
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the email entered by the employee
    email = email_entry.get()

    # Get the employee's location
    location = geocoder.ip('me').latlng

    # Add the data to the attendance dataframe
    attendance_df.loc[len(attendance_df)] = [email, start_time, '', location]

    # Show a message box to confirm the data has been recorded
    messagebox.showinfo('Success', 'Attendance data recorded!')


# Define a function to record the end time of the employee and their location
def record_end_time():
    # Get the current system time
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the email entered by the employee
    email = email_entry.get()

    # Get the employee's location
    location = geocoder.ip('me').latlng

    # Update the end time and location in the attendance dataframe for the corresponding email
    attendance_df.loc[attendance_df['Email'] == email, ['End Time', 'Location']] = [end_time, location]

    # Show a message box to confirm the data has been recorded
    messagebox.showinfo('Success', 'Attendance data recorded!')


# Define a function to show all the attendance data in the dataframe
def show_attendance_data():
    # Create a new window to display the attendance data
    window = tk.Toplevel(root)

    # Create a text widget to display the attendance data
    text_widget = tk.Text(window)

    # Insert the attendance data into the text widget
    text_widget.insert(tk.END, attendance_df.to_string(index=False))

    # Disable editing of the text widget
    text_widget.config(state=tk.DISABLED)

    # Pack the text widget into the window
    text_widget.pack()


# Create the main window
root = tk.Tk()

# Set the window title
root.title('Employee Attendance Tracker')

# Create a label for the email entry
email_label = tk.Label(root, text='Enter Email:')
email_label.pack()

# Create an entry widget for the email
email_entry = tk.Entry(root)
email_entry.pack()

# Create a button to record the start time
start_time_button = tk.Button(root, text='Record Start Time', command=record_start_time)
start_time_button.pack()

# Create a button to record the end time
end_time_button = tk.Button(root, text='Record End Time', command=record_end_time)
end_time_button.pack()

# Create a button to show all attendance data
show_data_button = tk.Button(root, text='Show Attendance Data', command=show_attendance_data)
show_data_button.pack()

# Start the main event loop
root.mainloop()
