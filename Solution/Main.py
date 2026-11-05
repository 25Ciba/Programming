import pygame as pg

from Classes import (
    Player,
    EnemyManager,
    Camera,
    DungeonMap,
    MAP_WIDTH,
    MAP_HEIGHT
)


pg.init()

WIDTH = 1200
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Melody of the Mist")
clock = pg.time.Clock()
running = True

# Create the tiled map and game objects.
dungeon_map = DungeonMap()
player = Player(screen)
enemy_manager = EnemyManager(screen, player, dungeon_map)
camera = Camera(screen, MAP_WIDTH, MAP_HEIGHT)


while running:
    dt = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_e:
            print(dungeon_map.interact(player.x, player.y))

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attack_enemies(enemy_manager.enemies)

    # Update objects.
    player.update(dt)
    player.keybinds(dt, dungeon_map)
    enemy_manager.update(dt)
    camera.update(player)

    if player.current_lives <= 0:
        running = False

    # Draw the dungeon map instead of the old background.
    screen.fill((15, 17, 23))
    dungeon_map.render(screen, camera)

    # Draw the player and enemies over the map.
    player.render(camera)
    enemy_manager.render(camera)

    # Fog of war.
    fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    fog_surface.fill((0, 0, 0, 220))

    player_screen_pos = camera.apply(player.x, player.y)
    pg.draw.circle(
        fog_surface,
        (0, 0, 0, 0),
        player_screen_pos,
        player.pvisionRadius()
    )
    screen.blit(fog_surface, (0, 0))

    # Health bar.
    hp_bar_width = 200
    hp_bar_height = 20
    hp_percentage = player.current_hp / player.max_hp

    pg.draw.rect(
        screen,
        (80, 80, 80),
        (20, 20, hp_bar_width, hp_bar_height)
    )
    pg.draw.rect(
        screen,
        (255, 71, 76),
        (20, 20, hp_bar_width * hp_percentage, hp_bar_height)
    )

    font = pg.font.Font(None, 28)

    hp_text = font.render(
        f"HP: {player.current_hp} / {player.max_hp}",
        True,
        (255, 255, 255)
    )
    screen.blit(hp_text, (20, 45))

    defence_text = font.render(
        f"Defence: {player.defence}",
        True,
        (255, 255, 255)
    )
    screen.blit(defence_text, (20, 70))

    lives_text = font.render(
        f"Lives: {player.current_lives} / {player.max_lives}",
        True,
        (255, 255, 255)
    )
    screen.blit(lives_text, (20, 95))

    pg.display.flip()

pg.quit()