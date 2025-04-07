import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import hashlib

# ----------------------------
# Helper Function: Database Connection
# ----------------------------
def get_connection():
    """Return a connection to the mriscan MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',               # Update username
            password='******',         # Update password
            database='mriscan'         # Ensure correct database name
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

# ----------------------------
# Patients Management Functions
# ----------------------------
def add_patient():
    """Insert a new patient record."""
    name = name_entry.get().strip()
    dob = dob_entry.get().strip()       #YYYY-MM-DD
    contact = contact_entry.get().strip()
    history = history_entry.get().strip()
    
    if not name:
        messagebox.showwarning("Input Error", "Name is required.")
        return
    
    connection = get_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO Patients (name, dob, contact, medical_history)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, dob, contact, history))
        connection.commit()
        messagebox.showinfo("Success", "Patient added successfully!")
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        connection.close()
    
    clear_patient_form()
    show_patients()

def fetch_patients():
    """Get all patient records."""
    connection = get_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Patients;")
        records = cursor.fetchall()
        return records
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return []
    finally:
        connection.close()

def show_patients():
    """Populate the patient Treeview."""
    for row in patient_tree.get_children():
        patient_tree.delete(row)
    records = fetch_patients()
    for record in records:
        patient_tree.insert("", "end", values=record)

def clear_patient_form():
    """Clear patient input fields."""
    name_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    history_entry.delete(0, tk.END)

# ----------------------------
# MRI Scans Management Functions
# ----------------------------
def add_mri_scan():
    """Insert a new MRI scan record."""
    pid = patient_id_entry.get().strip()
    scan_date = scan_date_entry.get().strip()   #YYYY-MM-DD
    scan_type = scan_type_entry.get().strip()
    notes = scan_notes_entry.get().strip()
    dicom_path = dicom_entry.get().strip()
    
    if not pid:
        messagebox.showwarning("Input Error", "Patient ID is required.")
        return
    
    try:
        pid_int = int(pid)
    except ValueError:
        messagebox.showerror("Input Error", "Patient ID must be an integer.")
        return

    connection = get_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO MRI_Scans (patient_id, scan_date, scan_type, notes, dicom_file_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (pid_int, scan_date, scan_type, notes, dicom_path))
        connection.commit()
        messagebox.showinfo("Success", "MRI scan record added successfully!")
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        connection.close()
    
    clear_scan_form()
    show_mri_scans()

def fetch_mri_scans():
    """Retrieve all MRI scan records."""
    connection = get_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MRI_Scans;")
        records = cursor.fetchall()
        return records
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return []
    finally:
        connection.close()

def show_mri_scans():
    """Populate the MRI scans Treeview."""
    for row in scan_tree.get_children():
        scan_tree.delete(row)
    records = fetch_mri_scans()
    for record in records:
        scan_tree.insert("", "end", values=record)

def clear_scan_form():
    """Clear MRI scan input fields."""
    patient_id_entry.delete(0, tk.END)
    scan_date_entry.delete(0, tk.END)
    scan_type_entry.delete(0, tk.END)
    scan_notes_entry.delete(0, tk.END)
    dicom_entry.delete(0, tk.END)

def browse_dicom_file():
    """Browse and select a DICOM file."""
    filepath = filedialog.askopenfilename(title="Select DICOM File",
                                          filetypes=[("DICOM files", "*.dcm"), ("All files", "*.*")])
    if filepath:
        dicom_entry.delete(0, tk.END)
        dicom_entry.insert(0, filepath)

# ----------------------------
# Users Management Functions
# ----------------------------
def add_user():
    """Insert a new user record."""
    username = user_entry.get().strip()
    password = password_entry.get().strip()
    role = role_entry.get().strip()
    
    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password are required.")
        return

    # Hash the password (using sha256)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    connection = get_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO Users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, password_hash, role))
        connection.commit()
        messagebox.showinfo("Success", "User added successfully!")
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        connection.close()
    
    clear_user_form()
    show_users()

def fetch_users():
    """Retrieve all user records."""
    connection = get_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, role FROM Users;")
        records = cursor.fetchall()
        return records
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return []
    finally:
        connection.close()

def show_users():
    """Populate the users Treeview."""
    for row in user_tree.get_children():
        user_tree.delete(row)
    records = fetch_users()
    for record in records:
        user_tree.insert("", "end", values=record)

def clear_user_form():
    """Clear user input fields."""
    user_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    role_entry.delete(0, tk.END)

# ----------------------------
# Tkinter GUI Setup with Notebook
# ----------------------------
root = tk.Tk()
root.title("MRI Scan Management")
root.geometry("900x700")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# ----- Tab 1: Patients Management -----
patient_frame = tk.Frame(notebook)
notebook.add(patient_frame, text="Patients")

# Patient Input Form
patient_form = tk.Frame(patient_frame)
patient_form.pack(pady=10)

tk.Label(patient_form, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Label(patient_form, text="DOB (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(patient_form, text="Contact:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Label(patient_form, text="Medical History:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

name_entry = tk.Entry(patient_form, width=30)
dob_entry = tk.Entry(patient_form, width=30)
contact_entry = tk.Entry(patient_form, width=30)
history_entry = tk.Entry(patient_form, width=30)

name_entry.grid(row=0, column=1, padx=5, pady=5)
dob_entry.grid(row=1, column=1, padx=5, pady=5)
contact_entry.grid(row=2, column=1, padx=5, pady=5)
history_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(patient_form, text="Add Patient", command=add_patient).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(patient_form, text="Clear Form", command=clear_patient_form).grid(row=5, column=0, columnspan=2, pady=10)

# Patient Treeview
patient_tree_frame = tk.Frame(patient_frame)
patient_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

patient_columns = ("id", "name", "dob", "contact", "medical_history")
patient_tree = ttk.Treeview(patient_tree_frame, columns=patient_columns, show="headings")
for col in patient_columns:
    patient_tree.heading(col, text=col.capitalize())
    patient_tree.column(col, width=150, anchor='center')
patient_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Button(patient_frame, text="Load Patients", command=show_patients).pack(pady=10)

# ----- Tab 2: MRI Scans Management -----
scan_frame = tk.Frame(notebook)
notebook.add(scan_frame, text="MRI Scans")

# MRI Scan Input Form
scan_form = tk.Frame(scan_frame)
scan_form.pack(pady=10)

tk.Label(scan_form, text="Patient ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Label(scan_form, text="Scan Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(scan_form, text="Scan Type:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Label(scan_form, text="Notes:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Label(scan_form, text="DICOM File:").grid(row=4, column=0, sticky="e", padx=5, pady=5)

patient_id_entry = tk.Entry(scan_form, width=30)
scan_date_entry = tk.Entry(scan_form, width=30)
scan_type_entry = tk.Entry(scan_form, width=30)
scan_notes_entry = tk.Entry(scan_form, width=30)
dicom_entry = tk.Entry(scan_form, width=30)

patient_id_entry.grid(row=0, column=1, padx=5, pady=5)
scan_date_entry.grid(row=1, column=1, padx=5, pady=5)
scan_type_entry.grid(row=2, column=1, padx=5, pady=5)
scan_notes_entry.grid(row=3, column=1, padx=5, pady=5)
dicom_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Button(scan_form, text="Browse DICOM", command=browse_dicom_file).grid(row=4, column=2, padx=5, pady=5)
tk.Button(scan_form, text="Add MRI Scan", command=add_mri_scan).grid(row=5, column=0, columnspan=3, pady=10)

# MRI Scan Treeview
scan_tree_frame = tk.Frame(scan_frame)
scan_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scan_columns = ("id", "patient_id", "scan_date", "scan_type", "notes", "dicom_file_path")
scan_tree = ttk.Treeview(scan_tree_frame, columns=scan_columns, show="headings")
for col in scan_columns:
    scan_tree.heading(col, text=col.capitalize())
    scan_tree.column(col, width=130, anchor='center')
scan_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Button(scan_frame, text="Load MRI Scans", command=show_mri_scans).pack(pady=10)

# ----- Tab 3: Users Management -----
user_frame = tk.Frame(notebook)
notebook.add(user_frame, text="Users")

# User Input Form
user_form = tk.Frame(user_frame)
user_form.pack(pady=10)

tk.Label(user_form, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Label(user_form, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(user_form, text="Role:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

user_entry = tk.Entry(user_form, width=30)
password_entry = tk.Entry(user_form, width=30, show="*")
role_entry = tk.Entry(user_form, width=30)

user_entry.grid(row=0, column=1, padx=5, pady=5)
password_entry.grid(row=1, column=1, padx=5, pady=5)
role_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(user_form, text="Add User", command=add_user).grid(row=3, column=0, columnspan=2, pady=10)

# Users Treeview
user_tree_frame = tk.Frame(user_frame)
user_tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

user_columns = ("id", "username", "role")
user_tree = ttk.Treeview(user_tree_frame, columns=user_columns, show="headings")
for col in user_columns:
    user_tree.heading(col, text=col.capitalize())
    user_tree.column(col, width=150, anchor='center')
user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Button(user_frame, text="Load Users", command=show_users).pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
