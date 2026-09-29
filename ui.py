import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from assignments import (
    create_assignment,
    get_status,
    is_valid_date,
    search_assignments
)
from storage import load_assignments, save_assignments
from utils import get_statistics


class AssignmentTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Tracker")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        self.assignments = load_assignments()

        self.create_interface()
        self.refresh_list()

    def create_interface(self):
        tk.Label(
            self.root,
            text="ASSIGNMENT TRACKER",
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Keep track of your college assignments",
            font=("Arial", 11)
        ).pack(pady=(0, 15))

        top = tk.Frame(self.root)
        top.pack(pady=5)

        tk.Button(
            top, text="Add Assignment",
            command=self.add_assignment, width=18
        ).pack(side="left", padx=5)

        tk.Button(
            top, text="Mark Completed",
            command=self.mark_completed, width=18
        ).pack(side="left", padx=5)

        tk.Button(
            top, text="Delete",
            command=self.delete_assignment, width=12
        ).pack(side="left", padx=5)

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame, text="Search",
            command=self.search
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame, text="Show All",
            command=self.refresh_list
        ).pack(side="left", padx=5)

        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=5)

        columns = ("title", "subject", "deadline", "priority", "status")

        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=14
        )

        headings = {
            "title": "Assignment",
            "subject": "Subject",
            "deadline": "Deadline",
            "priority": "Priority",
            "status": "Status"
        }

        widths = {
            "title": 220,
            "subject": 130,
            "deadline": 110,
            "priority": 90,
            "status": 110
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column])

        self.tree.pack(side="left")

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.stats_label = tk.Label(
            self.root, text="", font=("Arial", 11, "bold")
        )
        self.stats_label.pack(pady=15)

        self.status_label = tk.Label(
            self.root, text="Status: Ready", font=("Arial", 10)
        )
        self.status_label.pack(side="bottom", pady=10)

    def add_assignment(self):
        window = tk.Toplevel(self.root)
        window.title("Add Assignment")
        window.geometry("430x430")
        window.resizable(False, False)

        entries = {}

        fields = [
            ("Title", "title"),
            ("Subject", "subject"),
            ("Deadline (DD-MM-YYYY)", "deadline")
        ]

        for row, (label, key) in enumerate(fields):
            tk.Label(window, text=label).grid(
                row=row, column=0, padx=10, pady=10, sticky="w"
            )
            entry = tk.Entry(window, width=32)
            entry.grid(row=row, column=1, padx=10, pady=10)
            entries[key] = entry

        tk.Label(window, text="Priority").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        priority = ttk.Combobox(
            window,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=29
        )
        priority.set("Medium")
        priority.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(window, text="Description").grid(
            row=4, column=0, padx=10, pady=10, sticky="nw"
        )

        description = tk.Text(window, width=30, height=6)
        description.grid(row=4, column=1, padx=10, pady=10)

        def save_new():
            title = entries["title"].get()
            subject = entries["subject"].get()
            deadline = entries["deadline"].get()

            if not title or not subject or not deadline:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter title, subject and deadline."
                )
                return

            if not is_valid_date(deadline):
                messagebox.showwarning(
                    "Invalid Date",
                    "Use DD-MM-YYYY."
                )
                return

            assignment = create_assignment(
                title,
                subject,
                deadline,
                priority.get(),
                description.get("1.0", "end")
            )

            self.assignments.append(assignment)

            if save_assignments(self.assignments):
                self.refresh_list()
                self.status_label.config(
                    text="Status: Assignment added"
                )
                window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Could not save the assignment."
                )

        tk.Button(
            window,
            text="Save Assignment",
            command=save_new,
            width=20
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def get_selected_index(self):
        selected = self.tree.selection()

        if not selected:
            return None

        return self.tree.index(selected[0])

    def mark_completed(self):
        index = self.get_selected_index()

        if index is None:
            messagebox.showwarning(
                "Select Assignment",
                "Please select an assignment first."
            )
            return

        self.assignments[index]["status"] = "Completed"

        if save_assignments(self.assignments):
            self.refresh_list()
            self.status_label.config(
                text="Status: Assignment completed"
            )

    def delete_assignment(self):
        index = self.get_selected_index()

        if index is None:
            messagebox.showwarning(
                "Select Assignment",
                "Please select an assignment first."
            )
            return

        if not messagebox.askyesno(
            "Delete Assignment",
            "Are you sure you want to delete this assignment?"
        ):
            return

        self.assignments.pop(index)

        if save_assignments(self.assignments):
            self.refresh_list()
            self.status_label.config(
                text="Status: Assignment deleted"
            )

    def search(self):
        results = search_assignments(
            self.assignments,
            self.search_entry.get()
        )
        self.display_assignments(results)

    def display_assignments(self, assignments):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for assignment in assignments:
            self.tree.insert(
                "",
                "end",
                values=(
                    assignment["title"],
                    assignment["subject"],
                    assignment["deadline"],
                    assignment["priority"],
                    get_status(assignment)
                )
            )

        self.update_statistics(assignments)

    def refresh_list(self):
        self.display_assignments(self.assignments)

    def update_statistics(self, assignments):
        total, completed, pending, overdue = get_statistics(assignments)

        self.stats_label.config(
            text=(
                f"Total: {total}    "
                f"Completed: {completed}    "
                f"Pending: {pending}    "
                f"Overdue: {overdue}"
            )
        )


def start_app():
    root = tk.Tk()
    AssignmentTracker(root)
    root.mainloop()
