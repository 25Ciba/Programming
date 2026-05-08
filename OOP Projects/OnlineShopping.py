class Customer():

    # Constructor
    def __init__(self, ID, bal):
        self.ID = ID
        self.Bal = bal

    # Getters

    def getID(self):
        print(f"Your ID is {self.ID}.")
    
    def getBal(self):
        print(f"Bal : {self.Bal} .")

    #Setters

    def pay(self, mula):
        if mula > self.Bal:
            print("Unable to process transaction.")
        else:
            self.Bal -= mula 
            print(f"£{mula} paid. New balance: £{self.Bal}")

#-----

class Products():

    # Constructor
    def __init__(self, items, itemPrice):
        self.item = items
        self.itp = itemPrice

    # Getters
    def getPrice(self):
        print(f"{self.item} is £{self.itp}.")


#-----

#Items

ItemS = [
        Products("Hat", 10), 
        Products("Mat", 14), 
        Products("Rug", 16), 
        Products("Watch", 115), 
        Products("Spoon", 6), 
        Products("Fork", 9),
        Products("Knife", 21), 
        Products("ICBM", 162000000), 
        Products("Hydrogeen Bomb", 25000000), 
        Products("TSAR Bomb", 120000000), 
        Products("Posiedon's Wrath :p", 67)
        ]

#-----

class Purchases(Customer, Products):

    #Constructor
    def __init__(self, ID, Bal, items, itemPrice,)





#-----

# Main Subroutines 

def printAllItemS():
    for i in range (len(ItemS)):
        print(ItemS[i].getPrice())





#-----
#Main
#-----