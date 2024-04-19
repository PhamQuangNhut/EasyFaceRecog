import tkinter as tk
from tkinter import ttk
from Controller.EmployeeController import EmployeeController
from Model.model import get_session, face_embs
import config
class EmployeeApp:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Employee Management")

        # Search frame
        self.search_frame = ttk.Frame(self.root)
        self.search_frame.pack(fill=tk.X, padx=10, pady=10)

# Configure style
        style = ttk.Style()
        style.configure("Treeview", background="#f0f0f0", fieldbackground="#f0f0f0")
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), foreground='black')
        style.configure("Treeview.Separator", background="#333333")  # Set a dark separator color
        
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        self.search_entry.bind("<Return>", self.search)  # Bind the Enter key to search

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT)

        # Treeview frame
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "Phone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.column("ID", width=50, anchor="center")  # Set the width and alignment of the ID column
        self.tree.column("Name", anchor="center")  # Center-align the Name column
        self.tree.column("Phone", anchor="center")  # Center-align the Phone column
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Populate table
        self.populate_table()

    def search(self):
        search_query = self.search_entry.get()
        employees = self.controller.get_employee_by_full_name(search_query) + self.controller.get_employee_by_number(search_query)
        employees = set(employees)
        employees = list(employees)
        self.populate_table(employees)

    def populate_table(self, employees=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if employees is None:
            employees = self.controller.get_all_employees()
        for employee in employees:
            self.tree.insert('', 'end', values=(employee.id, employee.full_name, employee.number))
session = get_session(config.SQLITE_DB_PATH)
e_controller = EmployeeController(session, face_embs)
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root, EmployeeController(session, face_embs))
    root.mainloop()
