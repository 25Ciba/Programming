import pygame as pg
import math
import sys

pg.init()
HEIGHT = 1000
WIDTH = 1000
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0

###

#Player Settings
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_speed = 5
vision_radius = 250
player_color = (137, 207, 240)

###

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
  screen.fill((211, 211, 211))

  #Player Creation + Movement
  pg.draw.circle(screen, player_color, player_pos, 15)
  keys = pg.key.get_pressed()
  if keys[pg.K_w]:
      player_pos.y -= 300 * dt
  if keys[pg.K_s]:
      player_pos.y += 300 * dt
  if keys[pg.K_a]:
      player_pos.x -= 300 * dt
  if keys[pg.K_d]:
      player_pos.x += 300 * dt

  fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
  fog_surface.fill((0, 0, 0, 220))
  pg.draw.circle(
      fog_surface, (0, 0, 0, 0), player_pos, vision_radius) 
  screen.blit(fog_surface, (0, 0))

  pg.display.flip()
  dt =clock.tick(60) / 1000

#############
pg.quit()