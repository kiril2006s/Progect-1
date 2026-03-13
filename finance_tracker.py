import json
from datetime import datetime

DATA_FILE = "data.json"

# ---------- Робота з файлом ----------
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {"budget": 0, "expenses": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ---------- Команди ----------
def set_budget(data):
    budget = float(input("Введіть суму бюджету: "))
    data["budget"] = budget
    save_data(data)
    print("Бюджет встановлено!")

def add_expense(data):
    amount = float(input("Сума: "))
    category = input("Категорія: ")
    date = input("Дата (YYYY-MM-DD): ")
    comment = input("Коментар (необов'язково): ")

    expense = {
        "amount": amount,
        "category": category,
        "date": date,
        "comment": comment
    }

    data["expenses"].append(expense)
    save_data(data)

    print("Витрату додано!")

    check_budget(data)

def show_expenses(data):
    if not data["expenses"]:
        print("Немає витрат.")
        return

    for e in data["expenses"]:
        print(f"{e['date']} | {e['category']} | {e['amount']} грн | {e['comment']}")

def show_by_date(data):
    date = input("Введіть дату (YYYY-MM-DD): ")

    for e in data["expenses"]:
        if e["date"] == date:
            print(f"{e['date']} | {e['category']} | {e['amount']} грн | {e['comment']}")

def show_by_period(data):
    start = input("Початкова дата (YYYY-MM-DD): ")
    end = input("Кінцева дата (YYYY-MM-DD): ")

    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    for e in data["expenses"]:
        d = datetime.strptime(e["date"], "%Y-%m-%d")

        if start <= d <= end:
            print(f"{e['date']} | {e['category']} | {e['amount']} грн | {e['comment']}")

def show_by_category(data):
    cat = input("Введіть категорію: ")

    for e in data["expenses"]:
        if e["category"].lower() == cat.lower():
            print(f"{e['date']} | {e['category']} | {e['amount']} грн | {e['comment']}")

def show_balance(data):
    total = sum(e["amount"] for e in data["expenses"])
    balance = data["budget"] - total

    print("Залишок:", balance, "грн")

def check_budget(data):
    total = sum(e["amount"] for e in data["expenses"])

    if total > data["budget"]:
        print("⚠ УВАГА! Ви перевищили бюджет!")

def report_by_category(data):
    report = {}

    for e in data["expenses"]:
        cat = e["category"]
        report[cat] = report.get(cat, 0) + e["amount"]

    print("Звіт по категоріях:")

    for cat, total in report.items():
        print(cat, ":", total, "грн")

def help_menu():
    print("""
Доступні команди:
допомога
встановити бюджет
додати витрату
показати витрати
витрати дата
витрати період
витрати категорія
залишок
звіт за категоріями
вийти
""")

# ---------- Головна програма ----------
def main():
    data = load_data()

    print("Вітаємо у боті 'Фінансовий трекер студента'!")

    while True:
        command = input("\nВведіть команду: ").lower()

        if command == "допомога":
            help_menu()

        elif command == "встановити бюджет":
            set_budget(data)

        elif command == "додати витрату":
            add_expense(data)

        elif command == "показати витрати":
            show_expenses(data)

        elif command == "витрати дата":
            show_by_date(data)

        elif command == "витрати період":
            show_by_period(data)

        elif command == "витрати категорія":
            show_by_category(data)

        elif command == "залишок":
            show_balance(data)

        elif command == "звіт за категоріями":
            report_by_category(data)

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда. Напишіть 'допомога'.")

main()
