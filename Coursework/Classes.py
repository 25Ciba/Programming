import pygame as pg
import random
import math
from BossArena import ArenaArt
from MobMotion import facing_row, mob_frames
from BossMotion import load_boss_steps, original_keeper_steps, boss_pose_offset, boss_pixel_frame, boss_idle_frames
from Violin import ViolinArt, VIOLIN_HABITATS
from Harp import HarpArt, HARP_HABITATS
from Cello import CelloArt, CELLO_HABITATS
from Flute import FluteArt, FLUTE_HABITATS
from Guitar import GuitarArt, GUITAR_HABITATS
from Frost import FrostArt, FROST_HABITATS
from RogueArt import RogueArt, DIRECTIONS
from pathlib import Path
from Settlements import Settlements, WORLD_WIDTH, WORLD_HEIGHT
from Story import ALTAR, ASCENT, Story
from Menus import held
from Items import ITEMS, START_SHIELD, START_WEAPON
from Ruins import RuinsArt, RuinsGate, GATE_X, GATE_Y, HABITATS, creature_frames
from DungeonLayout import REGIONS, ROOMS, CORRIDORS, GATES, BOSS_ROOMS, START_X, START_Y

###

IMAGE_FOLDER = Path(__file__).resolve().parent / "Images"

MAP_WIDTH = WORLD_WIDTH
MAP_HEIGHT = WORLD_HEIGHT

###

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
        self.frost_art = FrostArt(IMAGE_FOLDER, self.ruins_art)
        self.guitar_art = GuitarArt(IMAGE_FOLDER, self.ruins_art)
        self.flute_art = FluteArt(IMAGE_FOLDER, self.ruins_art)
        self.cello_art = CelloArt(IMAGE_FOLDER, self.ruins_art)
        self.harp_art = HarpArt(IMAGE_FOLDER, self.ruins_art)
        self.violin_art = ViolinArt(IMAGE_FOLDER, self.ruins_art)
        self.rooms = []
        self.room_floors = []
        self.corridors = []
        for name, region, x, y, width, height in ROOMS:
            rect = pg.Rect(x, y, width, height)
            self.rooms.append((name, region, rect))
            shape = (len(self.rooms) + region) % 4
            if name in ("Overture Arena", "Resonance Arena", "Flute Hall", "Cello Amphitheatre", "Harp Chamber", "Performance Hall"):
                shape = 1
            for floor in self.room_shape(rect, shape):
                self.room_floors.append((name, region, floor))
        for region, x, y, width, height in CORRIDORS:
            self.corridors.append((region, pg.Rect(x, y, width, height)))
        self.arena_art = ArenaArt(self.rooms, IMAGE_FOLDER)
        self.ruins_art.place_masonry(self.room_floors, self.corridors)
        self.frost_art.populate(self.room_floors, self.corridors)
        self.guitar_art.populate()
        self.ruins_edges = []
        self.frost_edges = []
        self.guitar_edges = []
        self.flute_edges = []
        self.cello_edges = []
        self.harp_edges = []
        self.violin_edges = []
        for name, region, rect in self.room_floors:
            if region == 0:
                self.add_ruins_edges(rect, self.ruins_edges)
            elif region == 1:
                self.add_ruins_edges(rect, self.frost_edges)
            elif region == 2:
                self.add_ruins_edges(rect, self.guitar_edges)
            elif region == 3:
                self.add_ruins_edges(rect, self.flute_edges)
            elif region == 4:
                self.add_ruins_edges(rect, self.cello_edges)
            elif region == 5:
                self.add_ruins_edges(rect, self.harp_edges)
            elif region == 6:
                self.add_ruins_edges(rect, self.violin_edges)
        for region, rect in self.corridors:
            if region == 0:
                self.add_ruins_edges(rect, self.ruins_edges)
            elif region == 1:
                self.add_ruins_edges(rect, self.frost_edges)
            elif region == 2:
                self.add_ruins_edges(rect, self.guitar_edges)
            elif region == 3:
                self.add_ruins_edges(rect, self.flute_edges)
            elif region == 4:
                self.add_ruins_edges(rect, self.cello_edges)
            elif region == 5:
                self.add_ruins_edges(rect, self.harp_edges)
            elif region == 6:
                self.add_ruins_edges(rect, self.violin_edges)

        self.settlements = Settlements(self)
        self.story = Story(self)

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

        if self.gate.blocks(x, y, radius) or self.ruins_art.blocks(x, y, radius) or self.frost_art.blocks(x, y, radius) or self.guitar_art.blocks(x, y, radius) or self.flute_art.blocks(x, y, radius) or self.cello_art.blocks(x, y, radius) or self.harp_art.blocks(x, y, radius) or self.violin_art.blocks(x, y, radius) or self.arena_art.blocks(x, y, radius):
            return False
        if hasattr(self, "settlements") and self.settlements.blocks(x, y, radius):
            return False
        points = [(x - radius, y), (x + radius, y), (x, y - radius), (x, y + radius)]
        for point_x, point_y in points:
            if not self.is_walkable(point_x, point_y):
                return False
        return True

    #

    def clear_enemy_path(self, x, y, target_x, target_y, radius):

        distance = math.hypot(target_x - x, target_y - y)
        steps = max(1, math.ceil(distance / 16))
        for step in range(1, steps + 1):
            check_x = x + (target_x - x) * step / steps
            check_y = y + (target_y - y) * step / steps
            if not self.can_move_circle(check_x, check_y, radius):
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
                    self.ruins_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 1:
                    self.frost_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 2:
                    self.guitar_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 3:
                    self.flute_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 4:
                    self.cello_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 5:
                    self.harp_art.draw_floor(screen, visible_rect, view, origin, '')
                elif region == 6:
                    self.violin_art.draw_floor(screen, visible_rect, view, origin, '')
        for name, region, rect in self.room_floors:
            visible_rect = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if view.colliderect(visible_rect):
                pg.draw.rect(screen, REGIONS[region][1], visible_rect)
                if region == 0:
                    self.ruins_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 1:
                    self.frost_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 2:
                    self.guitar_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 3:
                    self.flute_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 4:
                    self.cello_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 5:
                    self.harp_art.draw_floor(screen, visible_rect, view, origin, name)
                elif region == 6:
                    self.violin_art.draw_floor(screen, visible_rect, view, origin, name)
        self.ruins_art.draw_walls(screen, camera, self.ruins_edges)
        self.frost_art.draw_walls(screen, camera, self.frost_edges)
        self.guitar_art.draw_walls(screen, camera, self.guitar_edges)
        self.flute_art.draw_walls(screen, camera, self.flute_edges)
        self.cello_art.draw_walls(screen, camera, self.cello_edges)
        self.harp_art.draw_walls(screen, camera, self.harp_edges)
        self.violin_art.draw_walls(screen, camera, self.violin_edges)
        for first_region, second_region, x, y in GATES:
            if (x, y) == (GATE_X, GATE_Y):
                continue
            gate_x, gate_y = camera.apply(x, y)
            pg.draw.rect(screen, (197, 168, 105), (gate_x - 6, gate_y - 6, 12, 12))
        self.ruins_art.render(screen, camera)
        self.ruins_art.render_lighting(screen, camera)
        self.frost_art.render(screen, camera)
        self.guitar_art.render(screen, camera)
        self.flute_art.render(screen, camera)
        self.cello_art.render(screen, camera)
        self.harp_art.render_arena(screen, camera)
        self.harp_art.render(screen, camera)
        self.violin_art.render(screen, camera)
        self.gate.render(screen, camera)
        self.arena_art.render(screen, camera)
        self.settlements.render(screen, camera)
        self.story.render(screen, camera)

    #

    def add_ruins_edges(self, rect, edges):

        # Group exposed floor boundaries into continuous wall runs.
        for side, boundary, outside in [("north", rect.top, rect.top - 1), ("south", rect.bottom, rect.bottom)]:
            start = None
            for x in range(rect.left, rect.right + 1):
                exposed = x < rect.right and not self.is_walkable(x, outside)
                if exposed and start is None:
                    start = x
                if not exposed and start is not None:
                    edges.append((start, boundary, x - start, side))
                    start = None
        for side, boundary, outside in [("west", rect.left, rect.left - 1), ("east", rect.right, rect.right)]:
            start = None
            for y in range(rect.top, rect.bottom + 1):
                exposed = y < rect.bottom and not self.is_walkable(outside, y)
                if exposed and start is None:
                    start = y
                if not exposed and start is not None:
                    edges.append((boundary, start, y - start, side))
                    start = None

    #

#================================================

# Player

class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.clan = "Rogue"
        self.progress = None
        self.x = START_X
        self.y = START_Y
        self.speed = 520
        self.size = 30
        self.visionRadius = 300

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.max_mana = 100
        self.current_mana = self.max_mana

        self.defence = 50

        self.attack = 20
        self.attack_range = 100
        self.attack_cooldown = 0
        self.attack_delay = 0.42

        self.max_lives = 7
        self.current_lives = self.max_lives
        self.facing = 0
        self.attack_facing = 0
        self.ranged_aim = pg.Vector2(0, 1)
        self.walk_distance = 0
        self.stride = 0
        self.idle_time = 0
        self.moving = False
        self.animation_time = 0
        self.attack_animation_time = 0
        self.enemies = []
        self.attack_targets = []
        self.attack_stage = 0
        self.attack_queued = False
        self.swing_duration = self.attack_delay
        self.attack_map = None

        self.block_duration = 0.5
        self.block_cooldown_length = 1.5
        self.block_time = 0
        self.block_cooldown = 0

        self.dash_duration = 0.5
        self.dash_cooldown_length = 2.0
        self.dash_speed = 840
        self.dash_time = 0
        self.dash_cooldown = 0
        self.dash_direction = pg.Vector2(0, 0)

        self.powers = None
        self.main_hand = START_WEAPON
        self.off_hand = START_SHIELD
        self.armour = None
        self.charm = None
        self.guard_multiplier = 0.2
        self.shots = []
        self.art = RogueArt()
        self.dash_trail = []
        self.dash_braking = False

    #

    def direction_keys(self):

        keys = pg.key.get_pressed()
        dx = int(held(keys,"Move right",pg.K_RIGHT)) - int(held(keys,"Move left",pg.K_LEFT))
        dy = int(held(keys,"Move down",pg.K_DOWN)) - int(held(keys,"Move up",pg.K_UP))
        return dx, dy

    #

    def begin_block(self):

        if self.block_cooldown > 0 or self.dash_time > 0 or self.attack_animation_time > 0:
            return False
        self.block_time = self.block_duration
        self.block_cooldown = self.block_cooldown_length
        return True

    #

    def begin_dash(self):

        if self.powers and (self.powers.familiar is not None or self.powers.active("Stab")):
            return False

        if self.dash_cooldown > 0 or self.dash_time > 0 or self.block_time > 0:
            return False
        direction = self.direction_keys()
        if direction != (0, 0):
            self.facing = DIRECTIONS.index(direction)
        self.dash_direction = pg.Vector2(DIRECTIONS[self.facing]).normalize()
        self.dash_time = self.dash_duration
        self.dash_cooldown = self.dash_cooldown_length
        self.attack_animation_time = 0
        self.attack_targets = []
        self.attack_stage = 0
        self.attack_queued = False
        self.dash_trail = []
        self.dash_braking = False
        return True

    #

    def keybinds(self, dt, game_map):

        if self.powers and (self.powers.familiar is not None or self.powers.active("Stab")):
            self.moving = False
            self.settle_stride(dt)
            return

        if self.dash_time > 0:
            self.move_dash(dt, game_map)
            self.stride = 0
            self.idle_time = 0
            return
        direction = self.direction_keys()
        self.moving = False
        if direction == (0, 0):
            self.settle_stride(dt)
            return
        if self.attack_animation_time <= 0 and self.block_time <= 0:
            self.facing = DIRECTIONS.index(direction)
        speed = self.speed * (self.powers.speed_factor() if self.powers else 1)
        if self.attack_animation_time > 0:
            speed *= 0.52
        move = pg.Vector2(direction).normalize() * speed * dt
        old_x, old_y = self.x, self.y
        self._move(move.x, move.y, game_map)
        distance = math.hypot(self.x - old_x, self.y - old_y)
        self.walk_distance += distance
        self.moving = distance > 0
        if self.moving:
            self.stride = min(1, self.stride + dt / 0.12)
            self.idle_time = 0
        else:
            self.settle_stride(dt)

    def settle_stride(self, dt):

        self.stride = max(0, self.stride - dt / 0.16)
        if self.stride == 0:
            self.walk_distance = 0
            self.idle_time += dt

    def movement_frame(self):

        return self.art.movement_frame(self.facing, self.walk_distance, self.stride, self.idle_time)


    #

    def move_dash(self, dt, game_map):

        self.moving = False
        elapsed = self.dash_duration - self.dash_time
        self.dash_time = max(0, self.dash_time - dt)
        if elapsed < 0.08 or self.dash_braking:
            return
        speed = self.dash_speed
        if self.dash_time < 0.10:
            speed *= self.dash_time / 0.10
        move = self.dash_direction * speed * dt
        steps = max(1, math.ceil(move.length() / 10))
        self.dash_trail.append((self.x, self.y))
        self.dash_trail = self.dash_trail[-6:]
        for step in range(steps):
            x = self.x + move.x / steps
            y = self.y + move.y / steps
            if not self.can_move_to(x, y, game_map):
                self.dash_braking = True
                self.dash_time = min(self.dash_time, 0.10)
                break
            self.x, self.y = x, y

    #

    def _move(self, move_x, move_y, game_map):

        if self.can_move_to(self.x + move_x, self.y, game_map):
            self.x += move_x
        if self.can_move_to(self.x, self.y + move_y, game_map):
            self.y += move_y

    #

    def can_move_to(self, x, y, game_map):

        if not game_map.can_move_circle(x, y, self.size):
            return False
        if hasattr(game_map, "arena_art") and not game_map.arena_art.allows_crossing(self, x, y):
            return False
        old_overlap = 0
        new_overlap = 0
        for enemy in self.enemies:
            if enemy.current_hp <= 0:
                continue
            after = enemy.body_overlap(x, y, self.size)
            if after <= 0:
                continue
            before = enemy.body_overlap(self.x, self.y, self.size)
            if before <= 0:
                return False
            old_overlap += before
            new_overlap += after
        # Let the Rogue back out if an enemy is already overlapping.
        return new_overlap == 0 or new_overlap < old_overlap

    # An existing overlap must get smaller. New overlaps still block movement.
        return new_overlap == 0 or new_overlap < old_overlap

    #

    def render(self, camera):

        _, _, crouch, glide = self.art.poses[self.facing]
        x, y = camera.apply(self.x, self.y)
        frame = self.movement_frame()
        for position, direction, remaining, damage, colour, targets, game_map in self.shots:
            point = pg.Vector2(camera.apply(position.x, position.y))
            pg.draw.line(self.screen, colour, point - direction * 12, point, 3)
        if self.dash_time > 0:
            if self.dash_time > self.dash_duration - 0.08 or self.dash_time < 0.10:
                frame = crouch
            else:
                frame = glide
            side = pg.Vector2(-self.dash_direction.y, self.dash_direction.x)
            for i, (world_x, world_y) in enumerate(self.dash_trail):
                px, py = camera.apply(world_x, world_y)
                start = pg.Vector2(px, py) + side * ((i % 3) - 1) * 9
                end = start - self.dash_direction * (14 + i * 4)
                pg.draw.line(self.screen, (73 + i * 12, 74 + i * 10, 110 + i * 13), start, end, 2 + i // 3)
        elif self.block_time > 0 or (self.powers and self.powers.active("Sneak")):
            frame = crouch
        elif self.attack_animation_time > 0:
            progress = 1 - self.attack_animation_time / self.swing_duration
            frame_number = min(23, int(progress * 24))
            frames = self.art.return_cuts if self.attack_stage == 2 else self.art.attacks
            frame = frames[self.attack_facing][frame_number]
            frame = self.art.held_gear(frame, self.attack_facing, None, self.off_hand)
            self.screen.blit(frame, frame.get_rect(center=(x, y)))
            return
        frame = self.art.held_gear(frame, self.facing, self.main_hand, self.off_hand, self.block_time > 0)
        self.screen.blit(frame, frame.get_rect(midbottom=(x, y + 24)))
        if self.block_time > 0:
            direction = pg.Vector2(DIRECTIONS[self.facing]).normalize()
            self.art.guard(self.screen, x, y, direction, 1 - self.block_time / self.block_duration)

    #

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    #

    def pvisionRadius(self):
        return self.visionRadius

    #

    def take_damage(self, incoming_damage):

        if self.powers and self.powers.active("Shield"):
            return 0
        damage_multiplier = self.max_hp / (self.max_hp + self.defence)
        if self.powers and self.powers.familiar is not None:
            damage_multiplier *= .6
        if self.powers and self.powers.active("Buff"):
            damage_multiplier *= .75
        actual_damage = max(1, round(incoming_damage * damage_multiplier))
        if self.block_time > 0:
            actual_damage = max(1, round(actual_damage * self.guard_multiplier))
        if self.progress is not None:
            self.progress["damage_taken"] += min(self.current_hp,actual_damage)
        self.current_hp = max(0, self.current_hp - actual_damage)
        if self.current_hp == 0:
            self.current_lives = max(0, self.current_lives - 1)
            if self.current_lives > 0:
                self.current_hp = self.max_hp
        return actual_damage

    #

    def uses_ranged_weapon(self):

        return ITEMS[self.main_hand][1] in ("Bow", "Focus")

    def aim_direction(self, target):

        direction = pg.Vector2(target) - (self.x, self.y)
        if not direction.length_squared():
            direction = pg.Vector2(DIRECTIONS[self.facing])
        return direction.normalize()

    def attack_enemies(self, enemies, game_map=None, target=None):

        if self.dash_time > 0 or self.block_time > 0 or (self.powers and self.powers.familiar is not None and not self.uses_ranged_weapon()):
            return
        if self.attack_stage == 1 and not self.uses_ranged_weapon():
            self.attack_queued = True
            return
        if self.attack_stage or self.attack_cooldown > 0:
            return
        self.attack_facing = self.facing
        if self.uses_ranged_weapon():
            self.ranged_aim = self.aim_direction(target) if target is not None else pg.Vector2(DIRECTIONS[self.facing]).normalize()
            self.attack_facing = max(range(len(DIRECTIONS)), key=lambda index: self.ranged_aim.dot(pg.Vector2(DIRECTIONS[index]).normalize()))
            self.facing = self.attack_facing
        self.attack_targets = enemies
        self.attack_map = game_map
        self.start_swing(1)

    def start_swing(self, stage):

        self.attack_stage = stage
        self.swing_duration = self.attack_delay if stage == 1 else self.attack_delay / 2
        self.attack_animation_time = self.swing_duration
        self.attack_cooldown = self.swing_duration

    def land_attack(self):

        direction = pg.Vector2(DIRECTIONS[self.attack_facing]).normalize()
        if self.powers and self.powers.active("True Strike"):
            target = self.powers.marked
            self.powers.effects.pop("True Strike")
            if target and target.current_hp > 0 and math.hypot(target.x - self.x, target.y - self.y) <= 650:
                self.powers.hit(target, self.attack)
                self.powers.cast_trails.append((pg.Vector2(self.x,self.y),pg.Vector2(target.x,target.y),(228,188,131),.27,.27))
                return
        if self.uses_ranged_weapon():
            direction = self.ranged_aim
            position = pg.Vector2(self.x, self.y)
            self.shots.append((position, direction, self.attack_range, self.attack + (ITEMS[self.charm][3] if self.charm else 0), ITEMS[self.main_hand][2], self.attack_targets, self.attack_map))
            return
        start = pg.Vector2(self.x,self.y)
        for enemy in self.melee_targets(self.attack_targets, start, direction, self.attack_range, self.attack_map):
            damage = self.attack + (ITEMS[self.charm][3] if self.charm else 0)
            if self.attack_stage != 1:
                damage = max(1, damage // 2)
            if self.powers:
                self.powers.hit(enemy, damage)
            else:
                enemy.take_damage(damage)

    def melee_targets(self, enemies, start, direction, reach, game_map):

        for enemy in enemies:
            if getattr(enemy, 'current_hp', 1) <= 0:
                continue
            offset = pg.Vector2(enemy.x, enemy.y) - start
            if offset.length() > reach + enemy.size:
                continue
            if offset.length_squared() and direction.dot(offset.normalize()) < 0.35:
                continue
            if game_map is None or game_map.clear_enemy_path(start.x, start.y, enemy.x, enemy.y, 4):
                yield enemy

    #

    def update_shots(self, dt):

        active = []
        for position, direction, remaining, damage, colour, targets, game_map in self.shots:
            distance = min(remaining, (790 if self.clan == "Marksman" else 620) * dt)
            end = position + direction * distance
            nearest = None
            nearest_distance = distance
            for enemy in targets:
                if enemy.current_hp <= 0:
                    continue
                offset = pg.Vector2(enemy.x, enemy.y) - position
                along = offset.dot(direction)
                radius = enemy.body_radius() + 5
                side = abs(offset.cross(direction))
                if side > radius:
                    continue
                half = math.sqrt(radius * radius - side * side)
                contact = max(0, along - half)
                if along + half >= 0 and contact <= nearest_distance:
                    nearest, nearest_distance = enemy, contact
            impact = position + direction * nearest_distance
            if game_map and not game_map.clear_enemy_path(position.x, position.y, impact.x, impact.y, 3):
                continue
            if nearest:
                if self.powers:
                    self.powers.hit(nearest, damage)
                else:
                    nearest.take_damage(damage)
            elif remaining > distance:
                active.append((end, direction, remaining - distance, damage, colour, targets, game_map))
        self.shots = active

    def update(self, dt):

        self.update_shots(dt)
        if self.powers:
            self.powers.update(dt)
        self.animation_time += dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        if self.attack_stage:
            previous_time = self.attack_animation_time
            self.attack_animation_time = max(0, previous_time - dt)
            contact = self.swing_duration * 0.58
            if previous_time > contact >= self.attack_animation_time:
                self.land_attack()
            if self.attack_animation_time == 0:
                if self.attack_stage == 1 and self.attack_queued:
                    self.start_swing(2)
                elif self.attack_stage == 2:
                    self.start_swing(3)
                else:
                    self.attack_stage = 0
                    self.attack_queued = False
                    self.attack_targets = []
                if self.attack_stage:
                    self.attack_animation_time -= dt - previous_time
                    self.attack_cooldown = self.attack_animation_time
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
        self.left_border = 470
        self.right_border = 470
        self.top_border = 320
        self.bottom_border = 285

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
        if ASCENT.collidepoint(player.x, player.y):
            self.offset.x = ALTAR[0] - self.screen_width // 2
        max_offset_x = max(0, self.world_width - self.screen_width)
        max_offset_y = max(0, self.world_height - self.screen_height)
        self.offset.x = max(0, min(self.offset.x, max_offset_x))
        self.offset.y = max(-self.top_border, min(self.offset.y, max_offset_y + self.bottom_border))

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

PIXEL_BOSSES = ("Piano", "Guitar", "Flute", "Cello", "Harp", "Violin")


class Enemy:
    def __init__(self, screen, enemy_type, player, game_map=None, name=None, home=None):

        self.screen = screen
        self.player = player
        self.game_map = game_map
        self.enemy_type = enemy_type
        self.name = name or enemy_type
        self.home = home
        if home is None:
            self.x, self.y = self.random_spawn_position()
        else:
            self.x, self.y = home
        self.set_stats()
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            self.size = 23
        if self.name in ("Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            self.attack_type = "projectile"
            self.attack_range = 155 if self.name == "Rosin Spirit" else 175
            if self.name in ("Ripple Wisp", "Bowshade"):
                self.attack_range = 195
        self.name_image = pg.font.Font(None, 20).render(self.name, True, (235, 228, 209))
        self.moving = False
        self.strikes = 0
        self.windup = 0
        self.windup_length = 1
        self.lunge_time = 0
        self.lunge_hit = False
        self.death_time = 0
        self.reward_claimed = False
        self.move_name = ''
        self.aim = pg.Vector2(0, 1)
        self.attack_cooldown = 0
        self.attack_delay = 2.0
        self.projectiles = []
        self.animation_time = random.random()
        self.attack_animation_time = 0
        self.facing_row = 0
        self.windup_frames = []
        self.death_frames = []
        self.directional_mob = self.home is not None and self.enemy_type in ("Common", "Strong")
        if self.directional_mob:
            self.idle_frames, self.run_frames, self.attack_frames, self.windup_frames, self.death_frames = mob_frames(IMAGE_FOLDER, self.name)
        self.keeper_poses = []
        self.boss_steps = []
        self.walked = 0
        if self.enemy_type == "Overture":
            for index in range(8):
                pose = pg.image.load(IMAGE_FOLDER / "BlueGrey" / "KeeperPoses" / f"{index}.png").convert_alpha()
                pose = pg.transform.scale(pose, (round(pose.get_width() * 2.5), round(pose.get_height() * 2.5)))
                self.keeper_poses.append(pose)
            self.boss_steps = original_keeper_steps(self.keeper_poses[0])
        if self.enemy_type in PIXEL_BOSSES:
            region_folder = "FrostPiano"
            if self.enemy_type == "Guitar":
                region_folder = "GuitarCaverns"
            elif self.enemy_type == "Flute":
                region_folder = "FluteCloister"
            elif self.enemy_type == "Cello":
                region_folder = "CelloCatacombs"
            elif self.enemy_type == "Harp":
                region_folder = "HarpReservoir"
            elif self.enemy_type == "Violin":
                region_folder = "ViolinHall"
            pose_scale = 0.90 if self.enemy_type == "Violin" else 1.23
            for index in range(8):
                pose = pg.image.load(IMAGE_FOLDER / region_folder / "BossPoses" / f"{index}.png").convert_alpha()
                pose = pg.transform.scale(pose, (round(pose.get_width() * pose_scale), round(pose.get_height() * pose_scale)))
                self.keeper_poses.append(pose)
            if self.enemy_type == "Guitar":
                self.boss_steps = load_boss_steps(IMAGE_FOLDER / "GuitarCaverns" / "BossPoses", self.keeper_poses[0])
            if self.enemy_type == "Cello":
                self.boss_steps = original_keeper_steps(self.keeper_poses[0])
            self.keeper_poses = [boss_pixel_frame(pose) for pose in self.keeper_poses]
            self.boss_steps = [boss_pixel_frame(pose) for pose in self.boss_steps]
            self.boss_idle = boss_idle_frames(self.keeper_poses[0], self.enemy_type)
            self.idle_frames = [[self.keeper_poses[0]]] * 4
            self.run_frames = self.idle_frames
            self.attack_frames = self.idle_frames
            return
        if self.windup_frames:
            return
        if self.home is not None:
            scale = 94
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                scale = 66
            if self.enemy_type == "Overture":
                scale = 138
            self.idle_frames = creature_frames(IMAGE_FOLDER, self.name, "Idle", scale)
            self.run_frames = creature_frames(IMAGE_FOLDER, self.name, "Run", scale)
            self.attack_frames = creature_frames(IMAGE_FOLDER, self.name, "Attack", scale)
        else:
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

        elif self.enemy_type == "Overture":
            self.max_hp = 600
            self.attack = 42
            self.speed = 175
            self.size = 42
            self.attack_range = 45
            self.attack_type = "melee"

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

        if self.current_hp <= 0:
            self.death_time += dt
            return
        self.animation_time += dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_animation_time = max(0, self.attack_animation_time - dt)
        self.moving = False
        if self.windup > 0:
            self.windup = max(0, self.windup - dt)
            if self.windup == 0:
                self.release_attack()
            return
        if self.lunge_time > 0:
            self.skitter_lunge(dt)
            return
        if self.projectiles:
            self.update_projectiles(dt)
        if self.enemy_type == "Overture":
            if not self.game_map.location_name(self.player.x, self.player.y).endswith("Overture Arena"):
                self.move_towards(self.home[0], self.home[1], dt, 3)
                return
        elif self.home is not None:
            player_distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
            home_distance = math.hypot(self.player.x - self.home[0], self.player.y - self.home[1])
            detection = 1050 if self.player.clan == "Familiar" else 410
            if self.player.powers and self.player.clan == "Assassin":
                detection = 165 if self.player.powers.active("Sneak") else 310
            if player_distance > detection or home_distance > 560:
                self.move_towards(self.home[0], self.home[1], dt, 3)
                return
        if self.attack_animation_time <= 0:
            stop_distance = self.attack_range
            if self.attack_type == "melee":
                stop_distance += self.player.size + self.size - 6
            self.move_towards(self.player.x, self.player.y, dt, stop_distance)
        self.check_attack()

    #

    def footprint(self):

        # Horizontal radius, vertical radius, and offset to the feet.
        if self.enemy_type == "Piano":
            return 41, 19, 9
        if self.enemy_type == "Overture":
            return 46, 22, 8
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            return 16, 12, 0
        return round(self.size * 0.84), round(self.size * 0.64), 4

    def body_radius(self):

        width, height, offset = self.footprint()
        return width

    def body_overlap(self, x, y, radius, center_x=None, center_y=None):

        width, height, offset = self.footprint()
        if center_x is None:
            center_x = self.x
            center_y = self.y
        dx = (x - center_x) / (width + radius)
        dy = (y - center_y - offset) / (height + radius)
        return 1 - math.hypot(dx, dy)

    def blocks_player(self, x, y, player_radius):

        return self.body_overlap(x, y, player_radius) > 0

    def can_step(self, x, y):

        room = "Overture Arena" if self.enemy_type == "Overture" else getattr(self, "arena_room", None)
        if room and not self.game_map.location_name(x, y).endswith(room):
            return False
        targets = (self.player, self.player.owner.player) if self.player.clan == "Familiar" else (self.player,)
        for target in targets:
            overlap = self.body_overlap(target.x,target.y,target.size,x,y)
            if overlap > 0 and overlap >= self.body_overlap(target.x,target.y,target.size):
                return False
        return self.game_map.can_move_circle(x, y, self.body_radius())

    #

    def move_towards(self, target_x, target_y, dt, stop_distance):

        dx = target_x - self.x
        dy = target_y - self.y
        direction = pg.Vector2(dx, dy)
        if direction.length() == 0:
            return
        if self.directional_mob:
            self.facing_row = facing_row(dx, dy)
        elif abs(dx) > abs(dy):
            self.facing_row = 2 if dx > 0 else 1
        else:
            self.facing_row = 0 if dy > 0 else 3
        distance = direction.length()
        direction = direction.normalize()
        move_x = direction.x * self.speed * dt
        move_y = direction.y * self.speed * dt
        if distance > stop_distance:
            old_x, old_y = self.x, self.y
            if self.game_map is None:
                self.x += move_x
                self.y += move_y
            else:
                if self.can_step(self.x + move_x, self.y):
                    self.x += move_x
                if self.can_step(self.x, self.y + move_y):
                    self.y += move_y
            distance_moved = math.hypot(self.x - old_x, self.y - old_y)
            self.moving = distance_moved > 0
            if self.moving and self.directional_mob:
                self.facing_row = facing_row(self.x - old_x, self.y - old_y)
            self.walked += distance_moved

    #
    
    def check_attack(self):

        distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
        if self.attack_cooldown > 0 or self.attack_animation_time > 0:
            return
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if self.enemy_type == "Overture":
            self.move_name = ["Resonance stomp", "Fork thrust", "Three-note volley"][self.strikes % 3]
            reach = [185, 280, 390][self.strikes % 3]
            self.windup_length = [0.72, 0.65, 0.85][self.strikes % 3]
        else:
            self.move_name = "Sonic dart" if self.attack_type == "projectile" else "Lunge"
            reach = self.attack_range + self.player.size + self.size
            self.windup_length = 0.32 if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat") else 0.42
            if self.name == "Chalk Skitter":
                reach += 29
            elif self.name == "Score Swarm":
                reach = 96
                self.windup_length = 0.58
            elif self.name in ("Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                self.windup_length = 0.48
            elif self.name in ("Silt Scorpion", "Mossback Snapper"):
                self.windup_length = 0.44
        if distance <= reach and self.can_reach_player():
            if offset.length_squared():
                self.aim = offset.normalize()
            if self.directional_mob:
                self.facing_row = facing_row(self.aim.x, self.aim.y)
            self.windup = self.windup_length

    def release_attack(self):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        distance = offset.length()
        self.attack_animation_time = 0.3
        self.attack_cooldown = self.attack_delay
        if self.name == "Chalk Skitter":
            self.lunge_time = 0.14
            self.lunge_hit = False
            return
        if self.name == "Score Swarm":
            if distance <= 96 and self.can_reach_player():
                self.player.take_damage(self.attack)
            return
        if self.move_name == "Three-note volley":
            for angle in (-23, 0, 23):
                self.projectiles.append(Projectile(self.screen, self.x, self.y, self.aim.rotate(angle), self.attack))
        elif self.move_name == "Sonic dart":
            dart = Projectile(self.screen, self.x, self.y, self.aim, self.attack)
            if self.name == "Rosin Spirit":
                dart.speed = 365
                dart.size = 10
                dart.colour = (229, 155, 97)
            elif self.name == "Ripple Wisp":
                dart.speed = 295
                dart.size = 12
                dart.colour = (111, 225, 215)
            elif self.name == "Bowshade":
                dart.speed = 355
                dart.size = 10
                dart.colour = (200, 164, 241)
            elif self.name == "Reed Wisp":
                dart.speed = 420
                dart.size = 8
                dart.colour = (173, 218, 194)
            self.projectiles.append(dart)
        else:
            hit = distance <= self.attack_range + self.player.size + self.size
            if self.move_name == "Resonance stomp":
                hit = distance <= 185
            elif self.move_name == "Fork thrust":
                hit = 0 <= offset.dot(self.aim) <= 280 and abs(offset.cross(self.aim)) < 50
            elif self.move_name == "Lunge":
                hit = hit and offset.dot(self.aim) >= 0 and abs(offset.cross(self.aim)) < 43
            if hit and self.can_reach_player():
                self.player.take_damage(self.attack)
        if self.enemy_type == "Overture":
            self.strikes += 1
            self.attack_cooldown = 1.10 if self.strikes % 3 else 2.0

    def skitter_lunge(self, dt):

        elapsed = min(dt, self.lunge_time)
        self.lunge_time -= elapsed
        move = self.aim * 410 * elapsed
        steps = max(1, math.ceil(move.length() / 6))
        for _ in range(steps):
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if not self.lunge_hit and 0 <= offset.dot(self.aim) <= 68 and abs(offset.cross(self.aim)) <= 37 and self.can_reach_player():
                self.player.take_damage(self.attack)
                self.lunge_hit = True
            x, y = self.x + move.x / steps, self.y + move.y / steps
            if not self.can_step(x, y):
                self.lunge_time = 0
                break
            self.x, self.y = x, y

    def draw_warning(self, x, y):

        color = (231, 156, 80) if self.windup else (251, 210, 127)
        origin = pg.Vector2(x, y)
        if self.name == "Score Swarm":
            colour = (190, 155, 202) if self.windup else (231, 191, 215)
            pg.draw.circle(self.screen, colour, (x, y), 96, 2)
            return
        if self.name in ("Silt Scorpion", "Mossback Snapper"):
            point = origin + self.aim * 65
            side = self.aim.rotate(90)
            color = (213, 151, 107) if self.windup else (248, 195, 130)
            if self.windup:
                pg.draw.lines(self.screen, color, False, [point - self.aim * 16 + side * 13, point, point - self.aim * 16 - side * 13], 3)
            else:
                strength = self.attack_animation_time / 0.3
                for i in range(3):
                    front = origin + self.aim * (35 + 11 * i)
                    back = front - self.aim * (13 + round(8 * strength))
                    pg.draw.line(self.screen, color, back + side * (i - 1) * 8, front, 2)
            return
        if self.name in ("Rosin Spirit", "Ripple Wisp"):
            point = origin + self.aim * 23
            point.y -= 15
            charge = 1 - self.windup / self.windup_length if self.windup else 1
            radius = 4 + round(charge * 7)
            pg.draw.circle(self.screen, (69, 152, 165) if self.name == "Ripple Wisp" else (170, 99, 82), (round(point.x), round(point.y)), radius, 2)
            pg.draw.circle(self.screen, (155, 247, 222) if self.name == "Ripple Wisp" else (243, 177, 109), (round(point.x), round(point.y)), max(2, radius // 3))
            for i in (-1, 1):
                spark = point + self.aim.rotate(i * 65) * (17 - charge * 7)
                pg.draw.rect(self.screen, (236, 166, 102), (round(spark.x), round(spark.y), 3, 3))
            return
        if self.name in ("Reed Wisp", "Bowshade"):
            point = origin + self.aim * 20
            point.y -= 19
            charge = 1 - self.windup / self.windup_length if self.windup else 1
            radius = 4 + round(charge * 7)
            center = (round(point.x), round(point.y))
            colour = (197, 158, 229) if self.name == "Bowshade" else (118, 184, 164)
            pg.draw.circle(self.screen, colour, center, radius, 2)
            pg.draw.circle(self.screen, (219, 243, 222), center, max(2, radius // 3))
            if self.windup:
                for i in (-1, 0, 1):
                    end = point + self.aim.rotate(i * 38) * (22 - charge * 8)
                    pg.draw.line(self.screen, (154, 198, 179), end, end - self.aim * 6, 2)
            return
        if self.name == "Chalk Skitter":
            tip = origin + self.aim * 72
            side = self.aim.rotate(90)
            if self.windup:
                pg.draw.lines(self.screen, (197, 177, 138), False, [tip - self.aim * 15 + side * 12, tip, tip - self.aim * 15 - side * 12], 2)
            elif self.lunge_time > 0:
                for angle in (-32, 32):
                    claw = origin + self.aim.rotate(angle) * 36
                    pg.draw.line(self.screen, (223, 216, 186), claw, claw + self.aim * 11, 2)
            return
        if self.move_name == "Resonance stomp":
            progress = 1 - self.windup / self.windup_length if self.windup else 1
            for angle in range(0, 360, 24):
                point = origin + pg.Vector2(150, 0).rotate(angle)
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 2 + round(progress * 2))
        elif self.move_name == "Fork thrust":
            for distance in range(65, 281, 35):
                point = origin + self.aim * distance
                tail = point - self.aim * 9
                side = self.aim.rotate(90) * 5
                pg.draw.lines(self.screen, color, False, [tail + side, point, tail - side], 2)
        elif self.move_name == "Three-note volley":
            for angle in (-23, 0, 23):
                direction = self.aim.rotate(angle)
                for distance in (75, 125, 175, 225):
                    point = origin + direction * distance
                    pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 3)
        else:
            pg.draw.line(self.screen, color, origin + self.aim * 22, origin + self.aim * 74, 3)

    def boss_rest_frame(self):

        if self.boss_steps and self.moving:
            step_length = 13 if self.enemy_type == "Guitar" else 36
            index = 1 + int(self.walked / step_length) % (len(self.boss_steps) - 1)
            frame = self.boss_steps[index]
        elif self.enemy_type == "Overture" and self.boss_steps and math.sin(self.animation_time * 2.6) > 0.2:
            frame = self.boss_steps[0]
        else:
            frame = self.keeper_poses[0]
        facing_left = self.facing_row == 1 if self.moving else self.aim.x < 0
        if facing_left:
            frame = pg.transform.flip(frame, True, False)
        return frame

    def keeper_frame(self):

        index = 0
        if self.windup or self.attack_animation_time:
            windup, impact = [(1, 2), (3, 4), (5, 6)][["Resonance stomp", "Fork thrust", "Three-note volley"].index(self.move_name)]
            if self.windup:
                index = windup
            elif self.attack_animation_time > 0.12:
                index = impact
            else:
                index = 7
        if index == 0:
            return self.boss_rest_frame()
        frame = self.keeper_poses[index]
        if self.aim.x < 0:
            return pg.transform.flip(frame, True, False)
        return frame

    def can_reach_player(self):

        if self.game_map is None:
            return True
        return self.game_map.clear_enemy_path(self.x, self.y, self.player.x, self.player.y, 4)

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
            if self.game_map is not None and not self.game_map.can_move_circle(projectile.x, projectile.y, projectile.size):
                self.projectiles.remove(projectile)
            elif projectile.collides_with_player(self.player):
                self.player.take_damage(projectile.damage)
                self.projectiles.remove(projectile)
            elif not projectile.is_on_screen():
                self.projectiles.remove(projectile)

    #

    def render(self, camera):

        if self.current_hp <= 0:
            x, y = camera.apply(self.x, self.y)
            frame = self.keeper_poses[7] if self.keeper_poses else self.idle_frames[self.facing_row][0]
            progress = min(1, self.death_time / 0.65)
            if self.death_frames:
                poses = self.death_frames[self.facing_row]
                frame = poses[min(len(poses) - 1, int(progress * (len(poses) + 1)))].copy()
                if self.name in ("Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                    y -= round(max(0, 1 - progress * (2.2 if self.name == "Ripple Wisp" else 4)) * 14)
            elif self.enemy_type in PIXEL_BOSSES:
                frame = frame.copy()
                y += round(progress * 10)
            else:
                frame = pg.transform.scale(frame, (frame.get_width(), max(2, round(frame.get_height() * (1 - progress * 0.82)))))
            frame.set_alpha(round(255 * (1 - progress)))
            self.screen.blit(frame, frame.get_rect(midbottom=(x, y + 14)))
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                spread = round(14 + 45 * progress)
                pg.draw.rect(self.screen, (181 - round(progress * 100), 129 - round(progress * 70), 79), (x + dx * spread, y + dy * spread, 3, 3))
            return

        if self.windup > 0 and self.windup_frames:
            frames = self.windup_frames[self.facing_row]
            progress = 1 - self.windup / self.windup_length
            frame = frames[min(len(frames) - 1, int(progress * len(frames)))]
        elif self.attack_animation_time > 0:
            frames = self.attack_frames[self.facing_row]
            frame_number = int((0.3 - self.attack_animation_time) * 16)
            if self.directional_mob:
                frame_number = int((1 - self.attack_animation_time / 0.3) * len(frames))
            frame_number = min(len(frames) - 1, frame_number)
            frame = frames[frame_number]
        else:
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                frames = self.run_frames[self.facing_row]
                frame = frames[int(self.animation_time * (10 if self.name == "Ripple Wisp" else 15)) % len(frames)]
            elif self.moving:
                frames = self.run_frames[self.facing_row]
                phase = self.animation_time * 10
                if self.name in ("Chalk Skitter", "Silt Scorpion", "Mossback Snapper", "Score Swarm"):
                    phase = self.walked / (8 if self.name == "Mossback Snapper" else 11)
                frame = frames[int(phase) % len(frames)]
            else:
                frames = self.idle_frames[self.facing_row]
                frame = frames[int(self.animation_time * 5) % len(frames)]
        if self.keeper_poses:
            frame = self.keeper_frame()
        screen_x, screen_y = camera.apply(self.x, self.y)
        if self.windup > 0:
            self.draw_warning(screen_x, screen_y)
            if not self.keeper_poses and not self.windup_frames:
                frame = pg.transform.scale(frame, (frame.get_width() + 6, max(1, frame.get_height() - 9)))
        elif self.attack_animation_time > 0 and self.move_name:
            self.draw_warning(screen_x, screen_y)
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            pg.draw.ellipse(self.screen, (27, 30, 46), (screen_x - 14, screen_y - 4, 28, 10))
            screen_y -= 14 + round(math.sin(self.animation_time * 8) * 3)
        if self.attack_animation_time > 0 and self.move_name and not self.directional_mob and self.enemy_type not in PIXEL_BOSSES:
            progress = 1 - self.attack_animation_time / 0.3
            force = math.sin(progress * math.pi)
            push = self.aim * force * (17 if self.enemy_type == "Overture" else 11)
            frame = pg.transform.scale(frame, (frame.get_width() + round(force * 8), frame.get_height() + round(force * 12)))
            screen_x += round(push.x)
            screen_y += round(push.y)
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                screen_y += round(force * 12)
        foot_offset = 21 if self.keeper_poses else 14
        if self.enemy_type == "Violin":
            foot_offset = 16
        if self.enemy_type in PIXEL_BOSSES:
            if not (self.moving or self.windup or self.attack_animation_time or self.encore or self.teleport_time or self.volley):
                pace = 5 if self.enemy_type in ("Guitar", "Violin") else 4
                frame = self.boss_idle[int(self.animation_time * pace) % len(self.boss_idle)]
                if self.aim.x < 0:
                    frame = pg.transform.flip(frame, True, False)
            else:
                offset_x, offset_y = boss_pose_offset(self)
                screen_x += offset_x
                screen_y += offset_y
        sprite_rect = frame.get_rect(midbottom=(screen_x, screen_y + foot_offset))
        self.screen.blit(frame, sprite_rect)
        sprite_top = sprite_rect.top + frame.get_bounding_rect().top
        bar_width = self.size * 2
        bar_x = screen_x - bar_width // 2
        bar_y = sprite_top - 12
        name_rect = self.name_image.get_rect(midbottom=(screen_x, bar_y - 3))
        pg.draw.rect(self.screen, (20, 24, 34), name_rect.inflate(8, 2))
        self.screen.blit(self.name_image, name_rect)
        pg.draw.rect(self.screen, (27, 31, 41), (bar_x, bar_y, bar_width, 7))
        pg.draw.rect(self.screen, (145, 190, 220), (bar_x, bar_y, bar_width * self.current_hp / self.max_hp, 7))
        for projectile in self.projectiles:
            projectile.render(camera)

    #

    def take_damage(self, damage):
        player = self.player.owner.player if self.player.clan == "Familiar" else self.player
        if player.progress is not None and self.current_hp > 0:
            dealt = min(damage,self.current_hp)
            player.progress["damage_dealt"] += dealt
            player.progress["highest_hit"] = max(player.progress["highest_hit"],dealt)
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
        self.player.enemies = self.enemies
        self.spawn_timer = 0
        self.spawn_delay = 2.0
        self.habitats = {}
        self.respawn_timers = {}
        if self.game_map is not None:
            from Bosses import CelloBoss, FluteBoss, GuitarBoss, HarpBoss, PianoBoss, ViolinBoss

            for name, enemy_type, x, y in HABITATS + FROST_HABITATS + GUITAR_HABITATS + FLUTE_HABITATS + CELLO_HABITATS + HARP_HABITATS + VIOLIN_HABITATS:
                enemy = Enemy(screen, enemy_type, player, game_map, name, (x, y))
                self.enemies.append(enemy)
                if enemy.directional_mob:
                    habitat = game_map.location_name(x,y)
                    if habitat == "Connecting passage":
                        habitat = (x//1400,y//1400)
                    self.habitats.setdefault(habitat,[]).append((name,enemy_type,x,y))
            self.enemies.append(PianoBoss(screen, player, game_map))
            self.enemies.append(GuitarBoss(screen, player, game_map))
            self.enemies.append(FluteBoss(screen, player, game_map))
            self.enemies.append(CelloBoss(screen, player, game_map))
            self.enemies.append(HarpBoss(screen, player, game_map))
            self.enemies.append(ViolinBoss(screen, player, game_map))

    #

    def update(self, dt):

        self.spawn_timer -= dt
        if self.game_map is None and self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = self.spawn_delay
        enemies_to_update = self.enemies[:]
        for enemy in enemies_to_update:
            if self.player.powers and enemy in self.player.powers.stunned:
                continue
            target = self.target_for(enemy)
            enemy.player = target
            try:
                enemy.update(dt)
            finally:
                enemy.player = self.player
            if enemy.death_time >= 0.65:
                self.enemies.remove(enemy)
        if self.game_map is not None:
            self.respawn_mobs(dt)
    
    #

    def respawn_mobs(self, dt):

        living = {(enemy.name, *enemy.home) for enemy in self.enemies if enemy.directional_mob and enemy.current_hp > 0}
        for habitat, members in self.habitats.items():
            if any((name,x,y) in living for name,_,x,y in members):
                self.respawn_timers.pop(habitat,None)
                continue
            timer = self.respawn_timers.get(habitat,3.0)
            self.respawn_timers[habitat] = max(0,timer-dt)
            if self.respawn_timers[habitat] > 0:
                continue
            positions = []
            for _,_,x,y in members:
                position = self.respawn_position(x,y,positions)
                if position is None:
                    break
                positions.append(position)
            if len(positions) != len(members):
                continue
            for (name,kind,x,y),position in zip(members,positions):
                enemy = Enemy(self.screen,kind,self.player,self.game_map,name,(x,y))
                enemy.x,enemy.y = position
                self.enemies.append(enemy)
            self.respawn_timers.pop(habitat,None)

    def respawn_position(self, x, y, positions):

        for dx,dy in [(0,0),(52,0),(-52,0),(0,52),(0,-52),(75,55),(-75,-55)]:
            point = (x+dx,y+dy)
            if math.hypot(point[0]-self.player.x,point[1]-self.player.y) < 64:
                continue
            if any(math.hypot(point[0]-px,point[1]-py)<48 for px,py in positions):
                continue
            if self.game_map.can_move_circle(*point,28):
                return point
        return None

    def target_for(self, enemy):

        powers = self.player.powers
        if not powers or powers.familiar is None or self.game_map is None:
            return self.player
        familiar = powers.familiar_actor
        if math.hypot(enemy.x-familiar.x,enemy.y-familiar.y) > 1050:
            return self.player
        arena = "Overture Arena" if enemy.enemy_type == "Overture" else getattr(enemy,"arena_room",None)
        if arena and not self.game_map.location_name(familiar.x,familiar.y).endswith(arena):
            return self.player
        if not self.game_map.clear_enemy_path(enemy.x,enemy.y,familiar.x,familiar.y,4):
            return self.player
        return familiar

    def render_enemy(self, enemy, camera):

        enemy.player = self.target_for(enemy)
        try:
            enemy.render(camera)
        finally:
            enemy.player = self.player

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
