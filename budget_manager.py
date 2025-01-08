class BudgetManager:
    def __init__(self):
        self.income = 0
        self.expenses = []

    def set_income(self, amount):
        """Set the user's income."""
        self.income = amount

    def add_expense(self, category, amount, description):
        """Add a new expense."""
        self.expenses.append({"category": category, "amount": amount, "description": description})

    def delete_expense(self, index):
        """Delete an expense by its index."""
        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)

    def get_remaining_budget(self):
        """Calculate the remaining budget."""
        total_expenses = sum(expense["amount"] for expense in self.expenses)
        return self.income - total_expenses
