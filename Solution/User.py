#collection
#map
#store
#interact
#use skill
#inventory
#equip item
#story cutscene
import pygame as pg

HEIGHT = 1000
WIDTH = 1000
screen = pg.display.set_mode((WIDTH, HEIGHT))

class Player:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 300
        self.colour = (137, 207, 240)
        self.size = 15
        self.visionRadius = 150

    def render(self):
        pg.draw.circle(screen, self.colour, (self.x, self.y), self.size)

    def keybinds(self, dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.y -= self.speed * dt
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.y += self.speed * dt
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.x += self.speed * dt

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    def pvisionRadius(self):
        return self.visionRadius
