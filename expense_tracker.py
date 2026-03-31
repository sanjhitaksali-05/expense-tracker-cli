import json
import csv
from datetime import datetime
import os

# Configuration: Ensure the data directory exists
DATA_DIR = "data"
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.json")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.json")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- UTILS LOGIC ---
def validate_float(value):
    """Helper to safely convert strings to floats."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

# --- EXPENSE LOGIC ---
def load_data():
    """Loads expenses from the JSON file."""
    try:
        with open(EXPENSE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Saves expenses to the JSON file."""
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    """Prompts user for expense details and saves them."""
    amount_input = input("Enter amount: ")
    amount = validate_float(amount_input)
    if amount is None:
        print("Invalid amount")
        return

    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    data = load_data()
    data.append({
        "amount": amount,
        "category": category,
        "date": date
    })
    save_data(data)
    print("Expense added!")

def view_expenses():
    """Displays all recorded expenses."""
    data = load_data()
    if not data:
        print("No expenses found.")
        return
    for i, exp in enumerate(data):
        print(f"{i}: {exp}")

def category_summary():
    """Prints total spending per category."""
    data = load_data()
    summary = {}
    for exp in data:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
    
    print("\nCategory Summary:")
    for k, v in summary.items():
        print(f"{k} : {v}")

def monthly_total():
    """Calculates total spending for a specific month (YYYY-MM)."""
    data = load_data()
    month = input("Enter month (YYYY-MM): ")
    total = sum(exp["amount"] for exp in data if exp["date"].startswith(month))
    print(f"Total for month {month}: {total}")

def delete_expense():
    """Deletes an expense by its list index."""
    data = load_data()
    view_expenses()
    try:
        idx = int(input("Enter index to delete: "))
        data.pop(idx)
        save_data(data)
        print("Deleted!")
    except (ValueError, IndexError):
        print("Invalid input")

def filter_expenses():
    """Filters data by category or specific date."""
    data = load_data()
    print("1. Filter by Category\n2. Filter by Date")
    choice = input("Choose: ")
    if choice == "1":
        cat = input("Enter category: ")
        result = [exp for exp in data if exp["category"] == cat]
    elif choice == "2":
        date = input("Enter date (YYYY-MM-DD): ")
        result = [exp for exp in data if exp["date"] == date]
    else:
        print("Invalid choice")
        return
    for exp in result:
        print(exp)

def top_category():
    """Identifies the category with the highest total spending."""
    data = load_data()
    summary = {}
    for exp in data:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
    if summary:
        top = max(summary, key=summary.get)
        print(f"Top spending category: {top} Amount: {summary[top]}")
    else:
        print("No data")

def export_csv():
    """Exports all expenses to a CSV file."""
    data = load_data()
    with open("export.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["amount", "category", "date"])
        writer.writeheader()
        writer.writerows(data)
    print("Exported to export.csv")

# --- BUDGET LOGIC --- 
def set_budget():
    """Sets the monthly budget limit."""
    amount_input = input("Enter monthly budget: ")
    amount = validate_float(amount_input)
    if amount is None:
        print("Invalid input")
        return
    with open(BUDGET_FILE, "w") as f:
        json.dump({"budget": amount}, f)
    print("Budget set!")

def check_budget():
    """Checks total spending against the set budget."""
    try:
        with open(BUDGET_FILE, "r") as f:
            budget = json.load(f)["budget"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return

    total = sum(exp["amount"] for exp in load_data())
    if total > budget:
        print(f"⚠ Budget exceeded! (Total: {total}, Budget: {budget})")

# --- MAIN INTERFACE ---
def menu():
    print("\n====== Expense Tracker CLI ======")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Category Summary")
    print("4. Monthly Total")
    print("5. Set Budget")
    print("6. Delete Expense")
    print("7. Filter Expenses")
    print("8. Top Spending Category")
    print("9. Export to CSV")
    print("10. Exit")

def main():
    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            monthly_total()
        elif choice == "5":
            set_budget()
        elif choice == "6":
            delete_expense()
        elif choice == "7":
            filter_expenses()
        elif choice == "8":
            top_category()
        elif choice == "9":
            export_csv()
        elif choice == "10":
            break
        else:
            print("Invalid choice!")

        check_budget()

if __name__ == "__main__":
    main()
