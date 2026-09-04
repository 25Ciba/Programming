import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player settings
player_pos = [400, 300]
player_speed = 5
vision_radius = 100

# Create fog overlay layer
fog_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

running = True
while running:
  screen.fill((30, 150, 30))  # Draw background terrain (green)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Handle movement
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    player_pos[0] -= player_speed
  if keys[pygame.K_RIGHT]:
    player_pos[0] += player_speed
  if keys[pygame.K_UP]:
    player_pos[1] -= player_speed
  if keys[pygame.K_DOWN]:
    player_pos[1] += player_speed

  # Reset fog and punch vision hole
  fog_surface.fill((0, 0, 0, 220))  # Dark fog overlay
  pygame.draw.circle(
      fog_surface, (0, 0, 0, 0), player_pos, vision_radius
  )  # Clear circle

  # Draw fog over the screen
  screen.blit(fog_surface, (0, 0))

  # Draw player
  pygame.draw.circle(screen, (255, 0, 0), player_pos, 15)

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
