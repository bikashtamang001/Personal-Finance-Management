import json

FILE_NAME = "budget.json"

def load_data():
    """Load budget data from a file."""
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data.get("income", 0), data.get("expenses", [])
    except FileNotFoundError:
        return 0, []

def save_data(income, expenses):
    """Save budget data to a file."""
    with open(FILE_NAME, "w") as file:
        json.dump({"income": income, "expenses": expenses}, file, indent=4)
