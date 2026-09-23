import pygame as pg
from User import Player

HEIGHT = 1000
WIDTH = 1000
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

player = Player()

while running:
    dt = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((211, 211, 211))

    player.keybinds(dt)
    player.render()

    fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    fog_surface.fill((0, 0, 0, 220))

    pg.draw.circle(
        fog_surface,
        (0, 0, 0, 0),
        player.pvector2(),
        player.pvisionRadius()
    )

    screen.blit(fog_surface, (0, 0))
    pg.display.flip()

pg.quit()
