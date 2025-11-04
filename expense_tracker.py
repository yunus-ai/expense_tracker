import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Step 1: Create or Load Expense Data
try:
    df = pd.read_csv("expenses.csv")
    print("✅ Loaded existing expense data.")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    print("🆕 No existing data found. Creating a new file.")


# Step 2: Add New Expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if date.strip() == "":
        date = datetime.date.today().strftime("%Y-%m-%d")

    category = input("Enter category (Food, Transport, Shopping, etc.): ")
    amount = float(input("Enter Amount: "))
    description = input("Enter description: ")

    new_entry = pd.DataFrame([[date, category, amount, description]],
                             columns=["Date", "Category", "Amount", "Description"])
    global df
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv("expenses.csv", index=False)
    print("✅ Expense added successfully!")


# Step 3: Analyze Data
def analyze_expenses():
    print("\n📊 Expense Summary:")
    print(df.groupby("Category")["Amount"].sum())
    print("\n💰 Total Spent:", df["Amount"].sum())


# Step 4: Plot Data
def plot_expenses():
    category_sum = df.groupby("Category")["Amount"].sum()
    category_sum.plot(kind="pie", autopct="%1.1f%%", figsize=(6, 6))
    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.savefig("expense_chart.png")
    plt.show()


# Step 5: Delete Expense
def delete_expense():
    global df
    if df.empty:
        print("No expenses to delete.")
        return

    print("\n Current Expenses:")
    print(df.reset_index())

    try:
        index_to_delete = int(input("\nEnter the index of the expense you want to delete: "))
        if 0 <= index_to_delete < len(df):
            deleted_row = df.iloc[index_to_delete]
            df = df.drop(index_to_delete).reset_index(drop=True)
            df.to_csv("expenses.csv", index=False)
            print(f"✅ Deleted: {deleted_row['Description']} ({deleted_row['Category']} - ₹{deleted_row['Amount']})")
        else:
            print("❌ Invalid index. Please enter a valid number.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")


# Step 6: Menu
while True:
    print("\n--- Expense Tracker Menu ---")
    print("1. Add Expense")
    print("2. View Summary")
    print("3. Plot Chart")
    print("4. Delete Expense")
    print("5. Exit")

    choice = input("Choose an option (1–5): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        analyze_expenses()
    elif choice == "3":
        plot_expenses()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        print("👋 Exiting... Data saved to expenses.csv")
        break
    else:
        print("❌ Invalid choice. Try again.")
