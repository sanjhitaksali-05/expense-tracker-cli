import json

FILE = "data/budget.json"

def set_budget():
    try:
        amount = float(input("Enter monthly budget: "))
    except:
        print("Invalid input")
        return

    with open(FILE, "w") as f:
        json.dump({"budget": amount}, f)

    print("Budget set!")

def check_budget():
    try:
        with open(FILE, "r") as f:
            budget = json.load(f)["budget"]
    except:
        return

    from expense import load_data
    total = sum(exp["amount"] for exp in load_data())

    if total > budget:
        print("⚠ Budget exceeded!")
