import pygame as pg
import random
import math
import os


TILE_SIZE = 16
GRID_WIDTH = 150
GRID_HEIGHT = 110
MAP_WIDTH = GRID_WIDTH * TILE_SIZE
MAP_HEIGHT = GRID_HEIGHT * TILE_SIZE


class DungeonMap:
    """A tiled dungeon built from connected rooms and corridors."""

    REGIONS = {
        "Mossbound Halls": {"colour": (72, 91, 70), "tileset": 0},
        "Frostglass Wing": {"colour": (67, 88, 108), "tileset": 2},
        "Drowned Archive": {"colour": (62, 91, 94), "tileset": 3},
        "Ember Reliquary": {"colour": (105, 72, 57), "tileset": 1},
        "Eclipse Keep": {"colour": (81, 66, 99), "tileset": 4},
    }

    def __init__(self):
        # Room format:
        # (id, name, region, x, y, width, height)
        # The starting area is at the bottom, like in your reference.
        self.rooms = [
            ("start", "Whispering Shrine", "Mossbound Halls", 82, 94, 16, 12),
            ("south_hall", "Silent Gallery", "Frostglass Wing", 65, 80, 20, 13),
            ("south_vault", "Sunken Vault", "Drowned Archive", 103, 78, 21, 14),
            ("lower_hall", "Rootbound Passage", "Mossbound Halls", 77, 73, 20, 14),
            ("central", "Resonant Crossroads", "Mossbound Halls", 62, 50, 30, 18),
            ("west_hall", "Moss-Covered Cloister", "Mossbound Halls", 39, 50, 19, 14),
            ("west_shrine", "Forgotten Shrine", "Ember Reliquary", 10, 42, 20, 15),
            ("west_vault", "Buried Reliquary", "Ember Reliquary", 28, 72, 20, 14),
            ("north_hall", "The Pale Nave", "Frostglass Wing", 66, 18, 19, 18),
            ("northwest", "Moonlit Conservatory", "Frostglass Wing", 34, 18, 21, 15),
            ("northeast", "Hall of Glass", "Frostglass Wing", 101, 18, 23, 15),
            ("east_archive", "The Drowned Archive", "Drowned Archive", 109, 44, 24, 15),
            ("east_hall", "Ashen Gallery", "Ember Reliquary", 121, 68, 20, 15),
            ("boss", "The Eclipse Throne", "Eclipse Keep", 125, 91, 20, 14),
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
        self.wall_tiles = []
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

    def _load_tiles(self):
        image_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "Images",
            "Tiles"
        )

        for number in range(1, 6):
            road_path = os.path.join(image_folder, f"Road{number}.png")
            wall_path = os.path.join(
                image_folder,
                f"Road{number}_ground.png"
            )

            road_sheet = pg.image.load(road_path).convert_alpha()
            wall_sheet = pg.image.load(wall_path).convert_alpha()

            # A 16 x 16 cobblestone sample from each supplied tilesheet.
            sample_rect = pg.Rect(32, 32, TILE_SIZE, TILE_SIZE)
            self.floor_tiles.append(
                road_sheet.subsurface(sample_rect).copy()
            )
            self.wall_tiles.append(
                wall_sheet.subsurface(sample_rect).copy()
            )

    def _room_by_id(self, room_id):
        for room in self.rooms:
            if room[0] == room_id:
                return room
        return None

    @staticmethod
    def _room_centre(room):
        _, _, _, x, y, width, height = room
        return x + width // 2, y + height // 2

    def _carve_rect(self, x, y, width, height, region):
        for tile_y in range(y, y + height):
            for tile_x in range(x, x + width):
                if 0 <= tile_x < GRID_WIDTH and 0 <= tile_y < GRID_HEIGHT:
                    self.grid[tile_y][tile_x] = True
                    self.region_grid[tile_y][tile_x] = region

    def _carve_rooms(self):
        for room in self.rooms:
            _, _, region, x, y, width, height = room
            self._carve_rect(x, y, width, height, region)

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

    def _connect_rooms(self):
        # The links form one large dungeon with branches and alternate routes.
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
            ("east_hall", "boss", False),
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

    def _create_doors(self):
        # Doors start open. Press E nearby to open or close a door.
        door_tiles = [
            (90, 92),
            (81, 86),
            (105, 80),
            (87, 68),
            (110, 86),
            (58, 59),
            (32, 57),
            (48, 68),
            (61, 79),
            (77, 42),
            (57, 27),
            (95, 27),
            (112, 39),
            (121, 63),
            (131, 87),
        ]

        for tile_x, tile_y in door_tiles:
            self.doors.append({
                "x": tile_x,
                "y": tile_y,
                "open": True
            })

    def _build_surface(self):
        surface = pg.Surface((MAP_WIDTH, MAP_HEIGHT))
        surface.fill((14, 17, 24))

        # Draw the themed floor tiles.
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

        # Draw stone walls along the edge of every room and corridor.
        for tile_y in range(GRID_HEIGHT):
            for tile_x in range(GRID_WIDTH):
                if self.grid[tile_y][tile_x]:
                    continue

                touches_floor = False
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    check_x = tile_x + dx
                    check_y = tile_y + dy

                    if (0 <= check_x < GRID_WIDTH and
                            0 <= check_y < GRID_HEIGHT and
                            self.grid[check_y][check_x]):
                        touches_floor = True
                        break

                if touches_floor:
                    rect = pg.Rect(
                        tile_x * TILE_SIZE,
                        tile_y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    wall_index = (tile_x + tile_y) % len(self.wall_tiles)
                    surface.blit(self.wall_tiles[wall_index], rect.topleft)
                    pg.draw.line(
                        surface,
                        (22, 25, 32),
                        rect.bottomleft,
                        rect.bottomright,
                        2
                    )

        return surface.convert()

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

    def can_move_circle(self, x, y, radius):
        points = (
            (x - radius, y),
            (x + radius, y),
            (x, y - radius),
            (x, y + radius)
        )
        return all(self.is_walkable(px, py) for px, py in points)

    def random_enemy_spawn_position(self, player_x=None, player_y=None):
        for _ in range(100):
            position = random.choice(self.walkable_positions)

            if player_x is None or player_y is None:
                return position

            distance = math.hypot(
                position[0] - player_x,
                position[1] - player_y
            )

            if distance > 450:
                return position

        return random.choice(self.walkable_positions)

    def nearest_door(self, x, y):
        nearest = None
        nearest_distance = 48

        for door in self.doors:
            door_x = door["x"] * TILE_SIZE + TILE_SIZE // 2
            door_y = door["y"] * TILE_SIZE + TILE_SIZE // 2
            distance = math.hypot(door_x - x, door_y - y)

            if distance < nearest_distance:
                nearest = door
                nearest_distance = distance

        return nearest

    def interact(self, x, y):
        door = self.nearest_door(x, y)

        if door is None:
            return "There is no door nearby."

        door["open"] = not door["open"]
        return "Door opened." if door["open"] else "Door closed."

    def render(self, screen, camera):
        screen.blit(self.surface, camera.apply(0, 0))

        for door in self.doors:
            screen_x = door["x"] * TILE_SIZE - camera.offset.x
            screen_y = door["y"] * TILE_SIZE - camera.offset.y
            rect = pg.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

            if door["open"]:
                # The open doorway shows a stone threshold.
                pg.draw.rect(screen, (91, 76, 55), rect, 2)
            else:
                # Closed doors are drawn over the doorway.
                pg.draw.rect(screen, (91, 54, 35), rect)
                pg.draw.rect(screen, (185, 139, 77), rect, 2)
                pg.draw.line(
                    screen,
                    (44, 32, 27),
                    (rect.centerx, rect.top + 2),
                    (rect.centerx, rect.bottom - 2),
                    2
                )
                pg.draw.circle(
                    screen,
                    (235, 197, 106),
                    (rect.right - 4, rect.centery),
                    2
                )


class Player(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.x = MAP_WIDTH / 2
        self.y = MAP_HEIGHT / 2
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

    def keybinds(self, dt, dungeon_map=None):
        keys = pg.key.get_pressed()

        dx = int(keys[pg.K_d] or keys[pg.K_RIGHT]) - int(
            keys[pg.K_a] or keys[pg.K_LEFT]
        )
        dy = int(keys[pg.K_s] or keys[pg.K_DOWN]) - int(
            keys[pg.K_w] or keys[pg.K_UP]
        )

        if dx or dy:
            movement = pg.Vector2(dx, dy).normalize()
            move_x = movement.x * self.speed * dt
            move_y = movement.y * self.speed * dt

            if dungeon_map is None:
                self.x += move_x
                self.y += move_y
            else:
                if dungeon_map.can_move_circle(
                        self.x + move_x, self.y, self.size):
                    self.x += move_x

                if dungeon_map.can_move_circle(
                        self.x, self.y + move_y, self.size):
                    self.y += move_y

        self.x = max(self.size, min(self.x, MAP_WIDTH - self.size))
        self.y = max(self.size, min(self.y, MAP_HEIGHT - self.size))

    def render(self, camera):
        screen_position = camera.apply(self.x, self.y)
        pg.draw.circle(self.screen, self.colour, screen_position, self.size)

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    def pvisionRadius(self):
        return self.visionRadius

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

    def attack_enemies(self, enemies):
        if self.attack_cooldown > 0:
            return

        for enemy in enemies:
            distance = math.hypot(enemy.x - self.x, enemy.y - self.y)

            if distance <= self.attack_range + enemy.size:
                enemy.take_damage(self.attack)
                self.attack_cooldown = self.attack_delay
                break

    def update(self, dt):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt


class Camera:
    def __init__(self, screen, world_width, world_height):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pg.Vector2(0, 0)
        self.borders = {
            "left": 200,
            "right": 200,
            "top": 100,
            "bottom": 100
        }

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

    def apply(self, x, y):
        return round(x - self.offset.x), round(y - self.offset.y)


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

    def update(self, dt):
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt

    def render(self, camera):
        screen_position = camera.apply(self.x, self.y)
        pg.draw.circle(
            self.screen,
            self.colour,
            screen_position,
            self.size
        )

    def collides_with_player(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance <= player.size + self.size

    def is_on_screen(self):
        return (
            -50 <= self.x <= MAP_WIDTH + 50 and
            -50 <= self.y <= MAP_HEIGHT + 50
        )


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

    def set_stats(self):
        if self.enemy_type == "Common":
            self.max_hp = random.randint(25, 50)
            self.current_hp = self.max_hp
            self.attack = random.randint(5, 10)
            self.speed = random.randint(180, 230)
            self.size = 12
            self.colour = (150, 150, 150)
            self.attack_range = 25
            self.attack_type = "melee"

        elif self.enemy_type == "Strong":
            self.max_hp = random.randint(50, 80)
            self.current_hp = self.max_hp
            self.attack = random.randint(10, 15)
            self.speed = random.randint(140, 190)
            self.size = 16
            self.colour = (220, 180, 60)
            self.attack_range = 150
            self.attack_type = random.choice(["melee", "projectile"])

        elif self.enemy_type == "Elite":
            self.max_hp = random.randint(150, 200)
            self.current_hp = self.max_hp
            self.attack = random.randint(20, 30)
            self.speed = random.randint(100, 140)
            self.size = 23
            self.colour = (180, 60, 220)
            self.attack_range = 35
            self.attack_type = random.choice(["melee", "projectile"])

        elif self.enemy_type == "Boss":
            self.max_hp = self.player.max_hp * 5
            self.current_hp = self.max_hp
            self.attack = self.player.attack * 2
            self.speed = random.randint(70, 100)
            self.size = 40
            self.colour = (180, 30, 30)
            self.attack_range = 50
            self.attack_type = random.choice(["melee", "projectile"])

    def random_spawn_position(self):
        if self.dungeon_map is not None:
            return self.dungeon_map.random_enemy_spawn_position(
                self.player.x,
                self.player.y
            )

        side = random.randint(1, 4)

        if side == 1:
            return random.randint(0, MAP_WIDTH), -50
        elif side == 2:
            return random.randint(0, MAP_WIDTH), MAP_HEIGHT + 50
        elif side == 3:
            return -50, random.randint(0, MAP_HEIGHT)
        else:
            return MAP_WIDTH + 50, random.randint(0, MAP_HEIGHT)

    def update(self, dt):
        self.attack_cooldown -= dt
        self.move_towards_player(dt)

        if self.attack_type == "projectile":
            self.update_projectiles(dt)

        self.check_attack()

    def move_towards_player(self, dt):
        direction = pg.Vector2(
            self.player.x - self.x,
            self.player.y - self.y
        )

        if direction.length() == 0:
            return

        direction = direction.normalize()
        move_x = direction.x * self.speed * dt
        move_y = direction.y * self.speed * dt

        if self.dungeon_map is None:
            self.x += move_x
            self.y += move_y
        else:
            if self.dungeon_map.can_move_circle(
                    self.x + move_x, self.y, self.size):
                self.x += move_x

            if self.dungeon_map.can_move_circle(
                    self.x, self.y + move_y, self.size):
                self.y += move_y

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

        elif self.attack_type == "projectile":
            if distance <= self.attack_range:
                self.shoot()
                self.attack_cooldown = self.attack_delay

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

    def update_projectiles(self, dt):
        for projectile in self.projectiles[:]:
            projectile.update(dt)

            if projectile.collides_with_player(self.player):
                self.player.take_damage(projectile.damage)
                self.projectiles.remove(projectile)

            elif not projectile.is_on_screen():
                self.projectiles.remove(projectile)

    def render(self, camera):
        screen_position = camera.apply(self.x, self.y)
        pg.draw.circle(
            self.screen,
            self.colour,
            screen_position,
            self.size
        )

        for projectile in self.projectiles:
            projectile.render(camera)

    def take_damage(self, damage):
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0
            return True

        return False


class EnemyManager:
    def __init__(self, screen, player, dungeon_map=None):
        self.screen = screen
        self.player = player
        self.dungeon_map = dungeon_map
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_delay = 2.0

    def update(self, dt):
        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_delay

        for enemy in self.enemies[:]:
            enemy.update(dt)

            if enemy.current_hp <= 0:
                self.enemies.remove(enemy)

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

    def render(self, camera):
        for enemy in self.enemies:
            enemy.render(camera)


class Background:
    """Kept for compatibility; Main.py now draws DungeonMap instead."""

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

    def render(self, screen, camera):
        screen.blit(
            self.image,
            camera.apply(self.rect.x, self.rect.y)
        )