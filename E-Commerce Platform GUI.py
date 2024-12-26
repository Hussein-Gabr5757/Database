import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

connection = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=HUSSIEN-GABR;"  
    "Database=E-CommercePlatform;"  
    "Trusted_Connection=yes;"
)


def get_tables():
    cursor = connection.cursor()
    cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_type = 'BASE TABLE' 
    AND table_name != 'sysdiagrams'
    """)
    tables = cursor.fetchall()
    return [table[0] for table in tables]


def show_columns(table_name):
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    AND COLUMNPROPERTY(OBJECT_ID('{table_name}'), COLUMN_NAME, 'IsIdentity') = 0
    """)
    columns = cursor.fetchall()

    
    for widget in input_frame.winfo_children():
        widget.destroy()

    
    global entry_widgets
    entry_widgets = []  
    row = 0
    for column in columns:
        label = tk.Label(input_frame, text=column[0], bg="#f9f9f9", fg="#333333", font=("Arial", 10))
        label.grid(row=row, column=0, padx=10, pady=5)
        entry = tk.Entry(input_frame)
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry_widgets.append(entry)
        row += 1

def on_table_select(event):
    try:
        selected_table = table_listbox.get(table_listbox.curselection())
        cursor = connection.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}'")
        columns = [row[0] for row in cursor.fetchall()]
        
        for widget in input_frame.winfo_children():
            widget.destroy()
        
        entry_widgets.clear()  
        column_labels.clear()
        
        for col in columns:
            label = tk.Label(input_frame, text=col, bg="#f9f9f9", fg="#333333", font=("Arial", 10))
            label.pack(anchor="w", padx=5, pady=2)
            entry = tk.Entry(input_frame, width=30)
            entry.pack(padx=5, pady=2)
            column_labels.append(col)
            entry_widgets.append(entry)
        
        save_button = tk.Button(input_frame, text="Save", bg="#4a90e2", fg="white", command=lambda: save_data(selected_table))
        save_button.pack(pady=10)
        
        show_data_button = tk.Button(input_frame, text="Show Data", bg="#4a90e2", fg="white", command=lambda: display_table_data(selected_table))
        show_data_button.pack(pady=10)
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load columns:\n{e}")


def save_data(table_name):
    try:
        values = [entry.get() for entry in entry_widgets]
        cursor = connection.cursor()
        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(column_labels)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", f"Data successfully inserted into {table_name}.")
        display_table_data(table_name)  # تحديث عرض البيانات
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert data:\n{e}")


def display_table_data(table_name):
    for widget in data_frame.winfo_children():
        widget.destroy()
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    tree = ttk.Treeview(data_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    
    for row in rows:
        tree.insert("", "end", values=row)


root = tk.Tk()
root.title("Database Manager")
root.geometry("1000x700")
root.configure(bg="#f3f4f6")

table_frame = tk.Frame(root, bg="#f3f4f6")
table_frame.pack(side="left", fill="y", padx=10, pady=10)

table_label = tk.Label(table_frame, text="Tables", bg="#4a90e2", fg="white", font=("Arial", 12, "bold"))
table_label.pack(fill="x")

table_listbox = tk.Listbox(table_frame, bg="white", fg="#333333", font=("Arial", 10))
table_listbox.pack(fill="y", expand=True, padx=5, pady=5)

tables = get_tables()
for table in tables:
    table_listbox.insert(tk.END, table)

table_listbox.bind("<<ListboxSelect>>", on_table_select)

input_frame = tk.Frame(root, bg="#f9f9f9", bd=2, relief="sunken")
input_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

input_label = tk.Label(input_frame, text="Enter Values for Table", bg="#4a90e2", fg="white", font=("Arial", 12, "bold"))
input_label.pack(fill="x")

entry_widgets = []
column_labels = []

data_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
data_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

data_label = tk.Label(data_frame, text="Table Data", bg="#4a90e2", fg="white", font=("Arial", 12, "bold"))
data_label.pack(fill="x")

root.mainloop()
