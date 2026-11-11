import pygame as pg
import random
import math
from pathlib import Path
from Ruins import RuinsArt, RuinsGate, GATE_X, GATE_Y
from DungeonLayout import REGIONS, ROOMS, CORRIDORS, GATES, BOSS_ROOMS, START_X, START_Y

###

IMAGE_FOLDER = Path(__file__).resolve().parent / "Images"

MAP_WIDTH = 23040
MAP_HEIGHT = 23040

###

def load_player_animation(character, action, scale=128):
    path = IMAGE_FOLDER / f"Characters/{character}/{action}.png"
    sheet = pg.image.load(path).convert_alpha()

    if character == "Rogue":
        frame_size = 256
    else:
        frame_size = 128

    frames = []
    for x in range(0, sheet.get_width(), frame_size):
        frame = sheet.subsurface((x, 0, frame_size, frame_size)).copy()
        frame = pg.transform.scale(frame, (scale, scale))
        frames.append(frame)

    return frames

#

def load_enemy_animation(slime_number, action, scale=128):

    path = IMAGE_FOLDER / f"Enemy/Slime{slime_number}/With_shadow/Slime{slime_number}_{action}_with_shadow.png"
    sheet = pg.image.load(path).convert_alpha()
    frame_size = 64
    frames_by_direction = []
    for row in range(sheet.get_height() // frame_size):
        row_frames = []
        for x in range(0, sheet.get_width(), frame_size):
            frame = sheet.subsurface((x, row * frame_size, frame_size, frame_size)).copy()
            frame = pg.transform.scale(frame, (scale, scale))
            row_frames.append(frame)
        frames_by_direction.append(row_frames)
    return frames_by_direction

#================================================

#Map

class Map:

    def __init__(self):

        self.gate = RuinsGate()
        self.ruins_art = RuinsArt(IMAGE_FOLDER)
        self.rooms = []
        self.room_floors = []
        self.corridors = []
        for name, region, x, y, width, height in ROOMS:
            rect = pg.Rect(x, y, width, height)
            self.rooms.append((name, region, rect))
            shape = (len(self.rooms) + region) % 4
            for floor in self.room_shape(rect, shape):
                self.room_floors.append((name, region, floor))
        for region, x, y, width, height in CORRIDORS:
            self.corridors.append((region, pg.Rect(x, y, width, height)))

    #

    def room_shape(self, rect, shape):

        x, y, width, height = rect
        inset_x = width // 6
        inset_y = height // 6
        if shape == 0:
            # Stepped oval.
            return [
                pg.Rect(x + inset_x * 2, y, width - inset_x * 4, height),
                pg.Rect(x + inset_x, y + inset_y // 2, width - inset_x * 2, height - inset_y),
                pg.Rect(x, y + inset_y * 2, width, height - inset_y * 4)
            ]
        if shape == 1:
            # Wide middle with clipped corners.
            return [
                pg.Rect(x + inset_x, y, width - inset_x * 2, height),
                pg.Rect(x, y + inset_y, width, height - inset_y * 2)
            ]
        if shape == 2:
            # Offset chambers, with a notch in opposite corners.
            return [
                pg.Rect(x, y, width - inset_x, height - inset_y),
                pg.Rect(x + inset_x, y + inset_y, width - inset_x, height - inset_y)
            ]
        # Broad lower chamber with a narrow upper end.
        return [
            pg.Rect(x + inset_x, y, width - inset_x * 2, height),
            pg.Rect(x, y + inset_y * 2, width, height - inset_y * 3)
        ]

    #

    def is_walkable(self, x, y):

        for name, region, rect in self.room_floors:
            if rect.collidepoint(x, y):
                return True
        for region, rect in self.corridors:
            if rect.collidepoint(x, y):
                return True
        return False

    #

    def location_name(self, x, y):

        for name, region, rect in self.room_floors:
            if rect.collidepoint(x, y):
                return f"{REGIONS[region][0]}  /  {name}"
        return "Connecting passage"

    #

    def can_move_circle(self, x, y, radius):

        if self.gate.blocks(x, y, radius) or self.ruins_art.blocks(x, y, radius):
            return False
        points = [(x - radius, y), (x + radius, y), (x, y - radius), (x, y + radius)]
        for point_x, point_y in points:
            if not self.is_walkable(point_x, point_y):
                return False
        return True

    #

    def random_enemy_spawn_position(self, player_x=None, player_y=None):

        for attempt in range(100):
            name, region, rect = random.choice(self.rooms)
            x = random.randint(rect.left + 50, rect.right - 50)
            y = random.randint(rect.top + 50, rect.bottom - 50)
            if not self.can_move_circle(x, y, 40):
                continue
            if player_x is None or player_y is None:
                return x, y
            distance = math.hypot(x - player_x, y - player_y)
            if distance > 900:
                return x, y
        return rect.center

    #

    def render(self, screen, camera):
        view = screen.get_rect()
        origin = camera.apply(0, 0)
        for region, rect in self.corridors:
            wall_rect = pg.Rect(camera.apply(rect.x, rect.y), rect.size).inflate(24, 24)
            if view.colliderect(wall_rect):
                pg.draw.rect(screen, (26, 29, 42), wall_rect)
        for name, region, rect in self.room_floors:
            wall_rect = pg.Rect(camera.apply(rect.x, rect.y), rect.size).inflate(24, 24)
            if view.colliderect(wall_rect):
                pg.draw.rect(screen, (26, 29, 42), wall_rect)
        for region, rect in self.corridors:
            visible_rect = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if view.colliderect(visible_rect):
                colour = (48, 52, 65)
                if region >= 0:
                    red, green, blue = REGIONS[region][1]
                    colour = (red * 3 // 4, green * 3 // 4, blue * 3 // 4)
                pg.draw.rect(screen, colour, visible_rect)
                if region == 0:
                    self.ruins_art.draw_floor(screen, visible_rect, view, origin)
        for name, region, rect in self.room_floors:
            visible_rect = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if view.colliderect(visible_rect):
                pg.draw.rect(screen, REGIONS[region][1], visible_rect)
                if region == 0:
                    self.ruins_art.draw_floor(screen, visible_rect, view, origin)
        for first_region, second_region, x, y in GATES:
            if (x, y) == (GATE_X, GATE_Y):
                continue
            gate_x, gate_y = camera.apply(x, y)
            pg.draw.rect(screen, (197, 168, 105), (gate_x - 6, gate_y - 6, 12, 12))
        self.ruins_art.render(screen, camera)
        self.gate.render(screen, camera)

    #

    def render_overview(self, screen, player, font):

        panel = pg.Rect(0, 0, 780, 650)
        panel.center = screen.get_rect().center
        pg.draw.rect(screen, (15, 19, 30), panel)
        map_x = panel.x + 16
        map_y = panel.y + 42
        scale = MAP_WIDTH / 600
        title = font.render("Dungeon layout   |   M to close", True, (238, 242, 247))
        screen.blit(title, (map_x, panel.y + 12))
        for region, rect in self.corridors:
            pg.draw.rect(screen, (64, 69, 85), (map_x + rect.x // scale, map_y + rect.y // scale, rect.width // scale, rect.height // scale))
        for name, region, rect in self.room_floors:
            pg.draw.rect(screen, REGIONS[region][1], (map_x + rect.x // scale, map_y + rect.y // scale, rect.width // scale, rect.height // scale))
        for name, region, rect in self.rooms:
            if name in BOSS_ROOMS:
                x = map_x + rect.centerx // scale
                y = map_y + rect.centery // scale
                colour = (183, 225, 193)
                if name != BOSS_ROOMS[0]:
                    colour = (240, 166, 169)
                pg.draw.polygon(screen, colour, [(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)])
        for first_region, second_region, x, y in GATES:
            pg.draw.circle(screen, (197, 168, 105), (map_x + x // scale, map_y + y // scale), 3)
        pg.draw.circle(screen, (250, 250, 250), (map_x + int(player.x) // scale, map_y + int(player.y) // scale), 5)
        for region in range(len(REGIONS)):
            name, colour = REGIONS[region]
            legend_y = map_y + region * 25
            pg.draw.rect(screen, colour, (panel.right - 160, legend_y + 4, 10, 10))
            screen.blit(font.render(name, True, (238, 242, 247)), (panel.right - 143, legend_y))
        for label, colour in [("Planned gate", (197, 168, 105)), ("First boss arena", (183, 225, 193)), ("Ultra Boss arena", (240, 166, 169))]:
            legend_y += 25
            pg.draw.rect(screen, colour, (panel.right - 160, legend_y + 4, 10, 10))
            screen.blit(font.render(label, True, (238, 242, 247)), (panel.right - 143, legend_y))


#================================================

# Player

class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.x = START_X
        self.y = START_Y
        self.speed = 600
        self.size = 30
        self.visionRadius = 300

        self.max_hp = 100
        self.current_hp = self.max_hp

        self.defence = 50

        self.attack = 20
        self.attack_range = 100
        self.attack_cooldown = 0
        self.attack_delay = 0.3

        self.max_lives = 7
        self.current_lives = self.max_lives
        self.facing = "down"
        self.moving = False
        self.animation_time = 0
        self.attack_animation_time = 0

        self.block_duration = 0.28
        self.block_cooldown_length = 1.5
        self.block_time = 0
        self.block_cooldown = 0

        self.dash_duration = 0.5
        self.dash_cooldown_length = 2.0
        self.dash_speed = 1120
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_direction = pg.Vector2(0, 0)

        # Samurai

        # self.idle_frames = load_player_animation("Samurai", "Idle")
        # self.run_frames = load_player_animation("Samurai", "Run")
        # self.attack_frames = load_player_animation("Samurai", "Attack_1")
        # self.shield_frames = load_player_animation("Samurai", "Shield")

        # Shinobi

        # self.idle_frames = load_player_animation("Shinobi", "Idle")
        # self.run_frames = load_player_animation("Shinobi", "Run")
        # self.attack_frames = load_player_animation("Shinobi", "Attack_1")
        # self.shield_frames = load_player_animation("Shinobi", "Shield")

        # Fighter

        # self.idle_frames = load_player_animation("Fighter", "Idle")
        # self.run_frames = load_player_animation("Fighter", "Run")
        # self.attack_frames = load_player_animation("Fighter", "Attack_1")
        # self.shield_frames = load_player_animation("Fighter", "Shield")

        #Rogue

        self.idle_frames = load_player_animation("Rogue", "idle")
        self.run_frames = load_player_animation("Rogue", "run")
        self.attack_frames = load_player_animation("Rogue", "attack")
        self.shield_frames = load_player_animation("Rogue", "shield")   

        self.white_shield_frames = []
        for frame in self.shield_frames:
            white_frame = frame.copy()
            white_frame.fill((255, 255, 255), special_flags=pg.BLEND_RGB_ADD)
            self.white_shield_frames.append(white_frame)

    #

    def begin_block(self):

        if self.block_cooldown > 0 or self.block_time > 0:
            return False
        self.block_time = self.block_duration
        self.block_cooldown = self.block_cooldown_length
        self.animation_time = 0
        return True

    #

    def begin_dash(self):

        if self.dash_cooldown > 0 or self.dash_time > 0:
            return False
        keys = pg.key.get_pressed()
        dx = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(keys[pg.K_a] or keys[pg.K_LEFT])
        dy = int(keys[pg.K_s] or keys[pg.K_DOWN]) - int(keys[pg.K_w] or keys[pg.K_UP])
        if dx or dy:
            self.dash_direction = pg.Vector2(dx, dy).normalize()
            if abs(dx) >= abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"
        elif self.facing == "up":
            self.dash_direction = pg.Vector2(0, -1)
        elif self.facing == "down":
            self.dash_direction = pg.Vector2(0, 1)
        elif self.facing == "left":
            self.dash_direction = pg.Vector2(-1, 0)
        else:
            self.dash_direction = pg.Vector2(1, 0)
        self.dash_time = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_length
        return True

    #

    def keybinds(self, dt, game_map):

        keys = pg.key.get_pressed()
        dx = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(keys[pg.K_a] or keys[pg.K_LEFT])
        dy = int(keys[pg.K_s] or keys[pg.K_DOWN]) - int(keys[pg.K_w] or keys[pg.K_UP])
        self.moving = bool(dx or dy)
        if self.moving:
            direction = pg.Vector2(dx, dy).normalize()
            if abs(dx) >= abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"
        if self.dash_time > 0:
            move_x = self.dash_direction.x * self.dash_speed * dt
            move_y = self.dash_direction.y * self.dash_speed * dt
            self._move(move_x, move_y, game_map)
            self.dash_time = max(0, self.dash_time - dt)
            self.moving = True
        elif self.moving:
            direction = pg.Vector2(dx, dy).normalize()
            move_x = direction.x * self.speed * dt
            move_y = direction.y * self.speed * dt
            self._move(move_x, move_y, game_map)

    #

    def _move(self, move_x, move_y, game_map):

        if game_map.can_move_circle(self.x + move_x, self.y, self.size):
            self.x += move_x
        elif self.dash_time > 0:
            self.dash_time = 0
        if game_map.can_move_circle(self.x, self.y + move_y, self.size):
            self.y += move_y
        elif move_y and self.dash_time > 0:
            self.dash_time = 0

    #

    def render(self, camera):

        if self.block_time > 0:
            frames = self.white_shield_frames
            elapsed = self.block_duration - self.block_time
            frame = frames[min(len(frames) - 1, int(elapsed / 0.09))]
        elif self.attack_animation_time > 0:
            frame_number = int((0.3 - self.attack_animation_time) / 0.05)
            frame_number = min(len(self.attack_frames) - 1, frame_number)
            frame = self.attack_frames[frame_number]
        elif self.moving:
            frame_number = int(self.animation_time * 12) % len(self.run_frames)
            frame = self.run_frames[frame_number]
        else:
            frame_number = int(self.animation_time * 5) % len(self.idle_frames)
            frame = self.idle_frames[frame_number]
        if self.facing == "left":
            frame = pg.transform.flip(frame, True, False)
        screen_x, screen_y = camera.apply(self.x, self.y)
        self.screen.blit(frame, frame.get_rect(midbottom=(screen_x, screen_y + 28)))
        if self.block_time > 0:
            pg.draw.circle(self.screen, (205, 230, 255), (screen_x, screen_y), 48, 3)

    #

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    #

    def pvisionRadius(self):
        return self.visionRadius

    #

    def take_damage(self, incoming_damage):

        damage_multiplier = self.max_hp / (self.max_hp + self.defence)
        actual_damage = max(1, round(incoming_damage * damage_multiplier))
        if self.block_time > 0:
            actual_damage = max(1, round(actual_damage * 0.2))
        self.current_hp = max(0, self.current_hp - actual_damage)
        if self.current_hp == 0:
            self.current_lives = max(0, self.current_lives - 1)
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
                self.attack_animation_time = 0.3
                break
    
    #

    def update(self, dt):

        self.animation_time += dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_animation_time = max(0, self.attack_animation_time - dt)
        self.block_time = max(0, self.block_time - dt)
        self.block_cooldown = max(0, self.block_cooldown - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)

#================================================

# Camera

class Camera:

    def __init__(self, screen, world_width, world_height):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pg.Vector2(0, 0)
        self.left_border = 400
        self.right_border = 400
        self.top_border = 200
        self.bottom_border = 200

    #

    def update(self, player):

        screen_x = player.x - self.offset.x
        screen_y = player.y - self.offset.y
        if screen_x < self.left_border:
            self.offset.x = player.x - self.left_border
        elif screen_x > self.screen_width - self.right_border:
            self.offset.x = player.x - (self.screen_width - self.right_border)
        if screen_y < self.top_border:
            self.offset.y = player.y - self.top_border
        elif screen_y > self.screen_height - self.bottom_border:
            self.offset.y = player.y - (self.screen_height - self.bottom_border)
        max_offset_x = max(0, self.world_width - self.screen_width)
        max_offset_y = max(0, self.world_height - self.screen_height)
        self.offset.x = max(0, min(self.offset.x, max_offset_x))
        self.offset.y = max(0, min(self.offset.y, max_offset_y))

    #

    def apply(self, x, y):
        return round(x - self.offset.x), round(y - self.offset.y)

#================================================

# Projectile

class Projectile:

    def __init__(self, screen, x, y, direction, damage):

        self.screen = screen
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1000
        self.damage = damage
        self.size = 12
        self.colour = (190, 225, 255)

    #

    def update(self, dt):
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt

    #

    def render(self, camera):
        screen_position = camera.apply(self.x, self.y)
        pg.draw.circle(self.screen, self.colour, screen_position, self.size)

    #

    def collides_with_player(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance <= player.size + self.size

    #

    def is_on_screen(self):
        return (-50 <= self.x <= MAP_WIDTH + 50 and -50 <= self.y <= MAP_HEIGHT + 50)

#================================================

# Enemy

class Enemy:
    def __init__(self, screen, enemy_type, player, game_map=None):

        self.screen = screen
        self.player = player
        self.game_map = game_map
        self.enemy_type = enemy_type
        self.x, self.y = self.random_spawn_position()
        self.set_stats()
        self.attack_cooldown = 0
        self.attack_delay = 2.0
        self.projectiles = []
        self.animation_time = random.random()
        self.attack_animation_time = 0
        self.facing_row = 0
        self.idle_frames = load_enemy_animation(self.slime_number, "Idle", self.sprite_scale)
        self.run_frames = load_enemy_animation(self.slime_number, "Run", self.sprite_scale)
        self.attack_frames = load_enemy_animation(self.slime_number, "Attack", self.sprite_scale)

    #

    def set_stats(self):

        if self.enemy_type == "Common":
            self.max_hp = random.randint(25, 50)
            self.attack = random.randint(5, 10)
            self.speed = random.randint(125, 300)
            self.size = 24
            self.slime_number = 1
            self.sprite_scale = 128
            self.attack_range = 25
            self.attack_type = "melee"

        elif self.enemy_type == "Strong":
            self.max_hp = random.randint(50, 80)
            self.attack = random.randint(10, 15)
            self.speed = random.randint(100, 275)
            self.size = 32
            self.slime_number = 2
            self.sprite_scale = 144
            self.attack_range = 50
            self.attack_type = random.choice(["melee", "projectile"])

        elif self.enemy_type == "Elite":
            self.max_hp = random.randint(150, 200)
            self.attack = random.randint(20, 30)
            self.speed = random.randint(75, 250)
            self.size = 46
            self.slime_number = 3
            self.sprite_scale = 160
            self.attack_range = 75
            self.attack_type = random.choice(["melee", "projectile"])

        else:
            self.max_hp = self.player.max_hp * 5
            self.attack = self.player.attack * 2
            self.speed = random.randint(50, 200)
            self.size = 64
            self.slime_number = 3
            self.sprite_scale = 224
            self.attack_range = 100
            self.attack_type = "projectile"

        self.current_hp = self.max_hp

    #

    def random_spawn_position(self):

        if self.game_map is not None:
            return self.game_map.random_enemy_spawn_position(self.player.x, self.player.y)
        return random.randint(0, MAP_WIDTH), random.randint(0, MAP_HEIGHT)

    #

    def update(self, dt):

        self.animation_time += dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_animation_time = max(0, self.attack_animation_time - dt)
        self.move_towards_player(dt)
        if self.attack_type == "projectile":
            self.update_projectiles(dt)
        self.check_attack()

    #

    def move_towards_player(self, dt):

        dx = self.player.x - self.x
        dy = self.player.y - self.y
        direction = pg.Vector2(dx, dy)
        if direction.length() == 0:
            return
        if abs(dx) > abs(dy):
            self.facing_row = 2 if dx > 0 else 1
        else:
            self.facing_row = 0 if dy > 0 else 3
        distance = direction.length()
        direction = direction.normalize()
        move_x = direction.x * self.speed * dt
        move_y = direction.y * self.speed * dt
        if distance > self.attack_range:
            if self.game_map is None:
                self.x += move_x
                self.y += move_y
            else:
                if self.game_map.can_move_circle(self.x + move_x, self.y, self.size):
                    self.x += move_x
                if self.game_map.can_move_circle(self.x, self.y + move_y, self.size):
                    self.y += move_y

    #
    
    def check_attack(self):

        distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
        if self.attack_cooldown > 0:
            return
        if self.attack_type == "melee":
            collision_distance = self.attack_range + self.player.size + self.size
            if distance <= collision_distance:
                self.player.take_damage(self.attack)
                self.attack_cooldown = self.attack_delay
                self.attack_animation_time = 0.3
        elif self.attack_type == "projectile":
            if distance <= self.attack_range:
                self.shoot()
                self.attack_cooldown = self.attack_delay
                self.attack_animation_time = 0.3

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

        projectiles_to_update = self.projectiles[:]
        for projectile in projectiles_to_update:
            projectile.update(dt)
            if projectile.collides_with_player(self.player):
                self.player.take_damage(projectile.damage)
                self.projectiles.remove(projectile)
            elif not projectile.is_on_screen():
                self.projectiles.remove(projectile)

    #

    def render(self, camera):

        if self.attack_animation_time > 0:
            frames = self.attack_frames[self.facing_row]
            frame_number = int((0.3 - self.attack_animation_time) * 16)
            frame_number = min(len(frames) - 1, frame_number)
            frame = frames[frame_number]
        else:
            distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
            if distance > self.attack_range:
                frames = self.run_frames[self.facing_row]
                frame = frames[int(self.animation_time * 10) % len(frames)]
            else:
                frames = self.idle_frames[self.facing_row]
                frame = frames[int(self.animation_time * 5) % len(frames)]
        screen_x, screen_y = camera.apply(self.x, self.y)
        self.screen.blit(frame, frame.get_rect(midbottom=(screen_x, screen_y + 14)))
        bar_width = self.size * 2
        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - self.size - 24
        pg.draw.rect(self.screen, (27, 31, 41), (bar_x, bar_y, bar_width, 7))
        pg.draw.rect(self.screen, (145, 190, 220), (bar_x, bar_y, bar_width * self.current_hp / self.max_hp, 7))
        for projectile in self.projectiles:
            projectile.render(camera)

    #

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0
            return True
        return False

#================================================

# Enemy manager

class EnemyManager:

    def __init__(self, screen, player, game_map=None):

        self.screen = screen
        self.player = player
        self.game_map = game_map
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 2.0

    #

    def update(self, dt):

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_delay
        enemies_to_update = self.enemies[:]
        for enemy in enemies_to_update:
            enemy.update(dt)
            if enemy.current_hp <= 0:
                self.enemies.remove(enemy)
    
    #

    def spawn_enemy(self):

        roll = random.randint(1, 100)
        if roll <= 70:
            enemy_type = "Common"
        elif roll <= 90:
            enemy_type = "Strong"
        elif roll <= 98:
            enemy_type = "Elite"
        else:
            enemy_type = "Boss"

        enemy = Enemy(self.screen, enemy_type, self.player, self.game_map)
        self.enemies.append(enemy)

    #

    def render(self, camera):
        for enemy in self.enemies:
            enemy.render(camera)

#================================================

#Background

class Background:

    def __init__(self, image_file, world_width, world_height):

        self.image = pg.image.load(image_file).convert()
        self.image = pg.transform.scale(self.image, (world_width, world_height))
        self.rect = self.image.get_rect(topleft=(0, 0))

    #

    def render(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect.x, self.rect.y))

