import pygame as pg
from Main import *


pg.init()
HEIGHT = 1000
WIDTH = 1000
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0

class Player():
    def __init__(self, playerX, playerY):
        self.x = playerX
        self.y = playerY
        self.speed = 5
        self.colour = (137, 207, 240)
        self.size = 15
        self.visionRadius = 150
        self.player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    def render(self):
        pg.draw.circle(self.screen, self.colour, self.player_pos, self.size)

    def Keybinds():
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            player_pos.y -= 300 * dt
        if keys[pg.K_s]:
            player_pos.y += 300 * dt
        if keys[pg.K_a]:
            player_pos.x -= 300 * dt
        if keys[pg.K_d]:
            player_pos.x += 300 * dt

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
  screen.fill((211, 211, 211))

  #Player Creation + Movement
  Player.render()
  Player.Keybinds()
  

  fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
  fog_surface.fill((0, 0, 0, 220))
  pg.draw.circle(
      fog_surface, (0, 0, 0, 0), player_pos, vision_radius) 
  screen.blit(fog_surface, (0, 0))


  pg.display.flip()
  dt =clock.tick(60) / 1000

#############
pg.quit()

