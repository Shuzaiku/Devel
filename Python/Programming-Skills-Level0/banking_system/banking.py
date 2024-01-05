import sqlite3

# Set up database cursor
connection = sqlite3.connect("banking.db")
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
            "1. Deposit\n2. Withdraw\n3. View\n4. Transfer\n5. Log out\n"+
            "Action number: "
        )
        
        if action_num < 1 or action_num > 5:
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


def add_money(amount: int, to_add=username):
    curr_balance = get_current_balance(to_add)

    cursor.execute(
        "UPDATE users "+
        f"SET balance = {curr_balance + amount} "+
        f"WHERE name = '{to_add}'"
    )


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

def deposit():
    amount = get_int("Deposit amount: $")
    add_money(amount)
    print("Successful deposit.")


def withdraw():
    amount = get_int("Withdrawal amount: $")
    if remove_money(amount):
        print("Successful withdrawal.")
    else:
        print("Unsuccessful withdrawal: Amount exceeds account balance.")
        

def view():
    curr_balance = get_current_balance()
    print(f"Your balance: ${curr_balance}")


def transfer():
    to_transfer = input("To which account would you like to transfer?: ")
    if not get_query(f"SELECT * FROM users WHERE name = '{to_transfer}'"):
        print("User not found in database.")
        return

    amount = get_int("Transfer amount: $")
    success = remove_money(amount)

    if success:
        add_money(amount, to_transfer)
        print(f"${amount} has been successfuly transferred to {to_transfer}.")
    else:
        print("Unsuccessful withdrawal: Amount exceeds account balance. You have not been charged.")


def log_out():
    print("Bye bye!")
    connection.commit()
    print("Data has been saved.")
    quit()


actions = [deposit, withdraw, view, transfer, log_out]

# Input loop
while True:
    action = get_valid_action_number()
    actions[action-1]()