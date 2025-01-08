import tkinter as tk
from tkinter import ttk, messagebox
from budget_manager import BudgetManager
from storage import load_data, save_data

class BudgetApp:
    def __init__(self):
        self.manager = BudgetManager()
        # Load data from storage
        income, expenses = load_data()
        self.manager.set_income(income)
        self.manager.expenses = expenses

        # Create main window
        self.root = tk.Tk()
        self.root.title("Personal Finance Manager")
        self.root.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):
        """Create the main GUI components."""
        # Income Section
        tk.Label(self.root, text="Total Income:").grid(row=0, column=0, padx=10, pady=10)
        self.income_entry = tk.Entry(self.root, width=20)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10)
        self.income_entry.insert(0, str(self.manager.income))
        tk.Button(self.root, text="Set Income", command=self.set_income).grid(row=0, column=2, padx=10, pady=10)

        # Add Expense Section
        tk.Label(self.root, text="Category:").grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(self.root, width=20)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root, width=20)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Description:").grid(row=3, column=0, padx=10, pady=10)
        self.description_entry = tk.Entry(self.root, width=20)
        self.description_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=3, column=2, padx=10, pady=10)

        # Expenses Table
        columns = ("Category", "Amount", "Description")
        self.expenses_table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.expenses_table.heading("Category", text="Category")
        self.expenses_table.heading("Amount", text="Amount")
        self.expenses_table.heading("Description", text="Description")
        self.expenses_table.column("Category", width=150)
        self.expenses_table.column("Amount", width=100)
        self.expenses_table.column("Description", width=200)
        self.expenses_table.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Remaining Budget
        self.remaining_label = tk.Label(self.root, text="Remaining Budget: $0.00", font=("Arial", 14))
        self.remaining_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Delete Button
        tk.Button(self.root, text="Delete Expense", command=self.delete_expense).grid(row=6, column=0, columnspan=3, pady=10)

        self.update_expenses_table()
        self.update_remaining_budget()

    def set_income(self):
        """Set the total income."""
        try:
            income = float(self.income_entry.get())
            self.manager.set_income(income)
            self.update_remaining_budget()
            save_data(self.manager.income, self.manager.expenses)
            messagebox.showinfo("Success", "Income updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid income value.")

    def add_expense(self):
        """Add a new expense."""
        try:
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            if not category:
                raise ValueError("Category cannot be empty.")
            self.manager.add_expense(category, amount, description)
            self.update_expenses_table()
            self.update_remaining_budget()
            save_data(self.manager.income, self.manager.expenses)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def delete_expense(self):
        """Delete the selected expense."""
        selected_item = self.expenses_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected.")
            return
        index = self.expenses_table.index(selected_item[0])
        self.manager.delete_expense(index)
        self.update_expenses_table()
        self.update_remaining_budget()
        save_data(self.manager.income, self.manager.expenses)
        messagebox.showinfo("Success", "Expense deleted successfully!")

    def update_expenses_table(self):
        """Update the expenses table with the latest data."""
        for row in self.expenses_table.get_children():
            self.expenses_table.delete(row)
        for expense in self.manager.expenses:
            self.expenses_table.insert("", "end", values=(expense["category"], f"${expense['amount']:.2f}", expense["description"]))

    def update_remaining_budget(self):
        """Update the remaining budget display."""
        remaining_budget = self.manager.get_remaining_budget()
        self.remaining_label.config(text=f"Remaining Budget: ${remaining_budget:.2f}")

    def run(self):
        """Run the application."""
        self.root.mainloop()
