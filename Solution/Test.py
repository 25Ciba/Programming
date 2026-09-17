#collection
#map
#store
#interact
#use skill
#inventory
#equip item
#story cutscene
import pygame as pg
import Main


class Player():
    def __init__(self, playerX, playerY):
        self.x = playerX
        self.y = playerY
        self.speed = 5
        self.colour = (137, 207, 240)
        self.size = 15
        self.visionRadius = 150

    def render(self):
        pg.draw.circle(self.screen, self.colour, (Main.screen.get_width() / 2, Main.screen.get_height() / 2), self.size)

class Proximity():

    def __init__()
import math
def proximity(playerpos.x, playerpos.y, complimentposX, complimentposY, radius):
    disable(Interact.keybind())
    playerprox = math.sqrt(((playeros.x - complimentposx)**2) + ((playerpos.y - complimentposy)**2))
    if playerprox =< 80:
        enable(Interact.keybind())
        return True
    else:
        return False

def collection(playerpos.x, playerpos.y, itemX, itemY):
    if proximity(playerpos.x, playerpos.y, itemX, itemY) == True:
        for items.onfloor.visible 





