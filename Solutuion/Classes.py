class Player():

    #Constructor
    def __init__(self, theName, theCurrentHp, theMaxMana, theCurrentMana theClan, theSpeed):

        self.Name = theName
        self.MaxHp = 300
        self.CurrentHp = 150
        self.MaxMana = 150
        self.CurrentMana = 100
        self.Experience = 0
        self.Level = 0
        self.Clan = theClan
        self.Vision = 10
        self.Speed = 2
    
    #Methods

    def Modify_Hp(self, amount):
        
        self.CurrentHp = max(0, min(self.CurrentHp + amount, self.MaxHp))

        if self.CurrentHp == 0:

            print("You have lost a life!")


    def Modify_Speed(self, amount, Is_Multiplier=False):

        if Is_Multiplier:
            self.Speed *= amount
        else:
            self.Speed += amount

        if self.Speed < 0:
            self.Speed = 0.0


    def Modify_Mana(self, amount):
        
        self.CurrentMana = max(0, min(self.CurrentMana + amount, self.MaxMana))

        if self.Mana == 0:

            print("You have run out of Mana!")

    def Modify_EXP_Lvl(self, amount):

        self.Experience = self.Experience + amount



    #Choose Clan

    #Modify vision















class Inventory():

class Item():

class
