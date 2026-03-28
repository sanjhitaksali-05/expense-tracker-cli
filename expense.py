import json
import csv
from datetime import datetime

FILE = "data/expenses.json"

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    try:
        amount = float(input("Enter amount: "))
    except:
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
    data = load_data()
    if not data:
        print("No expenses found.")
        return

    for i, exp in enumerate(data):
        print(i, exp)

def category_summary():
    data = load_data()
    summary = {}

    for exp in data:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]

    print("\nCategory Summary:")
    for k, v in summary.items():
        print(k, ":", v)

def monthly_total():
    data = load_data()
    month = input("Enter month (YYYY-MM): ")

    total = sum(exp["amount"] for exp in data if exp["date"].startswith(month))
    print("Total for month:", total)

def delete_expense():
    data = load_data()
    view_expenses()

    try:
        idx = int(input("Enter index to delete: "))
        data.pop(idx)
        save_data(data)
        print("Deleted!")
    except:
        print("Invalid input")

def filter_expenses():
    data = load_data()
    print("1. Filter by Category")
    print("2. Filter by Date")
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
    data = load_data()
    summary = {}

    for exp in data:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]

    if summary:
        top = max(summary, key=summary.get)
        print("Top spending category:", top, "Amount:", summary[top])
    else:
        print("No data")

def export_csv():
    data = load_data()

    with open("export.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["amount", "category", "date"])
        writer.writeheader()
        writer.writerows(data)

    print("Exported to export.csv")
