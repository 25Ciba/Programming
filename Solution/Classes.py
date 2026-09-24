# class Proximity():

#     def __init__()
# import math
# def proximity(playerpos.x, playerpos.y, complimentposX, complimentposY, radius):
#     disable(Interact.keybind())
#     playerprox = math.sqrt(((playeros.x - complimentposx)**2) + ((playerpos.y - complimentposy)**2))
#     if playerprox =< 80:
#         enable(Interact.keybind())
#         return True
#     else:
#         return False

# def collection(playerpos.x, playerpos.y, itemX, itemY):
#     if proximity(playerpos.x, playerpos.y, itemX, itemY) == True:
#         for items.onfloor.visible 







class Lives():

    #Constructor
    def __init__(self):        

        self.maxlives = 7
        self.currentlives = 7

###

class Attack():

    #Constructor
    def __init__(self):

        self.minatk = 1
        self.currentatk = 10

###

class Defence(Attack):

    #Constructor
    def __init__(self):
        super().__init__()

        self.maxdef = 1000
        self.currentdef = 100

    def ReduceDmg(self):

        

###

class HealthBar(Lives, Defence):

    #Constructor
    def __init__(self):
        super().__init__()

        self.maxhp = 100
        self.currenthp = 100
        
    #Methods

    def Modify_Hp(self, amount):

        self.currenthp = max(0, min(self.currenthp + amount, self.maxhp))
        if self.currenthp == 0:
            self.currentlives = self.currentlives - 1
    
###

        





