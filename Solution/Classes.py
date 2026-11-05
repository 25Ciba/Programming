import pygame as pg
import random
import math
import os

# ============================================================

# Screen and world dimensions

TILE_SIZE = 32 # Tiles are scaled to 200% (from 16 px).
GRID_WIDTH = 150
GRID_HEIGHT = 110
MAP_WIDTH = GRID_WIDTH * TILE_SIZE
MAP_HEIGHT = GRID_HEIGHT * TILE_SIZE
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")
CHARACTER_FOLDER = os.path.join(IMAGE_FOLDER, "Characters")
ENEMY_FOLDER = os.path.join(IMAGE_FOLDER, "Enemy")

# ============================================================

def load_player_animation(character, action, scale=128):

    path = os.path.join(CHARACTER_FOLDER, character, f"{action}.png")
    sheet = pg.image.load(path).convert_alpha()
    frames = []
    for x in range(0, sheet.get_width(), 128):
        frame = sheet.subsurface((x, 0, 128, 128)).copy()
        frames.append(pg.transform.scale(frame, (scale, scale)))
    return frames

def load_enemy_animation(slime_number, action, scale=128):

    filename = f"Slime{slime_number}_{action}_with_shadow.png"
    path = os.path.join(ENEMY_FOLDER, f"Slime{slime_number}", "With_shadow", filename)
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

# ============================================================

# Dungeon map

class DungeonMap:

    REGIONS = {
        "Obsidian Halls": {"colour": (48, 55, 67), "tileset": 0}, 
        "Frostglass Wing": {"colour": (54, 68, 84), "tileset": 2},
        "Glacier Archive": {"colour": (48, 65, 79), "tileset": 3},
        "Blue-Ice Reliquary": { "colour": (57, 72, 91), "tileset": 1},
        "Eclipse Keep": {"colour": (43, 49, 65), "tileset": 4}
        }

    def __init__(self):

        self.rooms = [

            ("start", "Whispering Shrine", "Obsidian Halls", 82, 94, 16, 12),
            ("south_hall", "Silent Gallery", "Frostglass Wing", 65, 80, 20, 13),
            ("south_vault", "Sunken Vault", "Glacier Archive", 103, 78, 21, 14),
            ("lower_hall", "Rootbound Passage", "Obsidian Halls", 77, 73, 20, 14),
            ("central", "Resonant Crossroads", "Obsidian Halls", 62, 50, 30, 18),
            ("west_hall", "Moss-Covered Cloister", "Obsidian Halls", 39, 50, 19, 14),
            ("west_shrine", "Forgotten Shrine", "Blue-Ice Reliquary", 10, 42, 20, 15),
            ("west_vault", "Buried Reliquary", "Blue-Ice Reliquary", 28, 72, 20, 14),
            ("north_hall", "The Pale Nave", "Frostglass Wing", 66, 18, 19, 18),
            ("northwest", "Moonlit Conservatory", "Frostglass Wing", 34, 18, 21, 15),
            ("northeast", "Hall of Glass", "Frostglass Wing", 101, 18, 23, 15),
            ("east_archive", "The Drowned Archive", "Glacier Archive", 109, 44, 24, 15),
            ("east_hall", "Ashen Gallery", "Blue-Ice Reliquary", 121, 68, 20, 15),
            ("boss", "The Eclipse Throne", "Eclipse Keep", 125, 91, 20, 14)

        ]

        self.grid = [
            [False for _ in range(GRID_WIDTH)]
            for _ in range(GRID_HEIGHT)
        ]
        self.region_grid = [
            [None for _ in range(GRID_WIDTH)]
            for _ in range(GRID_HEIGHT)
        ]

        self.floor_tiles = []
        self.doors = []

        self._load_tiles()
        self._carve_rooms()
        self._connect_rooms()
        self._create_doors()
        self.surface = self._build_surface()

        self.walkable_positions = [
            (
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2
            )
            for y in range(GRID_HEIGHT)
            for x in range(GRID_WIDTH)
            if self.grid[y][x]
        ]

    ###

    @property
    def pixel_width(self):
        return MAP_WIDTH

    #

    @property
    def pixel_height(self):
        return MAP_HEIGHT

    ###

    def _load_tiles(self):

        tile_folder = os.path.join(IMAGE_FOLDER, "Tiles")


        for number in range(1, 6):
            tile_path = os.path.join(tile_folder, f"Road{number}.png")
            sheet = pg.image.load(tile_path).convert_alpha()
            source_tile = sheet.subsurface((32, 32, 16, 16)).copy()
            tile = pg.transform.scale(source_tile, (TILE_SIZE, TILE_SIZE))

            ice_tint = pg.Surface(tile.get_size(), pg.SRCALPHA)
            ice_tint.fill((145, 165, 190, 115))
            tile.blit(ice_tint, (0, 0))

            darken = pg.Surface(tile.get_size(), pg.SRCALPHA)
            darken.fill((8, 13, 24, 75))
            tile.blit(darken, (0, 0))

            self.floor_tiles.append(tile)

    #

    def _room_by_id(self, room_id):

        for room in self.rooms:
            if room[0] == room_id:
                return room

        return None

    #

    @staticmethod
    def _room_centre(room):

        _, _, _, x, y, width, height = room
        return x + width // 2, y + height // 2

    #

    def _carve_rect(self, x, y, width, height, region):

        for tile_y in range(y, y + height):
            for tile_x in range(x, x + width):
                if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
                    self.grid[tile_y][tile_x] = True
                    self.region_grid[tile_y][tile_x] = region

    #

    def _carve_rooms(self):

        for room in self.rooms:
            _, _, region, x, y, width, height = room
            self._carve_rect(x, y, width, height, region)

    #

    def _carve_corridor(self, start, end, region, horizontal_first=True):

        x1, y1 = start
        x2, y2 = end
        corridor_width = 6
        half_width = corridor_width // 2

        def carve_horizontal(a, b, y):
            left = min(a, b)
            right = max(a, b)
            self._carve_rect(
                left,
                y - half_width,
                right - left + 1,
                corridor_width,
                region
            )

        def carve_vertical(x, a, b):
            top = min(a, b)
            bottom = max(a, b)
            self._carve_rect(
                x - half_width,
                top,
                corridor_width,
                bottom - top + 1,
                region
            )

        if horizontal_first:
            carve_horizontal(x1, x2, y1)
            carve_vertical(x2, y1, y2)
        else:
            carve_vertical(x1, y1, y2)
            carve_horizontal(x1, x2, y2)

    #

    def _connect_rooms(self):

        links = [
            ("start", "south_hall", False),
            ("south_hall", "lower_hall", True),
            ("lower_hall", "south_vault", True),
            ("lower_hall", "central", False),
            ("south_hall", "boss", True),
            ("central", "west_hall", True),
            ("west_hall", "west_shrine", True),
            ("west_hall", "west_vault", False),
            ("west_vault", "lower_hall", True),
            ("central", "north_hall", False),
            ("north_hall", "northwest", True),
            ("north_hall", "northeast", True),
            ("northeast", "east_archive", False),
            ("east_archive", "east_hall", False),
            ("east_hall", "boss", False)
        ]

        for room_a_id, room_b_id, horizontal_first in links:
            room_a = self._room_by_id(room_a_id)
            room_b = self._room_by_id(room_b_id)

            self._carve_corridor(
                self._room_centre(room_a),
                self._room_centre(room_b),
                room_a[2],
                horizontal_first
            )

    #

    def _create_doors(self):


        door_tiles = [
            (90, 92), (81, 86), (105, 80), (87, 68), (110, 86),
            (58, 59), (32, 57), (48, 68), (61, 79), (77, 42),
            (57, 27), (95, 27), (112, 39), (121, 63), (131, 87)
        ]

        for tile_x, tile_y in door_tiles:
            self.doors.append({
                "x": tile_x,
                "y": tile_y,
                "open": True
            })

    #

    def _build_surface(self):

        surface = pg.Surface((MAP_WIDTH, MAP_HEIGHT))
        surface.fill((10, 13, 21))


        for tile_y in range(GRID_HEIGHT):
            for tile_x in range(GRID_WIDTH):
                if not self.grid[tile_y][tile_x]:
                    continue

                region = self.region_grid[tile_y][tile_x]
                region_data = self.REGIONS[region]
                tile_index = region_data["tileset"]
                rect = pg.Rect(
                    tile_x * TILE_SIZE,
                    tile_y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pg.draw.rect(surface, region_data["colour"], rect)
                surface.blit(self.floor_tiles[tile_index], rect.topleft)


                pg.draw.line(
                    surface,
                    (27, 34, 47),
                    rect.bottomleft,
                    rect.bottomright,
                    1
                )


        for tile_y in range(GRID_HEIGHT):
            for tile_x in range(GRID_WIDTH):
                if self.grid[tile_y][tile_x]:
                    continue

                touches_floor = any(
                    0 <= tile_x + dx < GRID_WIDTH and
                    0 <= tile_y + dy < GRID_HEIGHT and
                    self.grid[tile_y + dy][tile_x + dx]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                )

                if not touches_floor:
                    continue

                rect = pg.Rect(
                    tile_x * TILE_SIZE,
                    tile_y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                wall_tile = self.floor_tiles[(tile_x + tile_y) % 5]
                surface.blit(wall_tile, rect.topleft)
                pg.draw.rect(surface, (20, 25, 36), rect, 2)
                pg.draw.line(
                    surface,
                    (10, 13, 20),
                    rect.bottomleft,
                    rect.bottomright,
                    3
                )

        return surface.convert()

    #

    def is_walkable(self, x, y):

        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)

        if not (0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT):
            return False

        if not self.grid[tile_y][tile_x]:
            return False

        for door in self.doors:
            if door["open"]:
                continue

            door_rect = pg.Rect(
                door["x"] * TILE_SIZE,
                door["y"] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            if door_rect.collidepoint(x, y):
                return False

        return True

    #

    def can_move_circle(self, x, y, radius):

        check_points = (
            (x - radius, y),
            (x + radius, y),
            (x, y - radius),
            (x, y + radius)
        )

        return all(
            self.is_walkable(point_x, point_y)
            for point_x, point_y in check_points
        )

    #

    def random_enemy_spawn_position(self, player_x=None, player_y=None):

        for _ in range(100):
            position = random.choice(self.walkable_positions)

            if player_x is None or player_y is None:
                return position

            distance = math.hypot(
                position[0] - player_x,
                position[1] - player_y
            )

            if distance > 900:
                return position

        return random.choice(self.walkable_positions)

    #

    def nearest_door(self, x, y):

        nearest = None
        nearest_distance = 96

        for door in self.doors:
            door_x = door["x"] * TILE_SIZE + TILE_SIZE // 2
            door_y = door["y"] * TILE_SIZE + TILE_SIZE // 2
            distance = math.hypot(door_x - x, door_y - y)

            if distance < nearest_distance:
                nearest = door
                nearest_distance = distance

        return nearest

    #

    def interact(self, x, y):

        door = self.nearest_door(x, y)

        if door is None:
            return "There is no door nearby."

        door["open"] = not door["open"]

        if door["open"]:
            return "Door opened."

        return "Door closed."

    #

    def render(self, screen, camera):

        screen.blit(self.surface, camera.apply(0, 0))

        for door in self.doors:
            screen_x = round(door["x"] * TILE_SIZE - camera.offset.x)
            screen_y = round(door["y"] * TILE_SIZE - camera.offset.y)
            rect = pg.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

            if door["open"]:

                pg.draw.rect(screen, (92, 115, 139), rect, 3)
            else:

                pg.draw.rect(screen, (35, 47, 64), rect)
                pg.draw.rect(screen, (129, 157, 187), rect, 3)
                pg.draw.line(
                    screen,
                    (185, 218, 244),
                    (rect.centerx, rect.top + 3),
                    (rect.centerx, rect.bottom - 3),
                    2
                )
                pg.draw.circle(
                    screen,
                    (205, 229, 250),
                    (rect.right - 7, rect.centery),
                    3
                )


# ============================================================

# Player

class Player(pg.sprite.Sprite):

    def __init__(self, screen):

        super().__init__()

        self.screen = screen
        self.x = MAP_WIDTH / 2
        self.y = MAP_HEIGHT / 2
        self.speed = 600
        self.size = 30
        self.visionRadius = 300
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.defence = 50
        self.attack = 20
        self.attack_range = 200
        self.attack_cooldown = 0
        self.attack_delay = 0.3
        self.max_lives = 7
        self.current_lives = self.max_lives

        self.facing = "down"
        self.moving = False
        self.animation_time = 0
        self.attack_animation_time = 0

        # Block
        self.block_duration = 0.28
        self.block_cooldown_length = 1.5
        self.block_time = 0
        self.block_cooldown = 0

        # Dash
        self.dash_duration = 0.5
        self.dash_cooldown_length = 2.0
        self.dash_speed = 1120
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_direction = pg.Vector2(0, 0)

        self.animations = {
            "Idle": load_player_animation("Samurai", "Idle"),
            "Run": load_player_animation("Samurai", "Run"),
            "Attack": load_player_animation("Samurai", "Attack_1"),
            "Shield": load_player_animation("Samurai", "Shield")
        }

        self.white_shield_frames = [
            self._make_white(frame)
            for frame in self.animations["Shield"]
        ]

    ###

    @staticmethod
    def _make_white(frame):

        white_frame = frame.copy()
        white_frame.fill(
            (255, 255, 255),
            special_flags=pg.BLEND_RGB_ADD
        )
        return white_frame

    #

    @property
    def blocking(self):
        return self.block_time > 0

    #

    @property
    def dashing(self):
        return self.dash_time > 0

    ###

    def begin_block(self):

        if self.block_cooldown > 0 or self.blocking:
            return False

        self.block_time = self.block_duration
        self.block_cooldown = self.block_cooldown_length
        self.animation_time = 0
        return True

    #

    def begin_dash(self):

        if self.dash_cooldown > 0 or self.dashing:
            return False

        keys = pg.key.get_pressed()
        dx = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(
            keys[pg.K_a] or keys[pg.K_LEFT]
        )
        dy = int(keys[pg.K_s] or keys[pg.K_DOWN]) - int(
            keys[pg.K_w] or keys[pg.K_UP]
        )

        if dx or dy:
            self.dash_direction = pg.Vector2(dx, dy).normalize()
            if abs(dx) >= abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"
        else:
            directions = {
                "up": pg.Vector2(0, -1),
                "down": pg.Vector2(0, 1),
                "left": pg.Vector2(-1, 0),
                "right": pg.Vector2(1, 0)
            }
            self.dash_direction = directions[self.facing]

        self.dash_time = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_length
        return True

    #

    def keybinds(self, dt, dungeon_map):

        keys = pg.key.get_pressed()
        dx = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(
            keys[pg.K_a] or keys[pg.K_LEFT]
        )
        dy = int(keys[pg.K_s] or keys[pg.K_DOWN]) - int(
            keys[pg.K_w] or keys[pg.K_UP]
        )

        self.moving = bool(dx or dy)

        if self.moving:
            direction = pg.Vector2(dx, dy).normalize()

            if abs(dx) >= abs(dy):
                self.facing = "right" if dx > 0 else "left"
            else:
                self.facing = "down" if dy > 0 else "up"

        if self.dashing:
            move_x = self.dash_direction.x * self.dash_speed * dt
            move_y = self.dash_direction.y * self.dash_speed * dt
            self._move(move_x, move_y, dungeon_map)
            self.dash_time = max(0, self.dash_time - dt)
            self.moving = True

        elif self.moving:
            direction = pg.Vector2(dx, dy).normalize()
            move_x = direction.x * self.speed * dt
            move_y = direction.y * self.speed * dt
            self._move(move_x, move_y, dungeon_map)

    #

    def _move(self, move_x, move_y, dungeon_map):

        if dungeon_map.can_move_circle(
            self.x + move_x,
            self.y,
            self.size
        ):
            self.x += move_x
        elif self.dashing:
            self.dash_time = 0

        if dungeon_map.can_move_circle(
            self.x,
            self.y + move_y,
            self.size
        ):
            self.y += move_y
        elif move_y and self.dashing:
            self.dash_time = 0

    #

    def render(self, camera):

        if self.blocking:
            frames = self.white_shield_frames
            elapsed = self.block_duration - self.block_time
            frame = frames[min(len(frames) - 1, int(elapsed / 0.09))]

        elif self.attack_animation_time > 0:
            frames = self.animations["Attack"]
            frame = frames[
                min(
                    len(frames) - 1,
                    int((0.3 - self.attack_animation_time) / 0.05)
                )
            ]

        elif self.moving:
            frames = self.animations["Run"]
            frame = frames[int(self.animation_time * 12) % len(frames)]

        else:
            frames = self.animations["Idle"]
            frame = frames[int(self.animation_time * 5) % len(frames)]

        if self.facing == "left":
            frame = pg.transform.flip(frame, True, False)

        screen_x, screen_y = camera.apply(self.x, self.y)
        self.screen.blit(
            frame,
            frame.get_rect(midbottom=(screen_x, screen_y + 28))
        )

        if self.blocking:
            pg.draw.circle(
                self.screen,
                (205, 230, 255),
                (screen_x, screen_y),
                48,
                3
            )

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

        if self.blocking:
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
        self.attack_animation_time = max(
            0,
            self.attack_animation_time - dt
        )
        self.block_time = max(0, self.block_time - dt)
        self.block_cooldown = max(0, self.block_cooldown - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)


# ============================================================

# Camera

class Camera:

    def __init__(self, screen, world_width, world_height):

        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pg.Vector2(0, 0)
        self.borders = {
            "left": 400,
            "right": 400,
            "top": 200,
            "bottom": 200
        }

    ###

    def update(self, player):

        screen_x = player.x - self.offset.x
        screen_y = player.y - self.offset.y

        if screen_x < self.borders["left"]:
            self.offset.x = player.x - self.borders["left"]
        elif screen_x > self.screen_width - self.borders["right"]:
            self.offset.x = player.x - (
                self.screen_width - self.borders["right"]
            )

        if screen_y < self.borders["top"]:
            self.offset.y = player.y - self.borders["top"]
        elif screen_y > self.screen_height - self.borders["bottom"]:
            self.offset.y = player.y - (
                self.screen_height - self.borders["bottom"]
            )

        max_offset_x = max(0, self.world_width - self.screen_width)
        max_offset_y = max(0, self.world_height - self.screen_height)
        self.offset.x = max(0, min(self.offset.x, max_offset_x))
        self.offset.y = max(0, min(self.offset.y, max_offset_y))

    #

    def apply(self, x, y):
        return round(x - self.offset.x), round(y - self.offset.y)


# ============================================================

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

    ###

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
        return (
            -50 <= self.x <= MAP_WIDTH + 50 and
            -50 <= self.y <= MAP_HEIGHT + 50
        )


# ============================================================

# Enemy

class Enemy:

    def __init__(self, screen, enemy_type, player, dungeon_map=None):

        self.screen = screen
        self.player = player
        self.dungeon_map = dungeon_map
        self.enemy_type = enemy_type
        self.x, self.y = self.random_spawn_position()
        self.set_stats()
        self.attack_cooldown = 0
        self.attack_delay = 1.0
        self.projectiles = []
        self.animation_time = random.random()
        self.attack_animation_time = 0
        self.facing_row = 0

        self.idle_frames = load_enemy_animation(
            self.slime_number,
            "Idle",
            self.sprite_scale
        )
        self.run_frames = load_enemy_animation(
            self.slime_number,
            "Run",
            self.sprite_scale
        )
        self.attack_frames = load_enemy_animation(
            self.slime_number,
            "Attack",
            self.sprite_scale
        )

    ###

    def set_stats(self):

        if self.enemy_type == "Common":
            self.max_hp = random.randint(25, 50)
            self.attack = random.randint(5, 10)
            self.speed = random.randint(360, 460)
            self.size = 24
            self.slime_number = 1
            self.sprite_scale = 128
            self.attack_range = 50
            self.attack_type = "melee"

        elif self.enemy_type == "Strong":
            self.max_hp = random.randint(50, 80)
            self.attack = random.randint(10, 15)
            self.speed = random.randint(280, 380)
            self.size = 32
            self.slime_number = 2
            self.sprite_scale = 144
            self.attack_range = 300
            self.attack_type = random.choice(["melee", "projectile"])

        elif self.enemy_type == "Elite":
            self.max_hp = random.randint(150, 200)
            self.attack = random.randint(20, 30)
            self.speed = random.randint(200, 280)
            self.size = 46
            self.slime_number = 3
            self.sprite_scale = 160
            self.attack_range = 70
            self.attack_type = random.choice(["melee", "projectile"])

        elif self.enemy_type == "Boss":
            self.max_hp = self.player.max_hp * 5
            self.attack = self.player.attack * 2
            self.speed = random.randint(140, 200)
            self.size = 64
            self.slime_number = 3
            self.sprite_scale = 224
            self.attack_range = 100
            self.attack_type = "projectile"

        self.current_hp = self.max_hp

    #

    def random_spawn_position(self):

        if self.dungeon_map is not None:
            return self.dungeon_map.random_enemy_spawn_position(
                self.player.x,
                self.player.y
            )

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
            if self.dungeon_map is None:
                self.x += move_x
                self.y += move_y
            else:
                if self.dungeon_map.can_move_circle(
                    self.x + move_x,
                    self.y,
                    self.size
                ):
                    self.x += move_x

                if self.dungeon_map.can_move_circle(
                    self.x,
                    self.y + move_y,
                    self.size
                ):
                    self.y += move_y

    #

    def check_attack(self):

        distance = math.hypot(
            self.player.x - self.x,
            self.player.y - self.y
        )

        if self.attack_cooldown > 0:
            return

        if self.attack_type == "melee":
            collision_distance = (
                self.attack_range + self.player.size + self.size
            )

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

        direction = pg.Vector2(
            self.player.x - self.x,
            self.player.y - self.y
        )

        if direction.length() == 0:
            return

        direction = direction.normalize()
        projectile = Projectile(
            self.screen,
            self.x,
            self.y,
            direction,
            self.attack
        )
        self.projectiles.append(projectile)

    #

    def update_projectiles(self, dt):

        for projectile in self.projectiles[:]:
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
            frame = frames[
                min(
                    len(frames) - 1,
                    int((0.3 - self.attack_animation_time) * 16)
                )
            ]
        else:
            distance = math.hypot(
                self.player.x - self.x,
                self.player.y - self.y
            )

            if distance > self.attack_range:
                frames = self.run_frames[self.facing_row]
                frame = frames[int(self.animation_time * 10) % len(frames)]
            else:
                frames = self.idle_frames[self.facing_row]
                frame = frames[int(self.animation_time * 5) % len(frames)]

        screen_x, screen_y = camera.apply(self.x, self.y)
        self.screen.blit(
            frame,
            frame.get_rect(midbottom=(screen_x, screen_y + 14))
        )

        bar_width = self.size * 2
        bar_x = screen_x - bar_width // 2
        bar_y = screen_y - self.size - 24
        pg.draw.rect(
            self.screen,
            (27, 31, 41),
            (bar_x, bar_y, bar_width, 7)
        )
        pg.draw.rect(
            self.screen,
            (145, 190, 220),
            (bar_x, bar_y, bar_width * self.current_hp / self.max_hp, 7)
        )

        for projectile in self.projectiles:
            projectile.render(camera)

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

    def __init__(self, screen, player, dungeon_map=None):

        self.screen = screen
        self.player = player
        self.dungeon_map = dungeon_map
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 2.0

    #

    def update(self, dt):

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_delay

        for enemy in self.enemies[:]:
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

        enemy = Enemy(
            self.screen,
            enemy_type,
            self.player,
            self.dungeon_map
        )
        self.enemies.append(enemy)

    #

    def render(self, camera):

        for enemy in self.enemies:
            enemy.render(camera)


# ============================================================

# Background
# The old cloud background is no longer used by Main.py.

class Background:

    def __init__(self, image_file, world_width, world_height):

        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            image_file
        )
        self.image = pg.image.load(image_path).convert()
        self.image = pg.transform.scale(
            self.image,
            (world_width, world_height)
        )
        self.rect = self.image.get_rect(topleft=(0, 0))

    #

    def render(self, screen, camera):

        screen.blit(
            self.image,
            camera.apply(self.rect.x, self.rect.y)
        )