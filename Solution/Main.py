import pygame as pg
import MainFunctions
import Player

Initial()

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
  screen.fill((211, 211, 211))

  #Player Creation + Movement
  Player.render()
  Player.keybinds()
  
  fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
  fog_surface.fill((0, 0, 0, 220))
  pg.draw.circle(
      fog_surface, (0, 0, 0, 0), Player.pvector2(), Player.pvisionRadius()) 
  screen.blit(fog_surface, (0, 0))


  pg.display.flip()
  dt =clock.tick(60) / 1000

#############
pg.quit()

