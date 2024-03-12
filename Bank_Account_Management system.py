import pandas as pd
from datetime import datetime, timedelta

# File paths for storing data
ACCOUNTS_FILE = 'accounts.csv'
TRANSACTIONS_FILE = 'transactions.csv'

# Initialize DataFrames to store account information and transactions
try:
    accounts_df = pd.read_csv(ACCOUNTS_FILE)
except FileNotFoundError:
    accounts_df = pd.DataFrame(columns=['Account Number', 'Balance'])

try:
    transactions_df = pd.read_csv(TRANSACTIONS_FILE)
except FileNotFoundError:
    transactions_df = pd.DataFrame(columns=['Account Number', 'Amount', 'Transaction Type', 'Transaction Time'])


class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.created_time = datetime.now()

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._record_transaction(amount, "deposit")
            print(f"Deposited Rs{amount}. New balance: Rs{self.balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
            if 0 < amount <= self.balance:
                self.balance -= amount
                self._record_transaction(amount, "withdraw")
                print(f"Withdrawn ${amount}. New balance: ${self.balance}")
            else:
                print("Insufficient funds.")

    def get_balance(self):
        return self.balance

    def _record_transaction(self, amount, transaction_type):
        transactions_df.loc[len(transactions_df)] = [self.account_number, amount, transaction_type, datetime.now()]


def create_account():
    account_number = input("Enter account number: ")
    initial_balance = float(input("Enter initial balance: "))
    accounts_df.loc[len(accounts_df)] = [account_number, initial_balance]
    return BankAccount(account_number, initial_balance)


def check_balance(account_number):
    balance = accounts_df.loc[accounts_df['Account Number'] == account_number, 'Balance'].values
    if len(balance) > 0:
        return balance[0]
    else:
        return None


def show_statement(account_number):
    statement = transactions_df[transactions_df['Account Number'] == account_number]
    if not statement.empty:
        print("Transaction History:")
        print(statement)
    else:
        print("No transactions found.")


def save_data_to_disk():
    accounts_df.to_csv(ACCOUNTS_FILE, index=False)
    transactions_df.to_csv(TRANSACTIONS_FILE, index=False)


def main():
    while True:
        print("\nChoose an option:")
        print("1. Create Bank Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. View Statement")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            account = create_account()
            print("Account created successfully.")
        elif choice == '2':
            account_number = input("Enter account number: ")
            amount = float(input("Enter deposit amount: "))
            if account_number not in accounts_df['Account Number'].tolist():
                print('Account Does not exist')
                continue
            account = BankAccount(account_number, check_balance(account_number))
            account.deposit(amount)
        elif choice == '3':
            account_number = input("Enter account number: ")
            amount = float(input("Enter withdrawal amount: "))
            account = BankAccount(account_number, check_balance(account_number))
            account.withdraw(amount)
        elif choice == '4':
            account_number = input("Enter account number: ")
            balance = check_balance(account_number)
            if balance is not None:
                print(f"Current balance for account {account_number}: ${balance}")
            else:
                print("Account not found.")
        elif choice == '5':
            account_number = input("Enter account number: ")
            show_statement(account_number)
        elif choice == '6':
            print("Exiting program.")
            save_data_to_disk() 
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
