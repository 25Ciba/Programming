import math
import random





class Player():

    #Constructor
    def __init__(self, theName, theCurrentHp, theMaxMana, theCurrentMana, theClan, theSpeed):

        self.Name = theName
        self.MaxHp = 300
        self.CurrentHp = 150
        self.MaxMana = 150
        self.CurrentMana = 100
        self.Experience = 0
        self.Level = 0
        self.Clan = theClan
        self.CurrentVision = 5
        self.Vision = 5
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

        if self.Experience == 10:
            self.Level = self.Level + 1


    def Modify_Vision(self, objects, max_distance=5, max_bonus=7):
        
        if not objects:
            self.CurrentVision = self.Vision
            return

        min_distance = float('inf')

        for obj in objects:

            distance = math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2)
            if distance < min_distance:
                min_distance = distance

        if min_distance <= max_distance:
            proximity_factor = 1 - (min_distance / max_distance)
            bonus = proximity_factor * max_bonus
            self.CurrentVision = self.Vision + bonus
        else:
            self.CurrentVision = self.Vision



    #Choose Clan

 





class Inventory():

class Item():

class
