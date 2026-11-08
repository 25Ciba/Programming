import math
import pygame as pg
from pathlib import Path
from Items import ITEMS, START_WEAPON, draw_hand

DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


def colour_robe(body, robe):

    for y in range(body.get_height()):
        for x in range(body.get_width()):
            red, green, blue, alpha = body.get_at((x, y))
            if alpha and blue > red + 6 and red > green + 5:
                strength = (red + green + blue) / 385
                body.set_at((x,y), (*[min(255,round(channel*strength)) for channel in robe], alpha))
    return body


class RogueArt:

    def __init__(self, robe=None, character='Male'):

        self.weapon = START_WEAPON
        self.bodies = []
        self.poses = []
        self.breathing = []
        self.soft_steps = []
        self.attacks = []
        self.return_cuts = []
        folder = Path(__file__).resolve().parent / "Images" / "Characters" / "Rogue" / "Directional"
        for i, (dx, dy) in enumerate(DIRECTIONS):
            body = pg.image.load(folder / f"Rogue_{i}.png").convert_alpha()
            if robe:
                colour_robe(body, robe)
            if character == "Female" and dy >= 0:
                center = body.get_width() // 2
                y = body.get_height() - 12
                pg.draw.rect(body,(220,171,130),(center-1,y,2,2))
                pg.draw.rect(body,(156,108,144),(center-2,y+2,4,2))
            self.bodies.append(body)
            steps = []
            for level in range(5):
                frames = []
                for frame in range(16):
                    phase = frame * math.tau / 16
                    stride = round(math.sin(phase) * level)
                    bob = round((1 - math.cos(phase * 2)) * level / 8)
                    frames.append(self.make_pose(body, dx, dy, stride, bob, lean=False))
                steps.append(frames)
            self.soft_steps.append(steps)
            idle = steps[0][0]
            self.breathing.append([idle, self.make_pose(body, dx, dy, 0, 1, lean=False), self.make_pose(body, dx, dy, 0, 2, lean=False)])
            frames = steps[4]
            crouch = self.make_pose(body, dx, dy, 0, 3)
            glide = self.make_pose(body, dx, dy, 2, 1)
            self.poses.append((idle, frames, crouch, glide))
            attack_frames = []
            return_frames = []
            for frame in range(24):
                progress = frame / 23
                attack_frames.append(self.make_attack(body, dx, dy, progress, 1))
                return_frames.append(self.make_attack(body, dx, dy, progress, -1))
            self.attacks.append(attack_frames)
            self.return_cuts.append(return_frames)

    def equip_weapon(self, name):

        if self.weapon == name:
            return
        self.weapon = name
        for index, (dx, dy) in enumerate(DIRECTIONS):
            body = self.bodies[index]
            self.attacks[index] = [self.make_attack(body, dx, dy, frame / 23, 1) for frame in range(24)]
            self.return_cuts[index] = [self.make_attack(body, dx, dy, frame / 23, -1) for frame in range(24)]

    def held_gear(self, frame, facing, weapon, shield, blocking=False):

        forward = pg.Vector2(DIRECTIONS[facing]).normalize()
        side = forward.rotate(90)
        center = pg.Vector2(frame.get_width() / 2, frame.get_height() / 2 + (15 if weapon else -13))
        main = pg.Surface(frame.get_size(), pg.SRCALPHA)
        offhand = pg.Surface(frame.get_size(), pg.SRCALPHA)
        if weapon:
            grip = center + side * 15 + forward * 3
            draw_hand(main, grip, forward, weapon, 1.45)
        if shield:
            grip = center - side * (12 if blocking else 16) + forward * (13 if blocking else 1)
            draw_hand(offhand, grip, forward, shield, 1.28)
        result = pg.Surface(frame.get_size(), pg.SRCALPHA)
        main_behind = forward.y < 0 or (forward.y == 0 and forward.x < 0)
        offhand_behind = not blocking and (forward.y < 0 or forward.x > 0)
        if main_behind:
            result.blit(main, (0, 0))
        if offhand_behind:
            result.blit(offhand, (0, 0))
        result.blit(frame, (0, 0))
        if not main_behind:
            result.blit(main, (0, 0))
        if not offhand_behind:
            result.blit(offhand, (0, 0))
        return result

    def make_pose(self, body, dx, dy, stride, crouch, lean=True):

        sprite = pg.Surface((48, 48), pg.SRCALPHA)
        x = (48 - body.get_width()) // 2
        y = 43 - body.get_height()
        feet_y = body.get_height() - 6
        top = body.subsurface((0, 0, body.get_width(), feet_y + 2))
        if crouch:
            top = pg.transform.scale(top, (top.get_width(), top.get_height() - crouch))
        half = body.get_width() // 2
        for left, width, side in [(0, half, -1), (half, body.get_width() - half, 1)]:
            step_x = (stride * side) // 2 if dx else 0
            step_y = (stride * side) // 2 if dy else abs(stride) // 2
            sprite.blit(body, (x + left + step_x, y + feet_y - 2 + step_y), (left, feet_y - 2, width, 8))
        sprite.blit(top, (x + (dx if crouch and lean else 0), y + crouch))
        return pg.transform.scale(sprite, (96, 96))

    def movement_frame(self, facing, distance, stride, idle_time):

        level = round(stride * 4)
        if level > 0:
            step = int(distance / 19) % 16
            return self.soft_steps[facing][level][step]
        # Ease through three breathing poses without shifting the boots.
        breath = round(1 - math.cos(idle_time * math.tau / 2.6))
        return self.breathing[facing][breath]

    def attack_pose(self, progress):

        # Time, forward lean, sideways twist, blade angle, blade reach.
        poses = [
            (0.00, 0, 0, -0.55, 22),
            (0.23, -7, -7, -1.58, 35),
            (0.42, 12, -2, -0.38, 70),
            (0.57, 15, 9, 0.95, 66),
            (0.75, 7, 5, 1.36, 43),
            (1.00, 0, 0, 1.10, 22)
        ]
        for first, second in zip(poses, poses[1:]):
            if progress <= second[0]:
                fraction = (progress - first[0]) / (second[0] - first[0])
                fraction = fraction * fraction * (3 - 2 * fraction)
                return [a + (b - a) * fraction for a, b in zip(first[1:], second[1:])]
        return poses[-1][1:]

    def weapon_pose(self, forward, progress, sweep):

        lean, twist, blade_angle, reach = self.attack_pose(progress)
        side = pg.Vector2(-forward.y, forward.x)
        shoulder = pg.Vector2(72, 64) + forward * lean * 0.45 + side * (twist * 0.5 + 5)
        blade = forward.rotate_rad(blade_angle * sweep)
        hand = shoulder + blade * 8 + side * 2
        tip = hand + blade * reach * 0.52
        # Keep the curved blade tip inside the sweep's outer edge.
        edge_center = pg.Vector2(72, 65)
        blade_side = blade.rotate(90)
        minimum = 0
        maximum = hand.distance_to(tip)
        for _ in range(8):
            distance = (minimum + maximum) / 2
            point = hand + blade * distance - blade_side * 3 - edge_center
            along = max(0, point.dot(forward) - 15) / 32
            across = point.dot(side) / 25
            if along * along + across * across <= 1:
                minimum = distance
            else:
                maximum = distance
        return shoulder, hand, hand + blade * minimum

    def make_attack(self, body, dx, dy, progress, sweep):

        forward = pg.Vector2(dx, dy).normalize()
        lean, twist, blade_angle, reach = self.attack_pose(progress)
        if ITEMS[self.weapon][1] in ("Focus", "Bow"):
            lean = round(math.sin(progress * math.pi) * 5)
        frame = pg.Surface((144, 144), pg.SRCALPHA)
        stance = self.make_pose(body, dx, dy, round(lean / 5), round(max(0, -lean) / 3))
        stance = pg.transform.scale(stance, (48, 48))
        shift = forward * lean * 0.45
        stance_rect = stance.get_rect(center=(round(72 + shift.x), round(60 + shift.y)))
        if dy < 0:
            self.draw_weapon(frame, forward, progress, sweep)
            frame.blit(stance, stance_rect)
        else:
            frame.blit(stance, stance_rect)
            self.draw_weapon(frame, forward, progress, sweep)
        return pg.transform.scale(frame, (288, 288))

    def draw_horseshoe(self, frame, forward, progress, sweep):

        if progress < 0.30 or progress > 0.78:
            return
        side = pg.Vector2(-forward.y, forward.x) * sweep
        center = pg.Vector2(72, 65)
        strength = min(1, (progress - 0.30) / 0.10, (0.78 - progress) / 0.20)
        extent = 1.52 + min(0.34, (progress - 0.30) * 2)
        outer = []
        inner = []
        edge = []
        for point in range(25):
            part = point / 24
            angle = (part * 2 - 1) * extent
            length = 15 + math.cos(angle) * 33
            width = math.sin(part * math.pi) ** 1.5 * 7
            tail = side * math.sin(angle) * 26
            outer.append(center + forward * length + tail)
            inner.append(center + forward * (length - width) + tail * (1 - width / 70))
            edge.append(center + forward * (length - width * 0.42) + tail * (1 - width / 130))
        pg.draw.polygon(frame, (117, 129, 175, round(190 * strength)), outer + inner[::-1])
        pg.draw.polygon(frame, (225, 232, 245, round(245 * strength)), outer + edge[::-1])

    def draw_weapon(self, frame, forward, progress, sweep):

        form = ITEMS[self.weapon][1]
        if form in ("Focus", "Bow"):
            side = forward.rotate(90)
            extension = math.sin(progress * math.pi) * 8
            shoulder = pg.Vector2(72, 64) + side * 5
            hand = shoulder + forward * (6 + extension)
            pg.draw.line(frame, (79, 58, 104), shoulder, hand, 4)
            draw_hand(frame, hand, forward, self.weapon)
            return
        shoulder, hand, tip = self.weapon_pose(forward, progress, sweep)
        self.draw_horseshoe(frame, forward, progress, sweep)
        pg.draw.line(frame, (79, 58, 104), shoulder, hand, 4)
        direction = tip - hand
        if direction.length_squared():
            draw_hand(frame, hand, direction, self.weapon, min(1, direction.length() / 24))

    def guard(self, screen, x, y, direction, progress):

        # A compact parry flash, drawn at the same pixel scale as the Rogue.
        effect = pg.Surface((80, 80), pg.SRCALPHA)
        side = pg.Vector2(-direction.y, direction.x)
        center = pg.Vector2(40, 37) + direction * 17
        strength = max(0, 1 - progress)
        size = 0.65 + min(0.35, progress * 2)
        points = []
        for forward, across in [(0, -13), (7, -8), (10, 0), (7, 8), (0, 13), (3, 4), (3, -4)]:
            points.append(center + (direction * forward + side * across) * size)
        pg.draw.polygon(effect, (54, 67, 102, round(145 * strength)), points)
        pg.draw.lines(effect, (188, 211, 232, round(245 * strength)), False, points[:5], 2)
        for offset in (-1, 1):
            point = center + side * offset * (12 + progress * 8) + direction * (6 + progress * 8)
            pg.draw.rect(effect, (238, 232, 190, round(220 * strength)), (round(point.x), round(point.y), 2, 2))
        screen.blit(pg.transform.scale(effect, (160, 160)), (x - 80, y - 80))

