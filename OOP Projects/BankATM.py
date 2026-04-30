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

# Accounts

def addAccountS():
    inputName = input("Enter account: ")
    inputBal = int(input("Enter your current balance: "))
    newAccount = Bank(inputName, inputBal)
    AccountS.append(newAccount)

AccountS = [Bank("Evee", 5012), Bank("Jolteon", 15587), Bank("Flareon", 2341), Bank("Vaporeon", 11009), Bank("Espeon", 25763), Bank("Umbreon", 6420),
Bank("Leafeon", 1250), Bank("Sylveon", 8991), Bank("Glaceon", 19005), Bank("Proffessor Oak", 4113), Bank("Ash Ketchum", 509)]


# Bank("Evee", 5012)
# Bank("Jolteon", 15587)
# Bank("Flareon", 2341)
# Bank("Vaporeon", 11009)
# Bank("Espeon", 25763)
# Bank("Umbreon", 6420)
# Bank("Leafeon", 1250)
# Bank("Sylveon", 8991)
# Bank("Glaceon", 19005)
# Bank("Proffessor Oak", 4113)
# Bank("Ash Ketchum", 509)

#-----------------------------------------------------------

# Main program methods
def getAccountS():
    for i in range (len(AccountS)):
        print(AccountS[i].getAccount())


def addAccountS():
    inputName = input("Enter account: ")
    inputBal = int(input("Enter your current balance: "))
    newAccount = Bank(inputName, inputBal)
    AccountS.append(newAccount)



#-----------------------------------------------------------

#Choice Menu

# print('''
#     ==                                                                  ==
#     ==                           |Menu|                                 ==
#     ==                                                                  ==
#     == Please choose an option below by entering the number accordingly ==
#     ==                                                                  ==
#     ==                                                                  ==
#     ==                                                                  ==
#     ==  1. Create a new account                                         ==
#     ==  2. Deposit                                                      ==
#     ==  3. Withdraw                                                     ==
#     ==  4. Check Current Balance                                        ==
#     ==  5. Exit                                                         ==
#     ==                                                                  ==
#     ==                                                                  ==
#     ''')

def menuChoice():
    choice = input("Enter Number Here: ")

    if choice == 1:
    addAccountS()
    elif choice ==2:
    
    elif choice ==3:

    elif choice ==4:

    elif choice ==5: