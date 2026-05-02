#-----------------------------------------------------------
class Bank():

    bankTotal = 100000  

    # Constructor
    def __init__(self, AccountName, Bal):

        # Attributes
        self.account = AccountName
        self.balance = Bal

#-----------------------------------------------------------

    # Getters

    def getBal(self):
        print(f"Account holder: {self.account}")
        print(f"Current balance: ${self.balance}")

    def getAccount(self):
        return self.account


#-----------------------------------------------------------

    # Setters

    def withdraw(self, mula):

        if mula > self.balance:
            print("You do not posses enuf mula brody. Come back with more bags.")
        else:
            self.balance -= mula
            Bank.bankTotal -= mula  
            print(f"Withdrew £{mula}. New balance: £{self.balance}")
            print(f"- Bank loses: £{mula}")
            print(f"- Current Bank balance £{Bank.bankTotal}")  

    def deposit(self, mula):

        self.balance += mula
        Bank.bankTotal += mula 
        print(f"Deposited £{mula}. New balance: £{self.balance}")
        print(f"- Bank gains: £{mula}")
        print(f"- Current Bank balance £{Bank.bankTotal}") 

#-----------------------------------------------------------

#Importing things

import itertools
import threading
import time
import sys

#-----------------------------------------------------------

# Accounts

AccountS = [
            Bank("Evee", 5012), 
            Bank("Jolteon", 15587), 
            Bank("Flareon", 2341), 
            Bank("Vaporeon", 11009), 
            Bank("Espeon", 25763), 
            Bank("Umbreon", 6420),
            Bank("Leafeon", 1250), 
            Bank("Sylveon", 8991), 
            Bank("Glaceon", 19005), 
            Bank("Proffessor Oak", 4113), 
            Bank("Ash Ketchum", 509)
            ]

#-----------------------------------------------------------

# Main program methods

def printAllAccountS():
    for i in range (len(AccountS)):
        print(AccountS[i].getAccount())


def get_input(prompt):
    return input(prompt).strip().lower()

def findAccount(name):  
    for account in AccountS:
        if name == account.getAccount().lower():
            return account
    return None


def animate():
    done = False
    def loading():
        nonlocal done
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
    t = threading.Thread(target=loading)
    t.start()
    time.sleep(2)
    done = True
    t.join()


def addAccountS():
    inputName = input("Enter account: ").strip()  
    inputBal = int(input("Enter your current balance: "))
    newAccount = Bank(inputName, inputBal)
    AccountS.append(newAccount)
    print("Registration successful!")


def CheckIn():
    print("Welcome to the most prestigeous bank in the world.")
    accountName = get_input("Enter account: ")
    found = False
    for account in AccountS:
        if accountName == account.getAccount().lower():
            animate()
            print(f"Welcome back {account.getAccount()}!")
            found = True
            break
    if not found:
        print("You dont seem to be registered as an account holder.")
        joinBank = get_input("Would you like to create a new account? (Y/N): ")

        if joinBank == 'y':
            addAccountS()
        else:
            print("Thank you for using our services. Goodbye.")
            return  

def CheckBal():
    accName = get_input("Enter account holder name/ID: ")
    account = findAccount(accName) 
    if account:
        animate()
        account.getBal()
    else:
        print("You are not registered with this bank")

def depositMoney():
    name = get_input("Enter account name: ")
    account = findAccount(name)
    if account:
        try:
            amount = int(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Enter a valid amount.")
                return
            account.deposit(amount)
            animate()
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Account not found")

def withdrawMoney():
    name = get_input("Enter account name: ")
    account = findAccount(name)
    if account:
        try:
            amount = int(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Enter a valid amount.")
                return
            account.withdraw(amount)
            animate()
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Account not found")

def menuChoice():
    CheckIn()

    while True:
        print("""
1. Create a new account
2. Deposit
3. Withdraw
4. Check Current Balance
5. Exit
""")

        choice = get_input("Enter Number Here: ")

        if choice == '1':
            addAccountS()
        elif choice == '2':
            depositMoney()
        elif choice == '3':
            withdrawMoney()
        elif choice == '4':
            CheckBal()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

#-----------------------------------------------------------
                    ##############
                    #MAIN PROGRAM#
                    #############
#-----------------------------------------------------------

menuChoice()  