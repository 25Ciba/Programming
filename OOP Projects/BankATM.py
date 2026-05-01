#-----------------------------------------------------------
class Bank():

    # Constructor
    def __init__(self, AccountName, Bal):

        # Attributes

        self.account = AccountName
        self.balance = Bal
        self.bankTotal = 100000

#-----------------------------------------------------------

    # Getters

    # def getBankTotal(self):
    #     return self.bankTotal

    ###

    def getBal(self):
        print(f"Account holder: {self.account}")
        print(f"Current balance: ${self.balance}")

    ###

    def getAccount(self):
        return self.account


#-----------------------------------------------------------

    # Setters

    def withdraw(self, mula):

        if mula > self.balance:
            print("You do not posses enuf mula brody. Come back with more bags.")
        else:
            self.balance -= mula
            print(f"Withdrew £{mula}. New balance: £{self.balance}")
            print(f"- Bank loses: £{mula}")
            print(f"- Current Bank balance £{self.bankTotal - mula}")

    ###

    def deposit(self, mula):

        self.balance += mula
        print(f"Deposited £{mula}. New balance: £{self.balance}")
        print(f"- Bank loses: £{mula}")
        print(f"- Current Bank balance £{self.bankTotal + mula}")

#-----------------------------------------------------------

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

def getAccountS():
    for i in range (len(AccountS)):
        print(AccountS[i].getAccount())

def animate():
    done = False
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(2) #Change how long animation is
    done = True

def addAccountS():
    inputName = input("Enter account: ")
    inputBal = int(input("Enter your current balance: "))
    newAccount = Bank(inputName, inputBal)
    AccountS.append(newAccount)
    print("Registration successful! Thank you for using out services!")

def CheckIn():
    print("Welcome to the most prestigeous bank in the world (not really - im kidding dont sue me Goldman Sachs).")
    print("Before any transactions please input the name of the account holder and current balance.")
    accountName = input("Enter account: ")
    accountBal = int(input("Enter your current balance: "))
    checkAccount = Bank(accountName, accountBal)
    for i in range (len(AccountS)):
        if checkAccount in (AccountS[i]):
            print(f"Welcome back {checkAccount.getAccount}!")
        else:
            print(f"You dont seem to be registered as an account holder within this establishment.")
            joinBank = input("Would you like to create a new account? Please anser with a prompt 'Y' or 'N' respectively: ")
            if joinBank == 'Y':
                addAccountS()
            else:
                print("Thank you for using our services. Have a great day, goodbye.")

def CheckBal():
    accName = input("Enter account holder name/ID: ")
    for i in range (len(AccountS)):
        if accName in (AccountS[i].getAccount()):
            print(accName.getBal())



#-----------------------------------------------------------

#Choice Menu

def menuChoice():
    CheckIn()
    print('''
    ==                                                                  ==
    ==                           |Menu|                                 ==
    ==                                                                  ==
    == Please choose an option below by entering the number accordingly ==
    ==                                                                  ==
    ==                                                                  ==
    ==                                                                  ==
    ==  1. Create a new account                                         ==
    ==  2. Deposit                                                      ==
    ==  3. Withdraw                                                     ==
    ==  4. Check Current Balance                                        ==
    ==  5. Exit                                                         ==
    ==                                                                  ==
    ==                                                                  ==
    ''')

    # choice = input("Enter Number Here: ")

    # if choice == 1:
    #     addAccountS()
    # elif choice ==2:
    
    # elif choice ==3:

    # elif choice ==4:

    # elif choice ==5:

#Figure out how to do num 4 in
#Maybe do this same ything but instead of an arry use a linke list.
#Then traverse linked list to find if person is in bank, use getters to find balance/name ect (element of the 'node')
#There will be a problem when you add to the list though
#lowkey good luck twin. Your gonna need it. (╥﹏╥)✌︎︎