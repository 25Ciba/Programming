import os
import syss
import pygame as pg
from random import randint
from Classes import Player, EnemyManager, Background

###

pg.init()
HEIGHT = 800
WIDTH = 1200
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

#Create objects
player = Player(screen)
enemy_manager = EnemyManager(screen, player)
BackGround = Background("Images/Clouds 4.png", [0,0])

###

while running:

    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attack_enemies(enemy_manager.enemies)

    # keep Updating objects
    player.update(dt)
    player.keybinds(dt)
    enemy_manager.update(dt)
    if player.current_lives <= 0:
        running = False

    # Screen Rendering
    screen.fill((211, 211, 211))

    #Background
    screen.blit(BackGround.image, BackGround.rect)

    #Object Rendering
    player.render()
    enemy_manager.render()

    #Fog of War
    fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    fog_surface.fill((0, 0, 0, 220))
    pg.draw.circle(fog_surface, (0, 0, 0, 0), player.pvector2(), player.pvisionRadius())
    screen.blit(fog_surface, (0, 0))

    #Hp Bar and display
    hp_bar_width = 200
    hp_bar_height = 20
    hp_percentage = (player.current_hp / player.max_hp)
    pg.draw.rect(screen, (80, 80, 80), (20, 20, hp_bar_width, hp_bar_height))
    pg.draw.rect(screen, (255, 71, 76), (20, 20, hp_bar_width * hp_percentage, hp_bar_height))
    font = pg.font.Font(None, 28)
    hp_text = font.render(f"HP: {player.current_hp} / {player.max_hp}", True, (255, 255, 255))
    screen.blit(hp_text,(20, 45))

    #Defence display
    defence_text = font.render(f"Defence: {player.defence}", True, (255, 255, 255))
    screen.blit(defence_text,(20, 70))

    #Lives display
    lives_text = font.render(f"Lives: {player.current_lives} / {player.max_lives}", True, (255, 255, 255))
    screen.blit(lives_text,(20, 95))

    #Pg display update
    pg.display.flip()

#Get outa program
pg.quit()