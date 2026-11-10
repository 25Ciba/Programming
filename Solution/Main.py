import pygame as pg
from Classes import Player, EnemyManager, Camera, Map, MAP_WIDTH, MAP_HEIGHT

# Start Pygame
pg.init()
WIDTH = 1200
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Melody of the Mist")
clock = pg.time.Clock()
running = True
show_map = False
font = pg.font.Font(None, 28)
small_font = pg.font.Font(None, 22)

# Create the game objects
game_map = Map()
player = Player(screen)
enemy_manager = EnemyManager(screen, player, game_map)
camera = Camera(screen, MAP_WIDTH, MAP_HEIGHT)
message = "WASD / arrow keys: move | left click: attack | right click: block | space: dash | M: map"
message_timer = 6.0

# Make the mist once. The clear part follows the player.
vision = player.pvisionRadius()
fog_radius = vision + 150
mist = pg.Surface((fog_radius * 2, fog_radius * 2), pg.SRCALPHA)
mist.fill((11, 14, 24, 240))
for radius in range(fog_radius, vision - 1, -1):
    fade = (radius - vision) / (fog_radius - vision)
    pg.draw.circle(mist, (11, 14, 24, int(240 * fade)), (fog_radius, fog_radius), radius)
fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

# Main game loop
while running:
    dt = min(clock.tick(60) / 1000, 0.05)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_m:
                show_map = not show_map
            elif event.key == pg.K_SPACE and not show_map:
                if player.begin_dash():
                    message = "Dash!"
                    message_timer = 0.6
        elif event.type == pg.MOUSEBUTTONDOWN and not show_map:
            if event.button == 1:
                player.attack_enemies(enemy_manager.enemies)
            elif event.button == 3:
                if player.begin_block():
                    message = "Block!"
                    message_timer = 0.6

    # Update the game objects
    if not show_map:
        player.update(dt)
        player.keybinds(dt, game_map)
        enemy_manager.update(dt)
        camera.update(player)

    if player.current_lives <= 0:
        running = False
    if message_timer > 0:
        message_timer -= dt

    # Draw the map and game objects
    screen.fill((10, 13, 21))
    game_map.render(screen, camera)
    enemy_manager.render(camera)
    player.render(camera)

    # Draw fog of war
    fog_surface.fill((11, 14, 24, 240))
    player_screen_pos = camera.apply(player.x, player.y)
    mist_rect = mist.get_rect(center=player_screen_pos)
    fog_surface.blit(mist, mist_rect, special_flags=pg.BLEND_RGBA_MIN)
    screen.blit(fog_surface, (0, 0))

    # Draw health and ability information
    pg.draw.rect(screen, (20, 24, 34), (14, 14, 285, 147))
    pg.draw.rect(screen, (74, 80, 91), (24, 25, 230, 18))
    hp_percentage = player.current_hp / player.max_hp
    pg.draw.rect(screen, (190, 62, 78), (24, 25, 230 * hp_percentage, 18))

    hp_text = font.render(f"HP: {player.current_hp} / {player.max_hp}", True, (238, 242, 247))
    screen.blit(hp_text, (24, 49))
    defence_text = small_font.render(f"Defence: {player.defence}", True, (214, 224, 236))
    screen.blit(defence_text, (24, 76))
    lives_text = small_font.render(f"Lives: {player.current_lives} / {player.max_lives}", True, (214, 224, 236))
    screen.blit(lives_text, (24, 99))

    if player.block_cooldown <= 0:
        block_cooldown = "ready"
    else:
        block_cooldown = f"{player.block_cooldown:.1f}s"
    if player.dash_cooldown <= 0:
        dash_cooldown = "ready"
    else:
        dash_cooldown = f"{player.dash_cooldown:.1f}s"

    screen.blit(small_font.render(f"Block: {block_cooldown}", True, (210, 225, 242)), (24, 121))
    screen.blit(small_font.render(f"Dash: {dash_cooldown}", True, (210, 225, 242)), (145, 121))

    if message_timer > 0:
        message_text = small_font.render(message, True, (235, 242, 250))
        message_box = message_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)).inflate(24, 14)
        pg.draw.rect(screen, (20, 24, 34), message_box)
        screen.blit(message_text, message_text.get_rect(center=message_box.center))

    location = small_font.render(game_map.location_name(player.x, player.y), True, (238, 242, 247))
    location_box = location.get_rect(topright=(WIDTH - 24, 24))
    pg.draw.rect(screen, (20, 24, 34), location_box.inflate(20, 12))
    screen.blit(location, location_box)

    if show_map:
        game_map.render_overview(screen, player, small_font)

    # Show the finished frame
    pg.display.flip()

pg.quit()
