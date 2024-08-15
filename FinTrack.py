import pandas as pd
import csv
from datetime import datetime
from Data_Entry import get_Amount, get_Category, get_Date, get_Description
import matplotlib.pyplot as plt

# This class handles all the operations related to the CSV file.
class CSV:
    # Class attributes: File name and column names used in the CSV file
    CSV_FILE = "KharchaBook.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]
    FORMAT = "%d-%m-%Y"  # Date format used throughout the program

    @classmethod
    def initialize_csv(cls):
        """
        This method checks if the CSV file exists. If not, it creates the file with the specified columns.
        """
        try:
            pd.read_csv(cls.CSV_FILE)  # Try to read the CSV file
        except FileNotFoundError:
            # If the file doesn't exist, create it with the specified columns
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)  # Save the empty DataFrame to a CSV file

    @classmethod
    def add_entry(cls, Date, Amount, Category, Description):
        """
        This method adds a new transaction to the CSV file.
        Parameters:
        - Date: The date of the transaction
        - Amount: The amount of money involved
        - Category: The type of transaction (e.g., Income, Expense)
        - Description: Details about the transaction
        """
        # Create a dictionary for the new transaction
        new_entry = {
            "Date": Date,
            "Amount": Amount,
            "Category": Category,
            "Description": Description,
        }
        # Open the CSV file in append mode to add the new entry
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)  # Write the new entry to the CSV file
        print("Transaction added successfully")  # Confirmation message

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        This method retrieves transactions within a specified date range.
        Parameters:
        - start_date: The beginning of the date range
        - end_date: The end of the date range
        Returns:
        - A filtered DataFrame containing transactions within the date range
        """
        # Read the CSV file into a DataFrame
        df = pd.read_csv(cls.CSV_FILE)
        # Convert the "Date" column to datetime format using the specified format
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT)
        # Convert the start and end dates to datetime objects
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Create a boolean mask to filter rows within the date range
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]  # Apply the mask to get the filtered DataFrame

        # Check if the filtered DataFrame is empty
        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            # Display the filtered transactions
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            # Calculate and display the summary: total income, total expense, and net savings
            total_income = filtered_df[filtered_df["Category"] == "Income"][
                "Amount"
            ].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"][
                "Amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df  # Return the filtered DataFrame for further use

# This function collects transaction details from the user and adds them to the CSV file.
def add():
    CSV.initialize_csv()  # Ensure the CSV file is initialized
    # Get transaction details from the user using imported functions
    Date = get_Date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    Amount = get_Amount()
    Category = get_Category()
    Description = get_Description()
    # Add the new entry to the CSV file
    CSV.add_entry(Date, Amount, Category, Description)

# This function plots income and expenses over time using the filtered DataFrame.
def plot_transactions(df):
    # Set the "Date" column as the index for the DataFrame
    df.set_index("Date", inplace=True)

    # Create separate DataFrames for income and expenses, resampled by day
    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    # Plot the income and expenses on a graph
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()  # Display the plot

# This is the main function that runs the financial tracking program.
def FinTrack():
    while True:  # Infinite loop to keep the program running
        # Display menu options to the user
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        # Handle user input based on their choice
        if choice == "1":
            add()  # Call the add() function to add a new transaction
        elif choice == "2":
            # Get the date range from the user and fetch transactions within that range
            start_date = get_Date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_Date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            # Optionally, plot the transactions if the user wants
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")  # Exit the program
            break  # Break the loop to stop the program
        else:
            print("Invalid choice. Enter 1, 2 or 3.")  # Handle invalid input

# This condition ensures the program runs only if it is executed directly (not imported).
if __name__ == "__FinTrack__":
    FinTrack()