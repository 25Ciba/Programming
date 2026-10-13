import pygame as pg
import random
import math
import os

HEIGHT = 1000
WIDTH = 1000

#============================================================

#Player

class Player(pg.sprite.Sprite):

    def __init__(self, screen):

        self.screen = screen
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 300
        self.colour = (137, 207, 240)
        self.size = 15
        self.visionRadius = 150
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.defence = 50
        self.attack = 20
        self.attack_range = 100
        self.attack_cooldown = 0
        self.attack_delay = 0.3
        self.max_lives = 7
        self.current_lives = self.max_lives


# Use this to add sprite for main character. Got this from Cameras in pygame git repo that you have saved.
# Here is the repo: https://github.com/clear-code-projects/Pygame-Cameras.git

# class Player(pygame.sprite.Sprite):
# 	def __init__(self,pos,group):
# 		super().__init__(group)
# 		self.image = pygame.image.load('graphics/player.png').convert_alpha()
# 		self.rect = self.image.get_rect(center = pos)
# 		self.direction = pygame.math.Vector2()
# 		self.speed = 5

    ###

    def keybinds(self, dt):

        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.y -= self.speed * dt
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.y += self.speed * dt
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.x += self.speed * dt

    #

    def render(self):
        pg.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

    #

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    #

    def pvisionRadius(self):
        return self.visionRadius

    #
    
    def take_damage(self, incoming_damage):
        damage_multiplier = self.max_hp / (self.max_hp + self.defence)
        actual_damage = round(incoming_damage * damage_multiplier)
        actual_damage = max(1, actual_damage)
        self.current_hp = max(0, self.current_hp - actual_damage)
        if self.current_hp == 0:
            self.current_lives -= 1
            self.current_lives = max(0, self.current_lives)
            if self.current_lives > 0:
                self.current_hp = self.max_hp
        return actual_damage
    #

    def attack_enemies(self, enemies):
        if self.attack_cooldown > 0:
            return
        for enemy in enemies:
            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if distance <= self.attack_range + enemy.size:
                enemy.take_damage(self.attack)
                self.attack_cooldown = self.attack_delay
                break

    #

    def update(self, dt):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt


# ============================================================

# Camera



# ============================================================

# Projectile

class Projectile:

    def __init__(self, screen, x, y, direction, damage):

        self.screen = screen
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 500
        self.damage = damage
        self.size = 6
        self.colour = (255, 100, 50)

    ###

    def update(self, dt):
        self.x += (self.direction.x* self.speed* dt)
        self.y += (self.direction.y* self.speed* dt)

    #

    def render(self):
        pg.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

    #

    def collides_with_player(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance <= (player.size + self.size)

    #

    def is_on_screen(self):
        return (-50 <= self.x <= WIDTH + 50 and -50 <= self.y <= HEIGHT + 50)


# ============================================================

# Enemy

class Enemy:

    def __init__(self, screen, enemy_type, player):

        self.screen = screen
        self.player = player
        self.enemy_type = enemy_type
        self.x, self.y = (self.random_spawn_position())
        self.set_stats()
        self.attack_cooldown = 0
        self.attack_delay = 1.0
        self.projectiles = []

    ###

    def set_stats(self):

        if self.enemy_type == "Common":
            self.max_hp = random.randint(25, 50)
            self.current_hp = self.max_hp
            self.attack = random.randint(5, 10)
            self.speed = random.randint(330, 380)
            self.size = 12
            self.colour = (150, 150, 150)
            self.attack_range = 25
            self.attack_type = "melee"

        ##

        elif self.enemy_type == "Strong":
            self.max_hp = random.randint(50, 80)
            self.current_hp = self.max_hp
            self.attack = random.randint(10, 15)
            self.speed = random.randint(250, 300)
            self.size = 16
            self.colour = (220, 180, 60)
            self.attack_range = 150
            self.attack_type = random.choice(["melee", "projectile"])

        ##

        elif self.enemy_type == "Elite":
            self.max_hp = random.randint(150, 200)
            self.current_hp = self.max_hp
            self.attack = random.randint(20, 30)
            self.speed = random.randint(180, 220)
            self.size = 23
            self.colour = (180, 60, 220)
            self.attack_range = 35
            self.attack_type = random.choice(["melee", "projectile"])

        ##

        elif self.enemy_type == "Boss":
            self.max_hp = (self.player.max_hp * 5)
            self.current_hp = self.max_hp
            self.attack = (self.player.attack * 2)
            self.speed = random.randint(120, 160)
            self.size = 40
            self.colour = (180, 30, 30)
            self.attack_range = 50
            self.attack_type = random.choice(["melee","projectile"])

    #

    def random_spawn_position(self):

        side = random.randint(1, 4)
        if side == 1:
            return (random.randint(0, WIDTH), -50)
        elif side == 2:
            return (random.randint(0, WIDTH), HEIGHT + 50)
        elif side == 3:
            return (-50, random.randint(0, HEIGHT))
        else:
            return (WIDTH + 50, random.randint(0, HEIGHT))

    #

    def update(self, dt):

        self.attack_cooldown -= dt
        self.move_towards_player(dt)
        if self.attack_type == "projectile":
            self.update_projectiles(dt)
        self.check_attack()

    #

    def move_towards_player(self, dt):

        direction = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if direction.length() == 0:
            return
        direction = direction.normalize()
        self.x += (direction.x * self.speed * dt)
        self.y += (direction.y * self.speed * dt)

    #

    def check_attack(self):

        distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
        if self.attack_cooldown > 0:
            return

        ##
    
        if self.attack_type == "melee":
            collision_distance = (self.attack_range + self.player.size + self.size)
            if distance <= collision_distance:
                self.player.take_damage(self.attack)
                self.attack_cooldown = (self.attack_delay)

        ##

        elif self.attack_type == "projectile":
            if distance <= self.attack_range:
                self.shoot()
                self.attack_cooldown = (self.attack_delay)

    #

    def shoot(self):

        direction = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if direction.length() == 0:
            return
        direction = direction.normalize()
        projectile = Projectile(self.screen, self.x, self.y, direction, self.attack)
        self.projectiles.append(projectile)

    #

    def update_projectiles(self, dt):

        for projectile in self.projectiles[:]:
            projectile.update(dt)

            ##

            if projectile.collides_with_player(self.player):
                self.player.take_damage(projectile.damage)
                self.projectiles.remove(projectile)

            ##

            elif not projectile.is_on_screen():
                self.projectiles.remove(projectile)

    #

    def render(self):

        pg.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)
        for projectile in self.projectiles:
            projectile.render()

    #

    def take_damage(self, damage):

        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            return True
        return False


# ============================================================

# Enemy Manager

class EnemyManager:

    def __init__(self, screen, player):

        self.screen = screen
        self.player = player
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 2.0

    ####

    def update(self, dt):

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = (self.spawn_delay)

        ##

        for enemy in self.enemies[:]:
            enemy.update(dt)
            if enemy.current_hp <= 0:
                self.enemies.remove(enemy)

    # ========================================================

    # Spawn Enemy

    def spawn_enemy(self):

        roll = random.randint(1, 100)

        ##

        # 70% Common
        if roll <= 70:
            enemy_type = "Common"

        ##

        # 20% Strong
        elif roll <= 90:
            enemy_type = "Strong"

        ##

        # 8% Elite
        elif roll <= 98:
            enemy_type = "Elite"

        ##

        # 2% Boss
        else:
            enemy_type = "Boss"

        ##

        enemy = Enemy(self.screen, enemy_type, self.player)
        self.enemies.append(enemy)

    #

    def render(self):
        for enemy in self.enemies:
            enemy.render()
    
# ============================================================

# Background

class Background(pg.sprite.Sprite):

    def __init__(self, image_file, location):

        pg.sprite.Sprite.__init__(self)
        image_path = os.path.join(os.path.dirname(__file__), image_file)
        self.image = pg.image.load(image_path).convert()
        self.image = pg.transform.scale(self.image, (1200, 800))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# box setup
		self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l,t,w,h)

		# ground
		self.ground_surf = pygame.image.load('Images/Structures/Clouds 5.png').convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

		# camera speed
		self.keyboard_speed = 5
		self.mouse_speed = 0.2

		# zoom 
		self.zoom_scale = 1
		self.internal_surf_size = (2500,2500)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self,target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def box_target_camera(self,target):

		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = target.rect.left
		if target.rect.right > self.camera_rect.right:
			self.camera_rect.right = target.rect.right
		if target.rect.top < self.camera_rect.top:
			self.camera_rect.top = target.rect.top
		if target.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = target.rect.bottom

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
		if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
		if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
		if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def mouse_control(self):
		mouse = pygame.math.Vector2(pygame.mouse.get_pos())
		mouse_offset_vector = pygame.math.Vector2()

		left_border = self.camera_borders['left']
		top_border = self.camera_borders['top']
		right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
		bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

		if top_border < mouse.y < bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector.x = mouse.x - left_border
				pygame.mouse.set_pos((left_border,mouse.y))
			if mouse.x > right_border:
				mouse_offset_vector.x = mouse.x - right_border
				pygame.mouse.set_pos((right_border,mouse.y))
		elif mouse.y < top_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
				pygame.mouse.set_pos((left_border,top_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
				pygame.mouse.set_pos((right_border,top_border))
		elif mouse.y > bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
				pygame.mouse.set_pos((left_border,bottom_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
				pygame.mouse.set_pos((right_border,bottom_border))

		if left_border < mouse.x < right_border:
			if mouse.y < top_border:
				mouse_offset_vector.y = mouse.y - top_border
				pygame.mouse.set_pos((mouse.x,top_border))
			if mouse.y > bottom_border:
				mouse_offset_vector.y = mouse.y - bottom_border
				pygame.mouse.set_pos((mouse.x,bottom_border))

		self.offset += mouse_offset_vector * self.mouse_speed

	def zoom_keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			self.zoom_scale += 0.1
		if keys[pygame.K_e]:
			self.zoom_scale -= 0.1

	def custom_draw(self,player):
		
		# self.center_target_camera(player)
		# self.box_target_camera(player)
		# self.keyboard_control()
		self.mouse_control()
		self.zoom_keyboard_control()

		self.internal_surf.fill('#71ddee')

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
		self.internal_surf.blit(self.ground_surf,ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image,offset_pos)

		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector * self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center = (self.half_w,self.half_h))

		self.display_surface.blit(scaled_surf,scaled_rect)
