import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cursor-Controlled Dot + Single Purple Dot")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (180, 60, 200)

DOT_RADIUS = 10
PURPLE_RADIUS = DOT_RADIUS + 4  


purple_dot = [
    WIDTH // 2 + random.randint(-200, 200),
    HEIGHT // 2 + random.randint(-200, 200)
]

def teleport_dot(dot):
    """Teleport a dot to a new random location near center."""
    dot[0] = WIDTH // 2 + random.randint(-200, 200)
    dot[1] = HEIGHT // 2 + random.randint(-200, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            dx = mouse_pos[0] - purple_dot[0]
            dy = mouse_pos[1] - purple_dot[1]
            if dx*2 + dy*2 <= PURPLE_RADIUS*2:
                teleport_dot(purple_dot)
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_x, pygame.K_z]:
                mouse_pos = pygame.mouse.get_pos()
                dx = mouse_pos[0] - purple_dot[0]
                dy = mouse_pos[1] - purple_dot[1]
                if dx*2 + dy*2 <= PURPLE_RADIUS*2:
                    teleport_dot(purple_dot)

    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    
    screen.fill(BLACK)
    
    pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), DOT_RADIUS)
    
    pygame.draw.circle(screen, PURPLE, (int(purple_dot[0]), int(purple_dot[1])), PURPLE_RADIUS)

    pygame.display.flip()
    clock.tick(60)