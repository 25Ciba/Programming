import pygame
import math

pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOG_COLOR = (0, 0, 0)

# Initialize the screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Fog of war effect layer
fog_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fog_layer.fill(FOG_COLOR)
fog_layer.set_alpha(180)  # Semi-transparent

# Game loop flag and player position
running = True
player_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Player settings
player_radius = 25
player_color = (255, 255, 255)
player_vision_radius = 150

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position based on key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos = (player_pos[0] - 5, player_pos[1])
    if keys[pygame.K_RIGHT]:
        player_pos = (player_pos[0] + 5, player_pos[1])
    if keys[pygame.K_UP]:
        player_pos = (player_pos[0], player_pos[1] - 5)
    if keys[pygame.K_DOWN]:
        player_pos = (player_pos[0], player_pos[1] + 5)

    # Clear the screen and apply the fog
    screen.fill((0, 0, 0))
    screen.blit(fog_layer, (0, 0))
    
    # Vision circle that reveals the map
    vision_circle = pygame.Surface((player_vision_radius * 2, player_vision_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(vision_circle, (0, 0, 0, 0), (player_vision_radius, player_vision_radius), player_vision_radius)

    # Blit the vision circle onto the fog layer
    fog_layer.blit(vision_circle, (player_pos[0] - player_vision_radius, player_pos[1] - player_vision_radius), special_flags=pygame.BLEND_RGBA_MIN)

    # Redraw the player
    pygame.draw.circle(screen, player_color, player_pos, player_radius)
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()