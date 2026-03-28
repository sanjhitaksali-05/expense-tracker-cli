from expense import (
    add_expense, view_expenses, category_summary,
    monthly_total, delete_expense, filter_expenses,
    top_category, export_csv
)
from budget import set_budget, check_budget

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
