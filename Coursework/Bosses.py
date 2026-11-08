import math
import pygame as pg
from Classes import Enemy, Projectile
from BossMotion import boss_pose_offset, draw_frost_fold
from Frost import ARENA_X, ARENA_Y
from Guitar import GUITAR_ARENA_X, GUITAR_ARENA_Y
from Flute import FLUTE_ARENA_X, FLUTE_ARENA_Y
from Cello import CELLO_ARENA_X, CELLO_ARENA_Y
from Harp import HARP_ARENA_X, HARP_ARENA_Y


# Piano Ultra Boss

class PianoNote(Projectile):

    def __init__(self, screen, x, y, direction, damage):

        super().__init__(screen, x, y, direction, damage)
        self.speed = 580

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        for distance, size in [(25, 3), (15, 5), (8, 6)]:
            px = round(x - self.direction.x * distance)
            py = round(y - self.direction.y * distance)
            pg.draw.rect(self.screen, (70, 149, 189), (px - size // 2, py - size // 2, size, size))
        pg.draw.ellipse(self.screen, (89, 182, 211), (x - 9, y - 5, 16, 12))
        pg.draw.ellipse(self.screen, (214, 250, 251), (x - 6, y - 3, 11, 7))
        pg.draw.lines(self.screen, (214, 250, 251), False, [(x + 4, y + 1), (x + 4, y - 12), (x + 11, y - 8)], 3)


class PianoBoss(Enemy):

    arena_room = "Piano Chamber"
    region_folder = "FrostPiano"
    instrument = "Piano"
    home_position = (ARENA_X, ARENA_Y)

    def __init__(self, screen, player, game_map):

        super().__init__(screen, self.instrument, player, game_map, f"{self.instrument} Ultra Boss", self.home_position)
        self.pattern = 0
        self.chord = []
        self.lanes = []
        self.volley = []
        self.beat_timer = 0
        self.engaged = False
        self.recovery = 0
        self.echoes = []
        self.wave = None
        self.wave_y = 0
        self.wave_gap = ARENA_X
        self.wave_hit = False
        self.encore = 0
        self.second_phase = False
        self.teleport_time = 0
        self.teleport_index = 0
        self.teleport_origin = self.home_position
        self.teleport_target = self.home_position

    def set_stats(self):

        self.max_hp = 1100
        self.current_hp = self.max_hp
        self.attack = 47
        self.size = 82

    def update(self, dt):

        self.animation_time += dt
        if self.current_hp <= 0:
            self.death_time += dt
            return
        if not self.game_map.location_name(self.player.x, self.player.y).endswith(self.arena_room):
            self.engaged = False
            self.windup = 0
            self.attack_animation_time = 0
            self.projectiles.clear()
            self.volley.clear()
            self.echoes.clear()
            self.wave = None
            self.encore = 0
            self.teleport_time = 0
            self.recovery = 0
            return
        if not self.engaged:
            self.engaged = True
            self.recovery = 0.8
        if self.instrument in ("Piano", "Flute", "Harp", "Violin") and self.update_teleport(dt):
            return
        self.update_projectiles(dt)
        self.update_floor_attacks(dt)
        if self.current_hp <= self.max_hp / 2 and not self.second_phase:
            self.second_phase = True
            self.encore = 1.1
            self.windup = 0
            self.attack_animation_time = 0
            self.echoes.clear()
            self.volley.clear()
            self.projectiles.clear()
            self.wave = None
        if self.encore > 0:
            self.encore = max(0, self.encore - dt)
            return
        if self.windup > 0:
            self.windup = max(0, self.windup - dt)
            if self.windup == 0:
                self.release_attack()
            return
        self.attack_animation_time = max(0, self.attack_animation_time - dt)
        if self.volley:
            self.beat_timer -= dt
            if self.beat_timer <= 0:
                angle = self.volley.pop(0)
                shot = self.make_note(self.aim.rotate(angle))
                self.projectiles.append(shot)
                self.beat_timer += 0.105
        self.recovery = max(0, self.recovery - dt)
        if self.recovery == 0 and not self.echoes and self.wave is None:
            self.start_phrase()

    def teleport_anchor(self):

        anchors = [
            (ARENA_X - 570, ARENA_Y - 240), (ARENA_X + 570, ARENA_Y - 240),
            (ARENA_X - 570, ARENA_Y + 250), (ARENA_X + 570, ARENA_Y + 250),
            (ARENA_X, ARENA_Y + 320)
        ]
        for step in range(len(anchors)):
            x, y = anchors[(step + self.teleport_index * 2) % len(anchors)]
            if math.hypot(x - self.x, y - self.y) < 180:
                continue
            if math.hypot(x - self.player.x, y - self.player.y) < 145:
                continue
            if self.can_step(x, y):
                return x, y
        return None

    def update_teleport(self, dt):

        thresholds = (0.75, 0.50, 0.25)
        if self.teleport_time == 0:
            if self.teleport_index == len(thresholds) or self.current_hp > self.max_hp * thresholds[self.teleport_index]:
                return False
            target = self.teleport_anchor()
            if target is None:
                return False
            self.teleport_time = 1.0
            self.teleport_origin = (self.x, self.y)
            self.teleport_target = target
            self.windup = 0
            self.attack_animation_time = 0
            self.echoes.clear()
            self.volley.clear()
            self.projectiles.clear()
            self.wave = None
        previous = self.teleport_time
        self.teleport_time = max(0, self.teleport_time - dt)
        if previous > 0.50 >= self.teleport_time:
            x, y = self.teleport_target
            if not self.can_step(x, y) or self.body_overlap(self.player.x, self.player.y, self.player.size, x, y) > 0:
                target = self.teleport_anchor()
                if target is None:
                    self.teleport_time = 0
                    return True
                self.teleport_target = target
            self.x, self.y = self.teleport_target
            self.teleport_index += 1
        if self.teleport_time == 0:
            self.recovery = 0.85
        return True

    def make_note(self, direction):

        return PianoNote(self.screen, self.x, self.y, direction, self.attack)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Frozen Chord", "Black-Key Sweep", "Rising Arpeggio", "Echo Notes", "Glissando"][self.pattern]
        self.windup_length = [0.92, 0.86, 0.98, 0.76, 1.05][self.pattern]
        if self.current_hp <= self.max_hp / 2:
            self.windup_length *= 0.82
        self.windup = self.windup_length
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - pg.Vector2(self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target + side * shift for shift in (-126, 0, 126)]
        # Alternate lanes, leaving a wide gap between each pair.
        center = round((target.x - ARENA_X) / 160) * 160 + ARENA_X
        self.lanes = [pg.Rect(center + step * 320 - 49, ARENA_Y - 520, 110, 1040) for step in (-2, -1, 0, 1, 2)]
        if self.pattern == 3:
            self.chord = [target + side * shift for shift in (-145, 0, 145)]
        if self.pattern == 4:
            shift = 165 if target.x <= ARENA_X else -165
            self.wave_gap = max(ARENA_X - 545, min(ARENA_X + 545, target.x + shift))
            self.wave_y = ARENA_Y - 390

    def release_attack(self):

        self.attack_animation_time = 0.3
        self.strikes += 1
        self.recovery = 1.25 if self.current_hp > self.max_hp / 2 else 1.0
        if self.pattern == 0:
            if any(point.distance_to((self.player.x, self.player.y)) <= 110 + self.player.size for point in self.chord):
                self.player.take_damage(self.attack)
        elif self.pattern == 1:
            if any(lane.inflate(self.player.size * 2, self.player.size * 2).collidepoint(self.player.x, self.player.y) for lane in self.lanes):
                self.player.take_damage(self.attack + 7)
        elif self.pattern == 2:
            self.volley = [-30, -15, 0, 15, 30]
            self.beat_timer = 0
            self.recovery += 0.42
        elif self.pattern == 3:
            self.echoes = [(point, 0.28 + index * 0.29) for index, point in enumerate(self.chord)]
        else:
            self.wave = self.wave_y
            self.wave_hit = False

    def update_floor_attacks(self, dt):

        active = []
        for point, remaining in self.echoes:
            remaining -= dt
            if remaining > 0:
                active.append((point, remaining))
            else:
                if point.distance_to((self.player.x, self.player.y)) <= 68 + self.player.size:
                    self.player.take_damage(self.attack - 9)
        self.echoes = active
        if self.wave is not None:
            speed = 650 if self.second_phase else 540
            self.wave += speed * dt
            in_width = abs(self.player.x - ARENA_X) <= 720
            in_gap = abs(self.player.x - self.wave_gap) <= 95 - self.player.size
            if in_width and not in_gap and not self.wave_hit and abs(self.player.y - self.wave) <= self.player.size + 15:
                self.player.take_damage(self.attack + 3)
                self.wave_hit = True
            if self.wave >= ARENA_Y + 425:
                self.wave = None

    def render(self, camera):

        if self.current_hp > 0:
            if self.teleport_time > 0:
                self.render_teleport(camera)
            for point, remaining in self.echoes:
                x, y = camera.apply(point.x, point.y)
                pg.draw.circle(self.screen, (114, 169, 226), (x, y), 68, 2)
                pg.draw.circle(self.screen, (207, 241, 249), (x, y), max(4, round(remaining * 55)), 3)
            if self.wave is not None:
                self.draw_wave(camera, self.wave, (162, 229, 248))
            if self.encore > 0:
                x, y = camera.apply(self.x, self.y)
                radius = round(90 + (1.1 - self.encore) * 90)
                pg.draw.circle(self.screen, (147, 209, 243), (x, y), radius, 3)
                pg.draw.circle(self.screen, (74, 135, 187), (x, y), radius + 12, 2)
        super().render(camera)

    def render_teleport(self, camera):

        draw_frost_fold(self.screen, camera, self.teleport_origin, 1 - self.teleport_time, False)
        draw_frost_fold(self.screen, camera, self.teleport_target, 1 - abs(2 * self.teleport_time - 1), True)

    def draw_wave(self, camera, y, color):

        for left, right in [(ARENA_X - 720, self.wave_gap - 95), (self.wave_gap + 95, ARENA_X + 720)]:
            x, py = camera.apply(left, y)
            width = round(right - left)
            pg.draw.rect(self.screen, (57, 101, 153), (x, py - 10, width, 21))
            pg.draw.line(self.screen, color, (x, py - 6), (x + width, py - 6), 3)
            for offset in range(0, width - 14, 22):
                pg.draw.rect(self.screen, color, (x + offset, py - 5, 12, 10))

    def keeper_frame(self):

        index = 0
        if self.teleport_time > 0:
            frame = self.keeper_poses[5 if self.teleport_time > 0.5 else 7].copy()
            frame.set_alpha(round(255 * abs(self.teleport_time - 0.5) * 2))
            return frame
        if self.encore > 0:
            index = 1
        elif self.windup > 0:
            index = (1, 3, 5, 5, 3)[self.pattern]
        elif self.attack_animation_time > 0.10 or self.volley:
            index = (2, 4, 6, 6, 4)[self.pattern]
        if index == 0:
            return self.boss_rest_frame()
        frame = self.keeper_poses[index]
        if self.aim.x < 0:
            return pg.transform.flip(frame, True, False)
        return frame

    def draw_warning(self, x, y):

        color = (104, 200, 225) if self.windup else (204, 249, 250)
        offset_x = x - self.x
        offset_y = y - self.y
        if self.pattern == 0:
            for point in self.chord:
                center = (round(point.x + offset_x), round(point.y + offset_y))
                pg.draw.circle(self.screen, color, center, 110, 3 if self.windup else 8)
                pg.draw.circle(self.screen, color, center, 7, 2)
        elif self.pattern == 1:
            for lane in self.lanes:
                rect = lane.move(round(offset_x), round(offset_y))
                for y_line in range(rect.top, rect.bottom, 34):
                    pg.draw.line(self.screen, color, (rect.left, y_line), (rect.left, y_line + 18), 3)
                    pg.draw.line(self.screen, color, (rect.right, y_line), (rect.right, y_line + 18), 3)
        elif self.pattern == 3:
            for point in self.chord:
                center = (round(point.x + offset_x), round(point.y + offset_y))
                pg.draw.circle(self.screen, (114, 169, 226), center, 68, 2)
        elif self.pattern == 4:
            if self.windup:
                top = round(self.wave_y + offset_y)
                for gap in (self.wave_gap - 95, self.wave_gap + 95):
                    edge = round(gap + offset_x)
                    for dy in range(0, 790, 48):
                        pg.draw.line(self.screen, (130, 223, 220), (edge, top + dy), (edge, top + dy + 16), 3)
        else:
            origin = pg.Vector2(x, y)
            for angle in (-30, -15, 0, 15, 30):
                for distance in (105, 155, 205, 255):
                    point = origin + self.aim.rotate(angle) * distance
                    pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 3)


class GuitarBoss(PianoBoss):

    arena_room = "Resonance Arena"
    region_folder = "GuitarCaverns"
    instrument = "Guitar"
    home_position = (GUITAR_ARENA_X, GUITAR_ARENA_Y)

    def set_stats(self):

        self.max_hp = 1250
        self.current_hp = self.max_hp
        self.attack = 48
        self.speed = 145
        self.size = 82

    def footprint(self):

        return 46, 22, 8

    def update(self, dt):

        self.moving = False
        super().update(dt)
        if not self.engaged and self.current_hp > 0:
            self.x, self.y = self.home_position
            return
        if self.current_hp > 0 and self.recovery > 0 and not self.windup and not self.encore and self.wave is None and self.attack_animation_time <= 0:
            self.move_towards(self.player.x, self.player.y, dt, 148)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Pick Rush", "Hammer-On", "Palm Mute", "Pickup Pull", "Fret Slide"][self.pattern]
        self.windup_length = [0.69, 0.62, 0.92, 0.84, 0.94][self.pattern]
        if self.second_phase:
            self.windup_length *= 0.82
        self.windup = self.windup_length
        self.wave_hit = False
        self.aim_at_player()

    def aim_at_player(self):

        aim = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if aim.length_squared():
            self.aim = aim.normalize()

    def release_attack(self):

        self.attack_animation_time = 0.3
        self.strikes += 1
        self.recovery = 1.25 if not self.second_phase else 1.02
        if self.pattern == 0:
            self.wave = 0.40
        elif self.pattern == 1:
            self.hit_front(155, 60, self.attack - 10)
            self.wave = 0.28
        elif self.pattern == 2:
            # Wait out the guard for a longer opening.
            self.recovery += 0.4
        elif self.pattern == 3:
            self.wave = 0.62
        else:
            self.wave = -60

    def take_damage(self, damage):

        if self.current_hp > 0 and self.pattern == 2 and self.windup > 0:
            self.windup = 0
            self.strikes += 1
            self.aim_at_player()
            self.wave = 0.26
            self.recovery = 1.35
            self.attack_animation_time = 0.3
            return False
        return super().take_damage(damage)

    def hit_front(self, reach, half_width, damage):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if 0 <= offset.dot(self.aim) <= reach and abs(offset.cross(self.aim)) <= half_width and self.can_reach_player():
            self.player.take_damage(damage)
            return True
        return False

    def update_floor_attacks(self, dt):

        if self.wave is None:
            return
        if self.pattern == 4:
            self.update_fret_slide(dt)
            return

        step_time = min(dt, self.wave)
        self.wave -= step_time
        if self.pattern == 0:
            self.rush(step_time)
        elif self.pattern == 3:
            self.pull_rogue(step_time)

        if self.wave == 0:
            self.wave = None
            if self.pattern == 1:
                self.hit_front(210, 82, self.attack)
                self.attack_animation_time = 0.3
            elif self.pattern == 2:
                self.hit_front(180, 65, self.attack + 9)
                self.attack_animation_time = 0.3
            elif self.pattern == 3:
                self.hit_front(155, 65, self.attack)
                self.attack_animation_time = 0.3

    def rush(self, dt):

        move = self.aim * (795 if self.second_phase else 680) * dt
        steps = max(1, math.ceil(move.length() / 8))
        for step in range(steps):
            if not self.wave_hit and self.hit_front(105, 57, self.attack + 2):
                self.wave_hit = True
            x, y = self.x + move.x / steps, self.y + move.y / steps
            if not self.can_step(x, y) or not self.game_map.location_name(x, y).endswith(self.arena_room):
                self.wave = 0
                break
            self.x, self.y = x, y

    def pull_rogue(self, dt):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if offset.length() > 450 or offset.dot(self.aim) < 0 or abs(offset.cross(self.aim)) > 95:
            return
        if self.player.dash_time > 0 or not self.can_reach_player():
            return
        pull = self.aim * (-270 * dt)
        self.player._move(pull.x, pull.y, self.game_map)

    def update_fret_slide(self, dt):

        previous = self.wave
        self.wave = min(60, self.wave + (180 if self.second_phase else 145) * dt)
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if not self.wave_hit and 0 < offset.length() <= 450 + self.player.size:
            angle = (self.aim.angle_to(offset) + 180) % 360 - 180
            margin = math.degrees(math.asin(min(1, (self.player.size + 7) / offset.length())))
            if previous - margin <= angle <= self.wave + margin:
                self.player.take_damage(self.attack + 4)
                self.wave_hit = True
        if self.wave >= 60:
            self.wave = None

    def draw_wave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        origin = pg.Vector2(x, y)
        copper = (249, 170, 95)
        if self.pattern == 0:
            for angle in (-16, 0, 16):
                pg.draw.line(self.screen, copper, origin, origin - self.aim.rotate(angle) * 58, 4)
        elif self.pattern == 3:
            side = self.aim.rotate(90)
            for i in range(-2, 3):
                point = origin + self.aim * (105 + (i + 2) * 42) + side * i * 14
                pg.draw.line(self.screen, copper, point, point - self.aim * 26, 3)
        elif self.pattern == 4:
            tip = origin + self.aim.rotate(value) * 450
            pg.draw.line(self.screen, (113, 53, 49), origin, tip, 15)
            pg.draw.line(self.screen, (255, 164, 71), origin, tip, 8)
            pg.draw.line(self.screen, (255, 233, 174), origin, tip, 3)

    def draw_warning(self, x, y):

        color = (227, 134, 67) if self.windup else (255, 213, 137)
        origin = pg.Vector2(x, y)
        side = self.aim.rotate(90)
        if self.pattern == 0 and self.windup:
            for distance in range(70, 330, 42):
                point = origin + self.aim * distance
                tail = point - self.aim * 18
                pg.draw.lines(self.screen, color, False, [tail + side * 18, point, tail - side * 18], 3)
        elif self.pattern in (1, 2) and (self.pattern == 1 or not self.windup):
            reach = 155 if self.windup else 210
            points = [origin + self.aim.rotate(angle) * reach for angle in range(-32, 33, 8)]
            pg.draw.lines(self.screen, color, False, points, 3)
        elif self.pattern == 2:
            pg.draw.lines(self.screen, (202, 215, 174), False, [(x - 49, y - 55), (x - 36, y - 75), (x + 36, y - 75), (x + 49, y - 55)], 4)
        elif self.pattern == 3:
            for i in (-1, 1):
                start = origin + side * (i * 16)
                end = origin + self.aim * 450 + side * (i * 95)
                pg.draw.line(self.screen, (194, 126, 104), start, end, 2)
        elif self.windup:
            for angle in (-60, 60):
                direction = self.aim.rotate(angle)
                for distance in range(75, 450, 30):
                    pg.draw.line(self.screen, color, origin + direction * distance, origin + direction * (distance + 14), 3)
            points = [origin + self.aim.rotate(angle) * 450 for angle in range(-60, 61, 10)]
            pg.draw.lines(self.screen, color, False, points, 2)


class WindOrb(Projectile):

    def __init__(self, screen, x, y, direction, damage, curve):

        super().__init__(screen, x, y, direction, damage)
        self.curve = curve
        self.speed = 320
        self.size = 13
        self.life = 2.5

    def update(self, dt):

        self.life -= dt
        self.direction = self.direction.rotate(self.curve * dt)
        super().update(dt)

    def is_on_screen(self):

        return self.life > 0 and super().is_on_screen()

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        pg.draw.circle(self.screen, (102, 162, 150), (x, y), 12, 2)
        pg.draw.arc(self.screen, (203, 240, 218), (x - 10, y - 10, 20, 20), 0.4, 4.9, 3)
        pg.draw.circle(self.screen, (223, 240, 229), (x, y), 3)


class FluteBoss(PianoBoss):

    arena_room = "Flute Hall"
    region_folder = "FluteCloister"
    instrument = "Flute"
    home_position = (FLUTE_ARENA_X, FLUTE_ARENA_Y)

    def set_stats(self):

        self.max_hp = 1350
        self.current_hp = self.max_hp
        self.attack = 48
        self.size = 82

    def footprint(self):

        return 37, 22, 8

    def teleport_anchor(self):

        for side in (1, -1):
            for offset in (-330, 310, 0):
                x = FLUTE_ARENA_X + 490 * side
                y = FLUTE_ARENA_Y + offset
                if math.hypot(x - self.x, y - self.y) > 220 and math.hypot(x - self.player.x, y - self.player.y) > 145 and self.can_step(x, y):
                    return x, y
        return None

    def render_teleport(self, camera):

        for index, point in enumerate((self.teleport_origin, self.teleport_target)):
            x, y = camera.apply(*point)
            spin = (1 - self.teleport_time) * 350 + index * 90
            for i in range(16):
                shift = pg.Vector2(23 + i * 4, 0).rotate(spin + i * 26)
                px, py = round(x + shift.x), round(y + shift.y * 0.5 - i * 3)
                pg.draw.line(self.screen, (165, 215, 197), (px - 9, py + 2), (px + 8, py), 2)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Long Breath", "Spiral Current", "Breathing Space", "Crossdraft", "Reed Wisps"][self.pattern]
        self.windup_length = [0.82, 0.76, 1.12, 0.85, 0.91][self.pattern]
        if self.second_phase:
            self.windup_length *= 0.85
        self.windup = self.windup_length
        direction = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if direction.length_squared():
            self.aim = direction.normalize()
        side = -1 if self.player.x > FLUTE_ARENA_X else 1
        self.wave_gap = (FLUTE_ARENA_X + side * 265, FLUTE_ARENA_Y + 170)
        self.wave_hit = False

    def release_attack(self):

        self.attack_animation_time = 0.3
        self.strikes += 1
        self.recovery = 1.35 if not self.second_phase else 1.05
        if self.pattern == 0:
            self.wave = 0.48
        elif self.pattern == 1:
            for angle, curve in [(-35, 68), (0, -74), (35, 68)]:
                self.projectiles.append(WindOrb(self.screen, self.x, self.y, self.aim.rotate(angle), self.attack, curve))
        elif self.pattern == 2:
            if math.hypot(self.player.x - self.wave_gap[0], self.player.y - self.wave_gap[1]) > 170:
                self.player.take_damage(self.attack + 4)
        elif self.pattern == 3:
            self.wave = 0.68
        else:
            for angle in (-90, 90, 180):
                direction = self.aim.rotate(angle)
                start = pg.Vector2(self.x, self.y) + direction * 95
                if self.game_map.can_move_circle(start.x, start.y, 14):
                    orb = WindOrb(self.screen, start.x, start.y, direction.rotate(70), self.attack - 8, 112)
                    orb.speed = 210
                    self.projectiles.append(orb)

    def update_floor_attacks(self, dt):

        if self.wave is None:
            return
        elapsed = min(dt, self.wave)
        self.wave -= elapsed
        if self.pattern == 0:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if 0 < offset.length() < 430 and self.aim.dot(offset.normalize()) > 0.78 and self.can_reach_player():
                if not self.wave_hit:
                    self.player.take_damage(self.attack)
                    self.wave_hit = True
                push = self.aim * 310 * elapsed
                self.player._move(push.x, push.y, self.game_map)
        elif self.pattern == 3 and self.player.dash_time <= 0:
            side = self.aim.rotate(90)
            push = side * 310 * elapsed
            x, y = self.player.x, self.player.y
            self.player._move(push.x, push.y, self.game_map)
            if not self.wave_hit and math.hypot(x - self.player.x, y - self.player.y) < push.length() * 0.30:
                self.player.take_damage(self.attack - 10)
                self.wave_hit = True
        if self.wave == 0:
            self.wave = None

    def draw_wave(self, camera, value, color):

        if self.pattern == 0:
            x, y = camera.apply(self.x, self.y)
            origin = pg.Vector2(x, y)
            for i in range(-3, 4):
                direction = self.aim.rotate(i * 10)
                for j in range(3):
                    point = origin + direction * (105 + j * 107 + (0.48 - value) * 95)
                    pg.draw.line(self.screen, (163, 220, 198), point, point + direction * 34, 2)
        elif self.pattern == 3:
            x, y = camera.apply(FLUTE_ARENA_X, FLUTE_ARENA_Y)
            side = self.aim.rotate(90)
            for i in range(18):
                point = pg.Vector2(x + (i * 83) % 900 - 450, y + (i * 71) % 620 - 310) + side * ((0.68 - value) * 90)
                pg.draw.line(self.screen, (157, 214, 194), point, point + side * 39, 2)

    def draw_warning(self, x, y):

        color = (133, 207, 181)
        origin = pg.Vector2(x, y)
        if self.pattern == 0:
            for angle in (-38, 38):
                direction = self.aim.rotate(angle)
                for distance in range(75, 430, 43):
                    point = origin + direction * distance
                    pg.draw.line(self.screen, color, point, point + direction * 19, 2)
        elif self.pattern == 1:
            for angle in (-35, 0, 35):
                point = origin + self.aim.rotate(angle) * 110
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 13, 3)
        elif self.pattern == 2:
            safe = (round(x + self.wave_gap[0] - self.x), round(y + self.wave_gap[1] - self.y))
            pg.draw.circle(self.screen, (211, 236, 189), safe, 170, 4)
            pg.draw.circle(self.screen, (107, 158, 144), safe, 162, 2)
        elif self.pattern == 3:
            side = self.aim.rotate(90)
            for i in (-2, -1, 0, 1, 2):
                point = origin + self.aim * (i * 75) + side * 100
                tail = point - side * 24
                pg.draw.lines(self.screen, color, False, [tail + self.aim * 11, point, tail - self.aim * 11], 3)
        else:
            for angle in (-90, 90, 180):
                point = origin + self.aim.rotate(angle) * 95
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 15, 2)


class CelloBoss(PianoBoss):

    arena_room = "Cello Amphitheatre"
    region_folder = "CelloCatacombs"
    instrument = "Cello"
    home_position = (CELLO_ARENA_X, CELLO_ARENA_Y)

    def set_stats(self):

        self.max_hp = 1500
        self.current_hp = self.max_hp
        self.attack = 52
        self.speed = 136
        self.size = 84

    def footprint(self):

        return 47, 25, 8

    def update(self, dt):

        self.moving = False
        super().update(dt)
        if not self.engaged and self.current_hp > 0:
            self.x, self.y = self.home_position
            return
        if self.current_hp > 0 and self.recovery > 0 and not self.windup and not self.encore and self.wave is None and self.attack_animation_time <= 0:
            self.move_towards(self.player.x, self.player.y, dt, 145)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Downbow", "Bridge Break", "Legato", "Bow Bind", "Bass Steps"][self.pattern]
        self.windup_length = [0.78, 0.92, 1.0, 1.0, 0.76][self.pattern]
        if self.second_phase:
            self.windup_length *= 0.84
        self.windup = self.windup_length
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        self.wave_hit = False
        self.chord = []

    def release_attack(self):

        self.attack_animation_time = 0.3
        self.strikes += 1
        self.recovery = 1.4 if not self.second_phase else 1.1
        if self.pattern == 0:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if 0 <= offset.dot(self.aim) <= 245 and abs(offset.cross(self.aim)) <= 48 and self.can_reach_player():
                self.player.take_damage(self.attack + 7)
        elif self.pattern == 1:
            self.wave = 0.93
        elif self.pattern == 2:
            self.wave = 1.05
            self.last_breath_position = (self.player.x, self.player.y)
            self.breath_still = 0
        elif self.pattern == 3:
            if math.hypot(self.player.x - self.x, self.player.y - self.y) < 265 and self.can_reach_player():
                self.player.take_damage(self.attack)
        else:
            self.wave = 0.76
            self.bass_steps = 0

    def update_floor_attacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if self.pattern == 1 and not self.wave_hit:
            reach = (0.93 - self.wave) * 475 + 42
            for angle in (-29, 29):
                line = self.aim.rotate(angle)
                if abs(offset.dot(line) - reach) < 31 and abs(offset.cross(line)) < 42 and self.can_reach_player():
                    self.player.take_damage(self.attack)
                    self.wave_hit = True
        elif self.pattern == 2 and not self.wave_hit:
            moved = math.hypot(self.player.x - self.last_breath_position[0], self.player.y - self.last_breath_position[1])
            self.last_breath_position = (self.player.x, self.player.y)
            self.breath_still = self.breath_still + dt if moved < dt * 24 else 0
            if self.breath_still >= 0.38 and offset.length() < 500 and self.can_reach_player():
                self.player.take_damage(self.attack - 7)
                self.wave_hit = True
        elif self.pattern == 4:
            beat = 1 if self.wave > 0.37 else 2
            if self.bass_steps < beat:
                self.bass_steps = beat
                self.move_towards(self.player.x, self.player.y, 0.24, 120)
                if math.hypot(self.player.x - self.x, self.player.y - self.y) < 155 and self.can_reach_player():
                    self.player.take_damage(self.attack - 13)
                self.attack_animation_time = 0.3
        if self.wave == 0:
            self.wave = None

    def draw_wave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        origin = pg.Vector2(x, y)
        if self.pattern == 1:
            reach = (0.93 - value) * 475 + 42
            for angle in (-29, 29):
                direction = self.aim.rotate(angle)
                tip = origin + direction * reach
                pg.draw.line(self.screen, (117, 71, 117), origin, tip, 3)
                pg.draw.circle(self.screen, (219, 194, 237), (round(tip.x), round(tip.y)), 12, 3)
        elif self.pattern == 2:
            px, py = camera.apply(self.player.x, self.player.y)
            if not self.wave_hit:
                pg.draw.arc(self.screen, (217, 190, 234), (px - 29, py - 21, 58, 42), 0, math.tau * min(1, self.breath_still / 0.38), 3)
        elif self.pattern == 4:
            radius = round(92 + (0.76 - value) % 0.38 * 135)
            pg.draw.ellipse(self.screen, (204, 174, 222), (x - radius, y - radius // 2, radius * 2, radius), 3)

    def draw_warning(self, x, y):

        origin = pg.Vector2(x, y)
        color = (212, 184, 229)
        side = self.aim.rotate(90)
        if self.pattern == 0:
            end = origin + self.aim * 245
            if self.windup:
                pg.draw.lines(self.screen, color, False, [origin + side * 28, end + side * 48, end - side * 48, origin - side * 28], 3)
            else:
                pg.draw.polygon(self.screen, (109, 65, 111), [origin + side * 13, end, origin - side * 13])
                pg.draw.line(self.screen, (237, 215, 246), origin, end, 4)
        elif self.pattern == 1:
            for angle in (-29, 29):
                direction = self.aim.rotate(angle)
                for distance in range(58, 475, 38):
                    point = origin + direction * distance
                    pg.draw.line(self.screen, color, point, point + direction * 19, 2)
        elif self.pattern == 2:
            for index in range(3):
                length = 28 + index * 15
                pg.draw.arc(self.screen, (216, 187, 231), (x - length, y - 71 + index * 11, length * 2, 33), 0.15, 2.9, 2)
        elif self.pattern == 3:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if offset.length() < 265 and self.can_reach_player():
                end = origin + offset
                bend = origin.lerp(end, 0.5) + offset.rotate(90) * 0.08
                pg.draw.lines(self.screen, (87, 52, 95), False, [origin, bend, end], 6)
                pg.draw.lines(self.screen, (222, 191, 236), False, [origin, bend, end], 2)
            pg.draw.circle(self.screen, (197, 168, 218), (x, y), 265, 2)
        else:
            pg.draw.ellipse(self.screen, color, (x - 155, y - 77, 310, 154), 2)


class HarpBoss(PianoBoss):

    arena_room = "Harp Chamber"
    region_folder = "HarpReservoir"
    instrument = "Harp"
    home_position = (HARP_ARENA_X, HARP_ARENA_Y)

    def set_stats(self):

        self.max_hp = 1650
        self.current_hp = self.max_hp
        self.attack = 55
        self.size = 87

    def footprint(self):

        return 45, 23, 10

    def teleport_anchor(self):

        for step in range(4):
            side_x, side_y = [(-1, -1), (1, 1), (1, -1), (-1, 1)][(step + self.teleport_index) % 4]
            x = HARP_ARENA_X + side_x * 460
            y = HARP_ARENA_Y + side_y * 375
            if math.hypot(x - self.player.x, y - self.player.y) > 180 and math.hypot(x - self.x, y - self.y) > 180 and self.can_step(x, y):
                return x, y
        return None

    def render_teleport(self, camera):

        for point in (self.teleport_origin, self.teleport_target):
            x, y = camera.apply(*point)
            for offset in (0, 22, 44):
                radius = round(22 + (1 - self.teleport_time) * 75 + offset)
                pg.draw.ellipse(self.screen, (103, 207, 187), (x - radius, y - radius // 2, radius * 2, radius), 2)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Tide Wells", "Crosscurrent", "Plucked Cascade", "Undertow", "Breaking String"][self.pattern]
        self.windup_length = [1.02, 0.92, 0.82, 1.10, 0.98][self.pattern]
        if self.second_phase:
            self.windup_length *= 0.85
        self.windup = self.windup_length
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target + side * shift for shift in (-230, 0, 230)]
        self.lanes = [pg.Rect(HARP_ARENA_X - 600, round(target.y + shift - 44), 1200, 88) for shift in (-205, 0, 205)]
        self.wave_hit = False

    def make_note(self, direction):

        bolt = Projectile(self.screen, self.x, self.y, direction, self.attack - 14)
        bolt.speed = 330
        bolt.size = 14
        bolt.colour = (126, 231, 207)
        return bolt

    def release_attack(self):

        self.strikes += 1
        self.attack_animation_time = 0.3
        self.recovery = 1.55 if self.second_phase else 1.85
        if self.pattern == 2:
            self.volley = [-34, -17, 0, 17, 34]
            self.beat_timer = 0
        elif self.pattern == 3:
            self.wave = 1.0
        else:
            self.wave = 0.34

    def update_floor_attacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if self.pattern == 0:
            hit = any(target.distance_to(point) <= 92 for point in self.chord)
        elif self.pattern == 1:
            hit = any(lane.collidepoint(target.x, target.y) for lane in self.lanes)
        elif self.pattern == 3:
            hit = abs(offset.length() - (570 * self.wave + 52)) <= 26
        else:
            hit = 0 <= offset.dot(self.aim) <= 620 and abs(offset.cross(self.aim)) <= 54
        if hit and not self.wave_hit:
            self.player.take_damage(self.attack)
            self.wave_hit = True
        if self.wave == 0:
            self.wave = None

    def draw_warning(self, x, y):

        if self.windup > 0:
            self.draw_pattern(x, y, (106, 187, 176), 1.0)

    def draw_wave(self, camera, value, color):

        self.draw_pattern(*camera.apply(self.x, self.y), (157, 246, 222), value)

    def draw_pattern(self, x, y, colour, value):

        shift = pg.Vector2(x - self.x, y - self.y)
        origin = pg.Vector2(x, y)
        if self.pattern == 0:
            for point in self.chord:
                center = point + shift
                pg.draw.circle(self.screen, colour, center, 92, 3)
                pg.draw.circle(self.screen, colour, center, 74, 1)
        elif self.pattern == 1:
            for lane in self.lanes:
                pg.draw.rect(self.screen, colour, lane.move(round(shift.x), round(shift.y)), 3)
        elif self.pattern == 2:
            for angle in (-34, -17, 0, 17, 34):
                direction = self.aim.rotate(angle)
                pg.draw.line(self.screen, colour, origin + direction * 85, origin + direction * 225, 2)
        elif self.pattern == 3:
            radius = round(570 * value + 52)
            for edge in (radius - 26, radius, radius + 26):
                pg.draw.circle(self.screen, colour, origin, edge, 4 if edge == radius else 1)
        else:
            side = self.aim.rotate(90) * 54
            end = origin + self.aim * 620
            pg.draw.lines(self.screen, colour, True, [origin + side, end + side, end - side, origin - side], 3)

    def keeper_frame(self):

        if self.teleport_time > 0:
            frame = self.keeper_poses[0].copy()
            frame.set_alpha(round(255 * abs(self.teleport_time - 0.5) * 2))
            return frame
        if self.windup > 0 and self.windup < self.windup_length * 0.73:
            return self.keeper_poses[1]
        if self.attack_animation_time > 0:
            return self.keeper_poses[2 if self.attack_animation_time > 0.085 else 4]
        if self.volley:
            return self.keeper_poses[2 if self.beat_timer > 0.06 else 1]
        if self.encore:
            return self.keeper_poses[1]
        return self.keeper_poses[0]

    def render(self, camera):

        super().render(camera)
        if self.current_hp <= 0 or self.teleport_time > 0:
            return
        if self.attack_animation_time <= 0 and not self.volley:
            return
        progress = 1 - self.attack_animation_time / 0.3 if self.attack_animation_time else 1 - min(1, self.beat_timer / 0.105)
        x, y = camera.apply(self.x, self.y)
        for index in range(5):
            spread = progress * (15 + index * 4)
            px = round(x + 46 + index * 4 + spread)
            py = round(y - 181 + index * 18 - spread * 0.36)
            colour = (164, 242, 219) if progress < 0.55 else (93, 171, 160)
            pg.draw.line(self.screen, colour, (px, py), (px + 4, py - 3), 2)


class ViolinBoss(PianoBoss):

    arena_room = "Performance Hall"
    region_folder = "ViolinHall"
    instrument = "Violin"
    home_position = (10880, 20320)

    def set_stats(self):

        self.max_hp = 1750
        self.current_hp = self.max_hp
        self.attack = 56
        self.size = 65

    def footprint(self):

        return 29, 17, 7

    def teleport_anchor(self):

        for step in range(4):
            dx, dy = [(-470, -340), (470, 340), (470, -340), (-470, 340)][(self.teleport_index + step) % 4]
            x, y = self.home_position[0] + dx, self.home_position[1] + dy
            if math.hypot(x - self.x, y - self.y) > 160 and math.hypot(x - self.player.x, y - self.player.y) > 165 and self.can_step(x, y):
                return x, y
        return None

    def render_teleport(self, camera):

        for point in (self.teleport_origin, self.teleport_target):
            x, y = camera.apply(*point)
            progress = 1 - abs(2 * self.teleport_time - 1)
            for offset in (-24, 0, 24):
                height = round(20 + 95 * progress)
                pg.draw.line(self.screen, (208, 151, 177), (x + offset, y), (x + offset, y - height), 2)

    def start_phrase(self):

        self.pattern = self.strikes % 5
        self.move_name = ["Bow Cut", "Crossed Strings", "Three Marks", "Pinch", "Final Rest"][self.pattern]
        self.windup_length = [0.79, 0.98, 0.89, 1.04, 1.12][self.pattern]
        if self.second_phase:
            self.windup_length *= 0.85
        self.windup = self.windup_length
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target - side * 168, target, target + side * 168]
        self.wave_hit = False

    def release_attack(self):

        self.strikes += 1
        self.attack_animation_time = 0.3
        self.recovery = 1.5 if self.second_phase else 1.8
        self.wave = 0.78 if self.pattern in (2, 3) else 0.32

    def string_lines(self, value):

        if self.pattern == 0:
            return [(pg.Vector2(self.x, self.y), self.aim, 400, 32)]
        if self.pattern == 1:
            return [(self.chord[1], self.aim.rotate(angle), 470, 29) for angle in (-39, 39)]
        side = self.aim.rotate(90)
        gap = 54 + round(138 * value / 0.78)
        return [(self.chord[1] + side * offset, self.aim, 490, 28) for offset in (-gap, gap)]

    def update_floor_attacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        point = pg.Vector2(self.player.x, self.player.y)
        if self.pattern == 2:
            index = min(2, int((0.78 - self.wave) / 0.26))
            hit = point.distance_to(self.chord[index]) <= 76
        elif self.pattern == 4:
            hit = 145 <= point.distance_to((self.x, self.y)) <= 425
        else:
            hit = False
            for origin, direction, length, width in self.string_lines(self.wave):
                offset = point - origin
                start = 0 if self.pattern == 0 else -length
                if start <= offset.dot(direction) <= length and abs(offset.cross(direction)) <= width:
                    hit = True
        if hit and not self.wave_hit:
            self.player.take_damage(self.attack)
            self.wave_hit = True
        if self.wave == 0:
            self.wave = None

    def draw_warning(self, x, y):

        if self.windup > 0:
            self.draw_strings(x, y, (186, 145, 175), 0.78, True)

    def draw_wave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        self.draw_strings(x, y, (236, 188, 207), value, False)

    def draw_strings(self, x, y, colour, value, warning):

        shift = pg.Vector2(x - self.x, y - self.y)
        if self.pattern == 2:
            index = min(2, int((0.78 - value) / 0.26))
            marks = self.chord if warning else [self.chord[index]]
            for point in marks:
                pg.draw.circle(self.screen, colour, point + shift, 76, 3)
                if not warning:
                    pg.draw.circle(self.screen, colour, point + shift, 61, 2)
        elif self.pattern == 4:
            for radius in (145, 425):
                pg.draw.circle(self.screen, colour, (x, y), radius, 3)
            if not warning:
                pg.draw.circle(self.screen, colour, (x, y), round(145 + 280 * value / 0.32), 2)
        else:
            for point, direction, length, width in self.string_lines(value):
                point = point + shift
                start = point if self.pattern == 0 else point - direction * length
                end = point + direction * length
                side = direction.rotate(90) * width
                pg.draw.lines(self.screen, colour, True, [start - side, end - side, end + side, start + side], 2)
                if not warning:
                    pg.draw.line(self.screen, colour, start, end, 4)
            if self.pattern == 3 and warning:
                for point, direction, length, width in self.string_lines(0):
                    start = point + shift - direction * length
                    pg.draw.line(self.screen, colour, start, start + direction * length * 2, 1)

    def keeper_frame(self):

        if self.teleport_time:
            frame = self.keeper_poses[0].copy()
            frame.set_alpha(round(510 * abs(self.teleport_time - 0.5)))
            return frame
        index = 0
        if self.windup > 0:
            progress = 1 - self.windup / self.windup_length
            if progress >= 0.22:
                index = 1
        elif self.attack_animation_time > 0:
            index = 2 if self.attack_animation_time >= 0.10 else 1
        elif self.encore > 0:
            index = 1
        frame = self.keeper_poses[index]
        return pg.transform.flip(frame, True, False) if self.aim.x < 0 else frame

    def render(self, camera):

        super().render(camera)
        if self.current_hp <= 0 or self.teleport_time > 0 or self.attack_animation_time <= 0.10:
            return
        progress = 1 - self.attack_animation_time / 0.3
        x, y = camera.apply(self.x, self.y)
        offset_x, offset_y = boss_pose_offset(self)
        x += offset_x
        y += offset_y
        side = -1 if self.aim.x < 0 else 1
        reach = round(20 * progress)
        colour = (217, 170, 185) if progress < 0.38 else (156, 111, 144)
        start = (x + side * (31 + reach), y - 105 + reach // 2)
        middle = (x + side * (47 + reach), y - 97 + reach)
        end = (x + side * (59 + reach), y - 86 + reach)
        pg.draw.lines(self.screen, colour, False, [start, middle, end], 2)
