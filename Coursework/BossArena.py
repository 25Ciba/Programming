import math
import pygame as pg
from Ruins import RuinsProp

# Arena name, passage centre, and door orientation.
ARENA_DOORS = [
    ("Overture Arena", 12245, 10880, True, 1),
    ("Overture Arena", 14390, 10880, True, -1),
    ("Piano Chamber", 10880, 2780, False, -1),
    ("Piano Chamber", 13155, 1600, True, -1),
    ("Resonance Arena", 2275, 10880, True, -1),
    ("Flute Hall", 19335, 10880, True, 1),
    ("Flute Hall", 20160, 9580, False, 1),
    ("Cello Amphitheatre", 3840, 19222, False, 1),
    ("Harp Chamber", 17920, 19150, False, 1),
    ("Performance Hall", 10880, 19105, False, 1)
]

PALETTES = [
    ("Overture Arena", (65, 70, 93), (185, 149, 89)),
    ("Piano Chamber", (49, 83, 115), (157, 224, 236)),
    ("Resonance Arena", (99, 57, 52), (230, 151, 75)),
    ("Flute Hall", (78, 106, 106), (174, 219, 202)),
    ("Cello Amphitheatre", (99, 67, 63), (219, 162, 112)),
    ("Harp Chamber", (34, 79, 83), (128, 208, 183)),
    ("Performance Hall", (85, 46, 71), (218, 162, 130))
]

DOOR_STORIES = [
    ("Overture Arena", "Overture Keeper", "Forkblade", "The Keeper has heard your footsteps. It is waiting for the downbeat.", "I counted three blows. On the fourth beat the Keeper went still. I wish I had known the silence was my turn."),
    ("Piano Chamber", "Piano Ultra Boss", "Ivory Sword", "The pianist saved the last note for whoever opens this door.", "The last key fell silent, but its note was still moving through the room. I stepped back into it."),
    ("Resonance Arena", "Guitar Ultra Boss", "Fretblade", "Six strings are humming beyond the door. The last challenger only heard five.", "He laid his palm across the strings. I mistook the silence for surrender. My blade is still where it fell."),
    ("Flute Hall", "Flute Ultra Boss", "Silver Reed", "The hall has been holding its breath. Will you be the one to break the silence?", "I heard him take a breath. The curtains moved first. I should have followed them."),
    ("Cello Amphitheatre", "Cello Ultra Boss", "Broken Bowblade", "The cellist has drawn the bow. The stone is waiting for the first stroke.", "I thought the bow had stopped. Then I felt the note in the floor beneath my boots."),
    ("Harp Chamber", "Harp Ultra Boss", "Tidehook", "The strings are taut beneath the water. Will you break the surface?", "Five strings rang. I saw the sixth trembling and stepped between the ripples."),
    ("Performance Hall", "Violin Ultra Boss", "Splintered Bow", "The final performer waits in silence. Will you take your place?", "I watched the bow instead of the floor. By the time I looked down, the strings were already crossing.")
]

# Centre x/y, offset to each wall's centre, width and height.
# Each pair creates side alcoves while leaving the middle passage open.
PARTITIONS = [
    (10880, 11395, 585, 210, 62, 64),
    (10880, 10050, 720, 235, 64, 66),
    (8640, 11270, 390, 150, 62, 64),
    (10880, 13170, 450, 142, 58, 62),
    (10880, 3470, 870, 222, 65, 62),
    (10880, 4290, 910, 205, 64, 62),
    (10880, 6060, 420, 160, 64, 62),
    (3840, 11400, 690, 228, 66, 62),
    (3840, 10170, 670, 220, 62, 62),
    (6080, 11045, 280, 88, 58, 58),
    (3840, 13055, 520, 138, 63, 62),
    (17920, 10410, 770, 192, 62, 63),
    (17920, 11180, 770, 192, 62, 63),
    (17920, 13035, 440, 125, 55, 58),
    (3840, 17260, 855, 196, 62, 62),
    (3840, 18180, 855, 196, 62, 62),
    (1600, 18070, 450, 125, 55, 60)
]


ALCOVE_RETURNS = [
    (10880, 11710, 690, 58, 188),
    (10880, 10210, 805, 58, 160),
    (8640, 11355, 466, 58, 142),
    (10880, 4480, 1020, 60, 185),
    (10880, 3625, 970, 60, 187),
    (3840, 11720, 785, 58, 190),
    (3840, 10410, 755, 58, 190),
    (3840, 13240, 590, 54, 176),
    (17920, 10700, 860, 58, 185),
    (17920, 11400, 860, 58, 172),
    (3840, 17550, 935, 58, 170),
    (3840, 18470, 935, 58, 170),
    (10880, 17560, 790, 58, 235),
    (10880, 18300, 790, 58, 235)
]


class ArenaDoor:

    def __init__(self, name, x, y, vertical, inside, folder):

        self.name = name
        self.x = x
        self.y = y
        self.vertical = vertical
        self.inside = inside
        self.allowed = False
        self.cleared = False
        for arena, boss_name, relic_name, challenge, inscription in DOOR_STORIES:
            if arena == name:
                self.boss_name = boss_name
                self.relic_name = relic_name
                self.challenge = challenge
                self.inscription = inscription
        sprite = pg.image.load(folder / f"{self.relic_name}.png").convert_alpha()
        width = round(sprite.get_width() * 84 / sprite.get_height())
        sprite = pg.transform.scale(sprite, (width, 84))
        relic_x = x - 166 * inside if vertical else x + 125
        relic_y = y + 125 if vertical else y - 166 * inside
        self.relic = RuinsProp(relic_x, relic_y, 24, sprite)
        self.note_x = relic_x - 29
        self.note_y = relic_y + 27
        self.half_opening = 216
        self.progress = 0
        self.hold = 0
        for arena, stone, metal in PALETTES:
            if arena == name:
                self.stone = stone
                self.metal = metal
        self.panel = pg.Surface((self.half_opening, 60), pg.SRCALPHA)
        self.panel.fill((29, 30, 46))
        pg.draw.rect(self.panel, self.stone, (0, 6, self.half_opening, 47))
        for x_line in range(10, self.half_opening - 2, 14):
            pg.draw.rect(self.panel, (37, 39, 54), (x_line, 12, 7, 35))
            pg.draw.rect(self.panel, self.metal, (x_line, 16, 3, 25))
        pg.draw.rect(self.panel, self.metal, (0, 5, self.half_opening, 4))
        pg.draw.rect(self.panel, self.metal, (0, 48, self.half_opening, 4))
        if name == "Piano Chamber":
            for x_line in range(6, self.half_opening - 5, 16):
                pg.draw.rect(self.panel, (220, 228, 226), (x_line, 31, 11, 16))
                pg.draw.rect(self.panel, (27, 38, 57), (x_line + 6, 29, 6, 10))
        elif name == "Resonance Arena":
            for y_line in range(18, 43, 5):
                pg.draw.line(self.panel, self.metal, (4, y_line), (self.half_opening - 5, y_line), 2)
        elif name == "Performance Hall":
            pg.draw.lines(self.panel, self.metal, False, [(86, 13), (76, 23), (83, 30), (76, 39), (91, 46), (106, 39), (99, 30), (106, 23), (96, 13)], 3)
            for string in (88, 92, 96):
                pg.draw.line(self.panel, (230, 177, 153), (string, 15), (string, 40), 1)
        elif name == "Harp Chamber":
            for x_line in range(76, 144, 12):
                pg.draw.line(self.panel, self.metal, (x_line, 13), (x_line, 45), 2)
            pg.draw.arc(self.panel, self.metal, (64, 6, 92, 48), math.pi, math.tau, 4)
        elif name == "Cello Amphitheatre":
            for y_line in (21, 26, 31, 36):
                pg.draw.line(self.panel, self.metal, (11, y_line), (self.half_opening - 11, y_line), 2)
            pg.draw.arc(self.panel, (232, 184, 123), (70, 12, 76, 37), 0.15, 3.0, 4)
        elif name == "Flute Hall":
            pg.draw.line(self.panel, self.metal, (18, 29), (self.half_opening - 18, 29), 5)
            for x_line in range(32, self.half_opening - 20, 21):
                pg.draw.circle(self.panel, (35, 47, 61), (x_line, 29), 3)
        else:
            pg.draw.lines(self.panel, self.metal, False, [(63, 16), (63, 30), (78, 36), (93, 30), (93, 16)], 3)
            pg.draw.line(self.panel, self.metal, (78, 34), (78, 44), 3)

    def update(self, dt, player):

        along, across = self.relative(player.x, player.y)
        nearby = abs(along) < 238 and abs(across) < 273
        inside = along * self.inside > 0
        if inside or not nearby:
            self.allowed = False
        if nearby and (inside or self.allowed or self.cleared):
            self.hold = 0.45
        else:
            self.hold = max(0, self.hold - dt)
        if self.hold > 0:
            self.progress = min(1, self.progress + dt * 2.8)
        else:
            self.progress = max(0, self.progress - dt * 2.1)

    def wants_confirmation(self, player):

        along, across = self.relative(player.x, player.y)
        return -220 < along * self.inside <= 0 and abs(across) < 190 and not self.allowed and not self.cleared

    def relic_near(self, player):

        return math.hypot(self.note_x - player.x, self.note_y - player.y) < 90

    def allows_crossing(self, player, x, y):

        start, _ = self.relative(player.x, player.y)
        end, across = self.relative(x, y)
        if abs(across) >= 290 or not (start * self.inside <= 0 < end * self.inside):
            return True
        return self.allowed or self.cleared

    def relative(self, x, y):

        if self.vertical:
            return x - self.x, y - self.y
        return y - self.y, x - self.x

    def blocks(self, x, y, radius):

        along, across = self.relative(x, y)
        if abs(along) > 14 + radius or abs(across) >= 290 + radius:
            return False
        # The frame fills the corridor. The panels retract into its sides.
        return abs(across) + radius >= self.half_opening * self.progress

    def render_note(self, screen, camera):

        x, y = camera.apply(self.note_x, self.note_y)
        pg.draw.ellipse(screen, (24, 25, 38), (x - 11, y - 2, 25, 13))
        pg.draw.polygon(screen, (205, 171, 126), [(x - 10, y - 7), (x + 9, y - 9), (x + 13, y + 4), (x - 7, y + 8)])
        for offset in (-4, 0, 4):
            pg.draw.line(screen, (108, 78, 69), (x - 5, y + offset), (x + 6, y + offset - 2), 1)

    def render(self, screen, camera):

        x, y = camera.apply(self.x, self.y)
        if not screen.get_rect().inflate(620, 620).collidepoint(x, y):
            return
        door = pg.Surface((576, 68), pg.SRCALPHA)
        left_edge = 288 - self.half_opening
        right_edge = 288 + self.half_opening
        for side in (0, right_edge):
            pg.draw.rect(door, (27, 27, 41), (side, 4, left_edge, 60))
            for offset in range(4, left_edge - 18, 26):
                pg.draw.rect(door, self.stone, (side + offset, 10, 22, 45))
                pg.draw.rect(door, (122, 116, 128), (side + offset, 10, 21, 4))
        amount = round(self.half_opening * (1 - self.progress))
        if amount:
            door.blit(self.panel, (left_edge, 4), (self.half_opening - amount, 0, amount, 60))
            right = pg.transform.flip(self.panel, True, False)
            door.blit(right, (right_edge - amount, 4), (0, 0, amount, 60))
        for post in (left_edge, right_edge):
            pg.draw.rect(door, (23, 25, 39), (post - 11, 1, 22, 65))
            pg.draw.rect(door, self.stone, (post - 8, 4, 16, 56))
            pg.draw.rect(door, self.metal, (post - 5, 9, 10, 11))
            pg.draw.rect(door, self.metal, (post - 5, 47, 10, 7))
        if self.vertical:
            door = pg.transform.rotate(door, 90)
        screen.blit(door, door.get_rect(center=(x, y)))


class ArenaArt:

    def __init__(self, rooms, image_folder):

        folder = image_folder / "ArenaRelics"
        self.doors = [ArenaDoor(name, x, y, vertical, inside, folder) for name, x, y, vertical, inside in ARENA_DOORS]
        self.relics = [door.relic for door in self.doors]
        self.rooms = [(name, rect) for name, region, rect in rooms if any(name == arena for arena, _, _ in PALETTES)]
        self.partitions = []
        for x, y, offset_x, offset_y, width, height in PARTITIONS:
            for side in (-1, 1):
                rect = pg.Rect(0, 0, width, height)
                rect.center = (x + side * offset_x, y + offset_y)
                self.partitions.append(rect)
        for x, y, offset, width, height in ALCOVE_RETURNS:
            for side in (-1, 1):
                rect = pg.Rect(0, 0, width, height)
                rect.center = (x + side * offset, y)
                self.partitions.append(rect)
        self.lights = []
        for name, stone, metal in PALETTES:
            light = pg.Surface((600, 440), pg.SRCALPHA)
            for radius in range(215, 16, -5):
                strength = round(45 * (1 - radius / 220) ** 1.4)
                pg.draw.ellipse(light, (*metal, strength), (300 - radius * 1.35, 220 - radius, radius * 2.7, radius * 2))
            self.lights.append(light)
        self.fog_mask = None
        self.revealed_room = None
        self.reveal = 0

    def update(self, dt, player, enemies=None):

        for door in self.doors:
            if enemies is not None:
                door.cleared = not any(enemy.name == door.boss_name and enemy.current_hp > 0 for enemy in enemies)
            door.update(dt, player)
        for name, rect in self.rooms:
            if rect.inflate(100, 100).collidepoint(player.x, player.y):
                self.revealed_room = name
                self.reveal = min(1, self.reveal + dt * 2)
                return
        self.reveal = max(0, self.reveal - dt * 2)

    def nearby_action(self, player):

        for door in self.doors:
            if door.relic_near(player):
                return door, False
        for door in self.doors:
            if door.wants_confirmation(player):
                return door, True
        return None

    def allows_crossing(self, player, x, y):

        for door in self.doors:
            if not door.allows_crossing(player, x, y):
                return False
        return True

    def blocks(self, x, y, radius):

        for door in self.doors:
            if door.blocks(x, y, radius):
                return True
        for rect in self.partitions:
            if rect.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def reveal_fog(self, fog, camera, room_floors):

        if self.reveal <= 0:
            return
        opacity = round(240 * (1 - self.reveal))
        # Reveal only the arena's actual floor shape, not the neighbouring tunnels.
        if self.fog_mask is None or self.fog_mask.get_size() != fog.get_size():
            self.fog_mask = pg.Surface(fog.get_size(), pg.SRCALPHA)
        mask = self.fog_mask
        mask.fill((255, 255, 255, 255))
        for name, region, rect in room_floors:
            if name == self.revealed_room:
                pg.draw.rect(mask, (255, 255, 255, opacity), pg.Rect(camera.apply(rect.x, rect.y), rect.size))
        fog.blit(mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)

    def hide_beyond_doors(self, fog, camera, player):

        view = fog.get_rect()
        for door in self.doors:
            along, across = door.relative(player.x, player.y)
            if abs(along) > 450 or abs(across) > 320:
                continue
            x, y = camera.apply(door.x, door.y)
            if door.vertical:
                edge = x + 24 if along <= 0 else x - 24
                if along <= 0:
                    hidden = pg.Rect(edge, 0, max(0, view.width - edge), view.height)
                else:
                    hidden = pg.Rect(0, 0, max(0, edge), view.height)
            else:
                edge = y + 24 if along <= 0 else y - 24
                if along <= 0:
                    hidden = pg.Rect(0, edge, view.width, max(0, view.height - edge))
                else:
                    hidden = pg.Rect(0, 0, view.width, max(0, edge))
            fog.fill((11, 14, 24, 255), view.clip(hidden))

    def render(self, screen, camera):

        view = screen.get_rect()
        for rect in self.partitions:
            face = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if not view.colliderect(face):
                continue
            pg.draw.rect(screen, (25, 25, 39), face.move(7, 9))
            pg.draw.rect(screen, (57, 56, 75), face)
            for course in range(3):
                y = face.y + course * 16
                for offset in range(-12 * (course % 2), face.width, 26):
                    left = max(0, offset)
                    width = min(face.width, offset + 24) - left
                    if width > 0:
                        pg.draw.rect(screen, (83 + course * 3, 80 + course * 3, 103 + course * 2), (face.x + left, y, width, 13))
                        pg.draw.line(screen, (117, 113, 133), (face.x + left, y), (face.x + left + width - 1, y), 2)
            pg.draw.line(screen, (42, 41, 59), (face.left, face.bottom - 3), (face.right - 1, face.bottom - 3), 5)
        ticks = pg.time.get_ticks() / 1000
        for name, room in self.rooms:
            region = next(i for i, values in enumerate(PALETTES) if values[0] == name)
            stone, metal = PALETTES[region][1:]
            x, y = camera.apply(*room.center)
            if not view.colliderect((x - 950, y - 770, 1900, 1540)):
                continue
            light = self.lights[region]
            for dx, dy in [(-395, -260), (395, -260), (-395, 260), (395, 260)]:
                screen.blit(light, light.get_rect(center=(x + dx, y + dy)))
            for i in range(44):
                dx = (i * 157) % 1200 - 600
                dy = (i * 91 - round(ticks * (8 + i % 6))) % 850 - 425
                px = x + dx + round(math.sin(ticks + i) * 9)
                py = y + dy
                color = metal if i % 6 == 0 else stone
                pg.draw.rect(screen, color, (px, py, 2, 2))
        for door in self.doors:
            door.render(screen, camera)
            door.render_note(screen, camera)
