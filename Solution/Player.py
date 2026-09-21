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
        self.x = Main.WIDTH/2
        self.y = Main.HEIGHT/2
        self.speed = 5
        self.colour = (137, 207, 240)
        self.size = 15
        self.visionRadius = 150

    def render(self):
        pg.draw.circle(Main.screen, self.colour, (Main.screen.get_width() / 2, Main.screen.get_height() / 2), self.size)

    def keybinds(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.y -= 300 * dt
        if keys[pg.K_s]:
            self.y += 300 * dt
        if keys[pg.K_a]:
            self.x -= 300 * dt
        if keys[pg.K_d]:
            self.x += 300 * dt

    def pvector2(self):
        Vector2 = pg.Vector2(Main.screen.get_width() / 2, Main.screen.get_height() / 2)
        return Vector2
    
    def pvisionRadius(self):
        return self.visionRadius







