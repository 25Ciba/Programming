import pygame
import math
import sys


pygame.init()


WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots")

clock = pygame.time.Clock()


BLACK = (0, 0, 0)
RED = (255, 60, 60)
BLUE = (60, 160, 255)


a = 500  
b = 300  
speed = 0.05  
t = 0


trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

def draw_glow(surface, x, y, color, radius):
    
    for i in range(10, 0, -1):
        glow_radius = radius + i * 2
        alpha = max(5, 50 - i * 5)
        glow_surf = pygame.Surface((glow_radius * (1/5), glow_radius * (1/5)), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf, (*color, alpha),
            (glow_radius, glow_radius),
            glow_radius
        )
        surface.blit(glow_surf, (x - glow_radius, y - glow_radius), special_flags=pygame.BLEND_PREMULTIPLIED)

    pygame.draw.circle(surface, color, (int(x), int(y)), radius)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    t += speed

    
    x = (a * math.cos(t)) / (1 + math.sin(t)**2)
    y = (b * math.sin(t) * math.cos(t)) / (1 + math.sin(t)**2)

    cx, cy = WIDTH // 2, HEIGHT // 2
    red_pos = (cx + x, cy + y)
    blue_pos = (cx - x, cy - y)

    
    trail_surface.fill((0, 0, 0, 7), special_flags=pygame.BLEND_RGBA_SUB)

    
    draw_glow(trail_surface, *red_pos, RED, 8)
    draw_glow(trail_surface, *blue_pos, BLUE, 8)

    
    screen.fill(BLACK)
    screen.blit(trail_surface, (0, 0))
    pygame.display.flip()

    clock.tick(60)