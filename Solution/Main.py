import pygame as pg
from Classes import (Player, EnemyManager, Camera, DungeonMap, MAP_WIDTH, MAP_HEIGHT)

# Initialise Pygame
pg.init()
WIDTH = 1200
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Melody of the Mist")
clock = pg.time.Clock()
running = True
font = pg.font.Font(None, 28)
small_font = pg.font.Font(None, 22)

# Create objects
dungeon_map = DungeonMap()
player = Player(screen)
enemy_manager = EnemyManager(screen, player, dungeon_map)
camera = Camera(screen, MAP_WIDTH, MAP_HEIGHT)
message = "WASD / arrows: move | left click: attack | right click: block | space: dash | E: door"
message_timer = 6.0

# Main game loop
while running:
    dt = min(clock.tick(60) / 1000, 0.05)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_e:
                message = dungeon_map.interact(player.x, player.y)
                message_timer = 2.0
            elif event.key == pg.K_SPACE:
                if player.begin_dash():
                    message = "Dash!"
                    message_timer = 0.6
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attack_enemies(enemy_manager.enemies)
            elif event.button == 3:
                if player.begin_block():
                    message = "Block!"
                    message_timer = 0.6

    # Update objects
    player.update(dt)
    player.keybinds(dt, dungeon_map)
    enemy_manager.update(dt)
    camera.update(player)
    if player.current_lives <= 0:
        running = False
    if message_timer > 0:
        message_timer -= dt

    # Screen rendering
    screen.fill((10, 13, 21))
    dungeon_map.render(screen, camera)

    # Object rendering
    enemy_manager.render(camera)
    player.render(camera)

    # Fog of war
    fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    fog_surface.fill((0, 0, 0, 205))
    player_screen_pos = camera.apply(player.x, player.y)
    pg.draw.circle(fog_surface, (0, 0, 0, 0), player_screen_pos, player.pvisionRadius())
    screen.blit(fog_surface, (0, 0))

    # Health and ability display
    pg.draw.rect(screen, (20, 24, 34), (14, 14, 285, 147), border_radius=6)
    pg.draw.rect(screen, (74, 80, 91), (24, 25, 230, 18), border_radius=4)
    hp_percentage = player.current_hp / player.max_hp
    pg.draw.rect(screen, (190, 62, 78), (24, 25, 230 * hp_percentage, 18), border_radius=4)
    hp_text = font.render(f"HP: {player.current_hp} / {player.max_hp}", True, (238, 242, 247))
    screen.blit(hp_text, (24, 49))
    defence_text = small_font.render(f"Defence: {player.defence}", True, (214, 224, 236))
    screen.blit(defence_text, (24, 76))
    lives_text = small_font.render(f"Lives: {player.current_lives} / {player.max_lives}", True, (214, 224, 236))
    screen.blit(lives_text, (24, 99))
    block_cooldown = (
        "ready" if player.block_cooldown <= 0
        else f"{player.block_cooldown:.1f}s"
    )
    dash_cooldown = (
        "ready" if player.dash_cooldown <= 0
        else f"{player.dash_cooldown:.1f}s"
    )
    screen.blit(
        small_font.render(f"Block: {block_cooldown}", True, (210, 225, 242)),
        (24, 121)
    )
    screen.blit(
        small_font.render(f"Dash: {dash_cooldown}", True, (210, 225, 242)),
        (145, 121)
    )
    if message_timer > 0:
        message_text = small_font.render(message, True, (235, 242, 250))
        message_box = message_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)).inflate(24, 14)
        pg.draw.rect(screen, (20, 24, 34), message_box, border_radius=6)
        screen.blit(message_text, message_text.get_rect(center=message_box.center))

    # Update display
    pg.display.flip()

# Quit Pygame

pg.quit()