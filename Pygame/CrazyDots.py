import pygame
import sys
import random
import math

pygame.init()


WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Pairs of Symmetrical Balls with Full Collision")

clock = pygame.time.Clock()


BLACK = (0, 0, 0)
RED = (255, 60, 60)
BLUE = (60, 160, 255)
PURPLE = (180, 60, 200)
YELLOW = (255, 220, 60)
ORANGE = (255, 140, 0)
GREEN = (60, 200, 60)


DOT_RADIUS = 8
SPEED = 5   
PAIR_SPEED = 4  
CHANGE_INTERVAL = 3000  


trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


red_pos = [random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS), random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)]
blue_pos = [WIDTH - red_pos[0], HEIGHT - red_pos[1]]
red_vel = [random.choice([-SPEED, SPEED]), random.choice([-SPEED, SPEED])]
blue_vel = [-red_vel[0], -red_vel[1]]


purple_pos = [random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS), random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)]
yellow_pos = [WIDTH - purple_pos[0], HEIGHT - purple_pos[1]]
angle = random.uniform(0, 2*math.pi)
purple_vel = [PAIR_SPEED * math.cos(angle), PAIR_SPEED * math.sin(angle)]
yellow_vel = [-purple_vel[0], -purple_vel[1]]


orange_pos = [random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS), random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)]
green_pos = [WIDTH - orange_pos[0], HEIGHT - orange_pos[1]]
angle2 = random.uniform(0, 2*math.pi)
orange_vel = [PAIR_SPEED * math.cos(angle2), PAIR_SPEED * math.sin(angle2)]
green_vel = [-orange_vel[0], -orange_vel[1]]

last_change = pygame.time.get_ticks()


dots = [
    {"pos": red_pos, "vel": red_vel, "color": RED},
    {"pos": blue_pos, "vel": blue_vel, "color": BLUE},
    {"pos": purple_pos, "vel": purple_vel, "color": PURPLE},
    {"pos": yellow_pos, "vel": yellow_vel, "color": YELLOW},
    {"pos": orange_pos, "vel": orange_vel, "color": ORANGE},
    {"pos": green_pos, "vel": green_vel, "color": GREEN},
]

def handle_collision(pos1, vel1, pos2, vel2, radius):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dist = math.hypot(dx, dy)
    if dist < 2 * radius and dist != 0:
        nx = dx / dist
        ny = dy / dist
        dvx = vel1[0] - vel2[0]
        dvy = vel1[1] - vel2[1]
        vn = dvx * nx + dvy * ny
        if vn < 0:
            vel1[0] -= vn * nx
            vel1[1] -= vn * ny
            vel2[0] += vn * nx
            vel2[1] += vn * ny

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = pygame.time.get_ticks()
    
    if now - last_change >= CHANGE_INTERVAL:
        angle = random.uniform(0, 2*math.pi)
        purple_vel[:] = [PAIR_SPEED * math.cos(angle), PAIR_SPEED * math.sin(angle)]
        yellow_vel[:] = [-purple_vel[0], -purple_vel[1]]

        angle2 = random.uniform(0, 2*math.pi)
        orange_vel[:] = [PAIR_SPEED * math.cos(angle2), PAIR_SPEED * math.sin(angle2)]
        green_vel[:] = [-orange_vel[0], -orange_vel[1]]

        last_change = now

    
    for dot in dots:
        dot["pos"][0] += dot["vel"][0]
        dot["pos"][1] += dot["vel"][1]
        if dot["pos"][0] <= DOT_RADIUS or dot["pos"][0] >= WIDTH - DOT_RADIUS:
            dot["vel"][0] *= -1
        if dot["pos"][1] <= DOT_RADIUS or dot["pos"][1] >= HEIGHT - DOT_RADIUS:
            dot["vel"][1] *= -1

    
    for i in range(len(dots)):
        for j in range(i+1, len(dots)):
            handle_collision(dots[i]["pos"], dots[i]["vel"], dots[j]["pos"], dots[j]["vel"], DOT_RADIUS)

    
    trail_surface.fill((0, 0, 0, 5), special_flags=pygame.BLEND_RGBA_SUB)

    
    for dot in dots:
        pygame.draw.circle(trail_surface, dot["color"], (int(dot["pos"][0]), int(dot["pos"][1])), DOT_RADIUS)

    
    screen.fill(BLACK)
    screen.blit(trail_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)