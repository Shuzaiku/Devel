import sqlite3
import random

# Set up database cursor
connection = sqlite3.connect("shipping.db")
cursor = connection.cursor()

# Helper methods
def get_query(command: str) -> str:
    query = cursor.execute(command)
    fetch = query.fetchall()
    if not len(fetch):
        return None

    result = fetch[0][0]
    return result


def get_int(prompt: str) -> int:
    user_input: int

    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except:
            print("Input must be a number. Please try again:")


def get_confirmation(prompt: str) -> bool:
    user_input: str

    while True:
        user_input = input(prompt + " (y/n) ")
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please try again:")

# Login
print("LOG IN")
username = input("Username: ")
while not get_query(f"SELECT name FROM users WHERE name IS '{username}'"):
    username = input(f"User '{username}' not found. Please try again:\n")

valid_password = get_query(f"SELECT password FROM users WHERE name IS '{username}'")
password = input("Password: ")
attempts = 1
while valid_password != password:
    if attempts >= 3:
        print("Too many attempts were made. User has been locked out.")
        quit()

    password = input("Incorrect password, please try again:\n")
    attempts += 1

print("Successful log in!")

# Actions
def get_valid_action_number() -> int:
    invalid_message = "Invalid input. Please try again:"
    while True:
        action_num = get_int(
            "Which action would you like to take?\n"+
            "1. Send package\n2. Log out\n"+
            "Action number: "
        )
        
        if action_num < 1 or action_num > 2:
            print(invalid_message)
        else:
            return action_num

def get_current_balance(to_check=username) -> int:
    curr_balance = int(get_query(
        "SELECT balance "+
        "FROM users "+
        f"WHERE name = '{to_check}'"
    ))
    return curr_balance


def remove_money(amount: int) -> bool:
    curr_balance = get_current_balance()

    if curr_balance < amount or amount < 0:
        return False

    cursor.execute(
        "UPDATE users "+
        f"SET balance = {curr_balance - amount} "+
        f"WHERE name = '{username}'"
    )
    return True


def log_out():
    print("Bye bye!")
    connection.commit()
    print("Data has been saved.")
    quit()


def send_package():
    recipient = input("Recipient username: ")
    if not get_query(f"SELECT * FROM users WHERE name = '{recipient}'"):
        print("User not found in database.")
        return
    
    # Calculate cost
    weight = get_int("Package weight (kg): ")
    if weight < 0:
        print("Invalid number.")
        return

    balance = get_current_balance()
    cost = 2 * weight

    if cost > balance:
        print("You do not have sufficient balance to cover the delivery cost.")
        return
    
    # Confirm transaction
    print(f"Amount to pay: ${cost}")
    confirmation = get_confirmation("Do you wish to proceed?")
    if confirmation:
        new_balance = balance - cost

        remove_money(cost)

        print("Transaction complete.")
        print(f"Current balance: ${new_balance}")
        print(f"Package number: {random.randint(0, 9999)}")
        print(f"Recipient: {recipient}")

    else:
        print("Transaction cancelled.")
    
    if not get_confirmation("Do you wish to perform another operation?"):
        log_out()


actions = [send_package, log_out]

# Menu
while True:
    action = get_valid_action_number()
    actions[action-1]()