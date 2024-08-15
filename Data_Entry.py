from datetime import datetime #This class allows us to work with dates in Python.

def get_Date(prompt, allow_default=False): #This is a boolean value (True or False) that specifies whether to allow an empty input to return the current date. Defaults to False
    date_str = input(prompt) #asks the user for the input for the date column. Stores it in the date_str variable
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")
   
    #If allow_default is True and the user enters nothing (not date_str), the function returns the current date formatted as "dd-mm-yyyy" using datetime.today().strftime("%d-%m-%Y").
    #If the user entered a date or allow_default is False, the code tries to convert the date_str into a valid date object using datetime.strptime(date_str, "%d-%m-%Y"). This assumes the user entered the date in the format "dd-mm-yyyy" (e.g., 14-08-2024).

    try:
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_Date(prompt, allow_default)
 # If there's an error (except ValueError), the code prints a message asking the user to enter the date in the correct format ("dd-mm-yyyy").
 #  After the error message, the function calls itself again (return get_Date(prompt, allow_default)) to give the user another chance to enter a valid date. 
 # This creates a loop until a valid date is entered.


def get_Amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative, non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_Amount()
# So first we are trying to take an input from the user, handling the error as the number shuld be non-Neg and non-zero.
# Lastly, the user gets into a loop until the amount is correctly entred.


Categories = {"I" : "Income", "E" : "Expense"}
def get_Category():
    while True:
        category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
        if category in Categories:
            return Categories[category]
        print("Invalid category. Please enter 'I' for Income and 'E' for Expense.")



def get_Description():
    #Prompts user for a description (optional).

    #Returns:
    #str: The entered description or an empty string if nothing is entered.
    
    return input("Enter a description (Optional): ")