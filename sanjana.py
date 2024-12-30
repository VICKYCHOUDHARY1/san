import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# CSV file name
CSV_FILE = "exam_centers.csv"

# Ensure the CSV file exists
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Center Code", "Center Name", "District", "State", "Student Roll No", "Class (10/12)"])

# Function to read data from CSV
def read_data():
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                data.append(row)
    return data

# Function to write a new record to the CSV file
def write_data(record):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(record)

# Function to update an existing record in the CSV file
def update_data(center_code, student_roll_no, new_center_name, new_district, new_state, new_class):
    data = read_data()
    updated = False
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Center Code", "Center Name", "District", "State", "Student Roll No", "Class (10/12)"])  # Write header
        for row in data:
            if row[0] == center_code and row[4] == student_roll_no:
                row[1] = new_center_name
                row[2] = new_district
                row[3] = new_state
                row[5] = new_class
                updated = True
            writer.writerow(row)
    return updated

# Function to delete a record from the CSV file
def delete_data(center_code):
    data = read_data()
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Center Code", "Center Name", "District", "State", "Student Roll No", "Class (10/12)"])  # Write header
        for row in data:
            if row[0] != center_code:
                writer.writerow(row)

# Admin panel
def admin_panel():
    def refresh_table():
        # Clear the treeview before adding new data
        for row in tree.get_children():
            tree.delete(row)
        for row in read_data():
            tree.insert("", "end", values=row)

    def add_record():
        try:
            start_roll = int(entry_start_rollno.get())
            end_roll = int(entry_end_rollno.get())
            class_name = entry_class.get()
            center_code = entry_center_code.get()
            center_name = entry_center_name.get()
            district = entry_district.get()
            state = entry_state.get()

            if start_roll > end_roll:
                messagebox.showwarning("Input Error", "Starting Roll No cannot be greater than Ending Roll No.")
                return

            # Generate records for all students in the range
            for roll_no in range(start_roll, end_roll + 1):
                new_record = (
                    center_code, center_name, district, state, str(roll_no), class_name
                )
                write_data(new_record)
            
            refresh_table()
            messagebox.showinfo("Success", f"Records for roll numbers {start_roll} to {end_roll} added successfully!")
            clear_fields()

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numeric values for Roll No.")

    def update_record():
        selected_item = tree.selection()  # Get selected row from the treeview
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return
        
        center_code = tree.item(selected_item[0])['values'][0]  # Extract center_code from the selected row
        student_roll_no = tree.item(selected_item[0])['values'][4]  # Extract student_roll_no from the selected row
        
        # Gather the updated values from the entry fields
        new_center_name = entry_center_name.get()
        new_district = entry_district.get()
        new_state = entry_state.get()
        new_class = entry_class.get()
        
        if messagebox.askyesno("Update Confirmation", f"Are you sure you want to update record with Center Code: {center_code}, Roll No: {student_roll_no}?"):
            if update_data(center_code, student_roll_no, new_center_name, new_district, new_state, new_class):
                refresh_table()  # Refresh the table to show updated records
                messagebox.showinfo("Success", f"Record updated successfully.")
            else:
                messagebox.showwarning("Update Failed", "Record not found.")

    def delete_record():
        selected_item = tree.selection()  # Get selected row from the treeview
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        
        center_code = tree.item(selected_item[0])['values'][0]  # Extract center_code from the selected row
        
        if messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete record with Center Code: {center_code}?"):
            delete_data(center_code)  # Call the delete_data function
            refresh_table()  # Refresh the table to show updated records
            messagebox.showinfo("Success", f"Record with Center Code: {center_code} deleted successfully.")

    def clear_fields():
        entry_center_code.delete(0, tk.END)
        entry_center_name.delete(0, tk.END)
        entry_district.delete(0, tk.END)
        entry_state.delete(0, tk.END)
        entry_class.delete(0, tk.END)
        entry_start_rollno.delete(0, tk.END)
        entry_end_rollno.delete(0, tk.END)

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("900x500")

    # Set background color
    admin_window.configure(bg="#f0f8ff")

    frame = tk.Frame(admin_window, bg="#f0f8ff")
    frame.pack(fill="both", expand=True)

    # Entry fields for new data
    labels = [
        "Center Code", "Center Name", "District", "State", 
        "Class (10/12)", "Start Roll No", "End Roll No"
    ]
    entries = []
    for i, label in enumerate(labels):
        lbl = tk.Label(frame, text=label, bg="#f0f8ff", font=("Helvetica", 10, "bold"))
        lbl.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    (entry_center_code, entry_center_name, entry_district, entry_state, 
     entry_class, entry_start_rollno, entry_end_rollno) = entries

    # Buttons for operations
    btn_add = tk.Button(frame, text="Add Records", bg="#20b2aa", fg="white", font=("Helvetica", 10, "bold"), command=add_record)
    btn_add.grid(row=0, column=2, padx=5, pady=5)

    btn_update = tk.Button(frame, text="Update Selected", bg="#ff8c00", fg="white", font=("Helvetica", 10, "bold"), command=update_record)
    btn_update.grid(row=1, column=2, padx=5, pady=5)

    btn_delete = tk.Button(frame, text="Delete Selected", bg="#dc143c", fg="white", font=("Helvetica", 10, "bold"), command=delete_record)
    btn_delete.grid(row=2, column=2, padx=5, pady=5)

    # Treeview for displaying data (without initial headers or data)
   
    tree = ttk.Treeview(admin_window, show="headings")
    
    # Note: We're not adding any initial data here and not showing the headers automatically
    tree.pack(fill="both", expand=True)

    # Refresh the table when the admin panel is opened
    refresh_table()

# Student panel (unchanged)
def student_panel():
    def fetch_student_details():
        roll_no = entry_student_rollno.get().strip()
        class_name = entry_student_class.get().strip()

        if not roll_no or not class_name:
            lbl_center_details.config(text="Please enter both Roll No and Class.")
            return

        data = read_data()
        result = None
        for row in data:
            if row[4].strip() == roll_no and row[5].strip() == class_name:
                result = row
                break

        if result:
            lbl_center_details.config(
                text=f"Center Code: {result[0]}\n"
                    f"Center Name: {result[1]}\n"
                    f"District: {result[2]}\n"
                     f"State: {result[3]}"
        )
        else:
            lbl_center_details.config(text="No data found for the provided Roll No and Class.")


    student_window = tk.Toplevel(root)
    student_window.title("Student Panel")
    student_window.geometry("800x400")

    # Set background color
    student_window.configure(bg="#ffe4e1")

    frame = tk.Frame(student_window, bg="#ffe4e1")
    frame.pack(pady=20)

    # Labels and entry fields for student details
    lbl_roll_no = tk.Label(frame, text="Enter Roll No:", bg="#ffe4e1", font=("Helvetica", 10, "bold"))
    lbl_roll_no.grid(row=0, column=0, padx=5, pady=5)
    entry_student_rollno = tk.Entry(frame)
    entry_student_rollno.grid(row=0, column=1, padx=5, pady=5)

    lbl_class = tk.Label(frame, text="Enter Class (10/12):", bg="#ffe4e1", font=("Helvetica", 10, "bold"))
    lbl_class.grid(row=1, column=0, padx=5, pady=5)
    entry_student_class = tk.Entry(frame)
    entry_student_class.grid(row=1, column=1, padx=5, pady=5)

    # Button to fetch details
    btn_fetch = tk.Button(frame, text="Fetch Center Details", bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), command=fetch_student_details)
    btn_fetch.grid(row=2, column=0, columnspan=2, pady=10)

    # Label for showing center details
    lbl_center_details = tk.Label(frame, text="Center Details will be displayed here.", bg="#ffe4e1", font=("Helvetica", 10, "bold"))
    lbl_center_details.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Login screen
root = tk.Tk()
root.title("Exam Center Management")
root.geometry("300x200")

# Set background color
root.configure(bg="#fffacd")

frame = tk.Frame(root, bg="#fffacd")
frame.pack(pady=20)

btn_admin = tk.Button(frame, text="Admin Login", width=15, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), command=admin_panel)
btn_admin.grid(row=0, column=0, padx=5, pady=10)

btn_student = tk.Button(frame, text="Student Login", width=15, bg="#32cd32", fg="white", font=("Helvetica", 10, "bold"), command=student_panel)
btn_student.grid(row=1, column=0, padx=5, pady=10)

# Initialize CSV file
init_csv()

root.mainloop()
