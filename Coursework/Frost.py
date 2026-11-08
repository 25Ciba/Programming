import pygame as pg
import math
from Ruins import RuinsArt, RuinsProp

# Name, position, artwork index, and width of the solid base.
LAKE_X = 10880
LAKE_Y = 3840
ARENA_X = 10880
ARENA_Y = 1500
PIANO_Y = 470
CHAMBER_NORTH = 120
LAKE_WIDTH = 920
LAKE_HEIGHT = 560

# Pairs share an axis. The lake and piano are single central landmarks.
FROST_PROPS = [
    ("Frozen grand piano", 10880, PIANO_Y, 0, 300)
]
FROST_PAIRS = [
    (10880, 5900, 300, 1, 112), (10880, 6230, 285, 2, 65),
    (10880, 3230, 440, 1, 138), (10880, 3340, 665, 2, 76),
    (10880, 3840, 655, 2, 72), (10880, 4230, 520, 1, 122),
    (10880, 4460, 590, 2, 68),
    (8640, 3530, 270, 1, 106), (8640, 4170, 245, 2, 62),
    (13120, 3420, 295, 1, 110), (13120, 4250, 300, 2, 65),
    (10880, 710, 535, 2, 88), (10880, 1160, 1220, 1, 190),
    (10880, 1930, 1180, 1, 178), (10880, 2230, 635, 2, 92)
]
for center, y, offset, index, width in FROST_PAIRS:
    for side in (-1, 1):
        name = "Ice cluster" if index == 1 else "Frost lantern"
        FROST_PROPS.append((name, center + side * offset, y, index, width))

FROST_HABITATS = [
    ("Rime Beetle", "Common", 10250, 3650),
    ("Rime Beetle", "Common", 10350, 3540),
    ("Glasswing Moth", "Strong", 10440, 3660),
    ("Rime Beetle", "Common", 11580, 4110),
    ("Rime Beetle", "Common", 11710, 4020),
    ("Glasswing Moth", "Strong", 11680, 4230),
    ("Glasswing Moth", "Strong", 8470, 3940),
    ("Rime Beetle", "Common", 8530, 4040),
    ("Rime Beetle", "Common", 12800, 3720),
    ("Glasswing Moth", "Strong", 12920, 3940),
    ("Glasswing Moth", "Strong", 11310, 6020),
    ("Rime Beetle", "Common", 11280, 6150)
]

EXTRA_LANDMARKS = [
    ("Music stand", 10145, 4460, 1, 74),
    ("Metronome", 11615, 4460, 3, 74),
    ("Key crates", 13310, 3810, 2, 105),
    ("Key crates", 12930, 3810, 2, 105),
    ("Music stand", 8820, 3780, 1, 72),
    ("Music stand", 8460, 3780, 1, 72)
]

FROST_NOTES = [
    (10880, 6120, "Read the frost marker", "The thaw never reached the court. Keep to the stones where the snow has worn away."),
    (10880, 4225, "Read the court register", "The pianist played through the first snowfall. By morning, the keys were frozen in place."),
    (8640, 3840, "Inspect the tuning ledger", "One ivory key is missing. Someone marked it as a keepsake."),
    (13120, 3840, "Read the practice markings", "Soft notes first. Let the last chord finish before you move."),
    (10880, 595, "Inspect the frozen piano", "A single key still gives. The note hangs in the air long after your hand leaves it."),
    (10145, 4360, "Read the frozen score", "The last bar has been crossed out. The pianist wanted a longer silence."),
    (11615, 4360, "Tap the frozen metronome", "It ticks once, then the pendulum freezes again."),
    (13310, 3920, "Search the key crates", "Several keys are numbered in chalk. A narrow compartment lies empty."),
    (8820, 3890, "Read the chapel music", "Hold the quiet notes. The moths gather when the room is still.")
]


class FrostArt(RuinsArt):

    def __init__(self, image_folder, ruins_art):

        folder = image_folder / "FrostPiano"
        self.arena_inlay = pg.image.load(folder / "RecitalInlay.png").convert_alpha()
        inlay_height = round(self.arena_inlay.get_height() * 1540 / self.arena_inlay.get_width())
        self.arena_inlay = pg.transform.scale(self.arena_inlay, (1540, min(810, inlay_height)))
        self.arena_light = pg.Surface((1660, 940), pg.SRCALPHA)
        for radius in range(295, 24, -5):
            alpha = round(41 * (1 - radius / 300) ** 1.45)
            pg.draw.ellipse(self.arena_light, (83, 175, 222, alpha), (830 - radius * 2.75, 470 - radius * 1.5, radius * 5.5, radius * 3))
        self.recital_beams = pg.Surface((920, 690), pg.SRCALPHA)
        for inset in (0, 11, 22):
            pg.draw.polygon(self.recital_beams, (114, 180, 228, 8 + inset // 2), [(280 + inset, 25), (333 - inset, 25), (605 - inset, 657), (351 + inset, 657)])
            pg.draw.polygon(self.recital_beams, (114, 180, 228, 8 + inset // 2), [(610 + inset, 25), (663 - inset, 25), (569 - inset, 657), (315 + inset, 657)])
        self.piano_halo = pg.Surface((440, 420), pg.SRCALPHA)
        for radius in range(204, 24, -4):
            alpha = round(68 * (1 - radius / 208) ** 1.5)
            pg.draw.ellipse(self.piano_halo, (92, 161, 240, alpha), (220 - radius, 210 - radius, radius * 2, radius * 2))
        tile = pg.image.load(folder / "Flagstones.png").convert()
        tile = pg.transform.scale(tile, (256, 256))
        self.floors = [("", tile)]
        for name, tint in [
            ("Snow Court", (210, 235, 250)),
            ("Piano Chamber", (175, 200, 242)),
            ("Side Chapel", (196, 213, 241)),
            ("Key Gallery", (186, 221, 233)),
            ("Thaw Passage", (174, 204, 217))
        ]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.wall_face = ruins_art.wall_face.copy()
        self.wall_face.fill((160, 214, 250), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.wall_face, (154, 183, 206), (0, 0, 128, 4))
        for x, length in [(4, 10), (22, 4), (43, 8), (70, 6), (97, 12), (117, 5)]:
            pg.draw.polygon(self.wall_face, (134, 170, 193), [(x, 3), (x + 5, 3), (x + 2, length + 4)])
        self.wall_banner = ruins_art.wall_banner.copy()
        self.wall_banner.fill((133, 211, 255), special_flags=pg.BLEND_RGB_MULT)
        self.wall_sconce = pg.Surface((30, 38), pg.SRCALPHA)
        pg.draw.polygon(self.wall_sconce, (42, 58, 76), [(6, 22), (24, 22), (18, 35), (11, 35)])
        pg.draw.polygon(self.wall_sconce, (91, 198, 213), [(10, 23), (10, 15), (16, 5), (21, 16), (20, 23)])
        pg.draw.polygon(self.wall_sconce, (195, 244, 244), [(13, 23), (13, 16), (16, 12), (18, 23)])
        self.lantern_glow = pg.Surface((216, 216), pg.SRCALPHA)
        for radius in range(106, 8, -2):
            alpha = round(45 * (1 - radius / 108) ** 2)
            pg.draw.circle(self.lantern_glow, (92, 166, 221, alpha), (108, 108), radius)
        sprites = []
        for filename in ("Piano.png", "Crystals.png", "Lantern.png"):
            sprites.append(pg.image.load(folder / filename).convert_alpha())
        self.props = []
        self.bases = []
        self.scatter = []
        self.lake = pg.Surface((LAKE_WIDTH, LAKE_HEIGHT), pg.SRCALPHA)
        self.lake_mask = self.lake.copy()
        rim = []
        water = []
        for i in range(60):
            angle = math.tau * i / 60
            wobble = 3 * math.sin(angle * 7) + 3 * math.cos(angle * 13)
            x = math.cos(angle)
            y = math.sin(angle)
            rim.append((round(LAKE_WIDTH / 2 + x * (LAKE_WIDTH / 2 - 7 + wobble)), round(LAKE_HEIGHT / 2 + y * (LAKE_HEIGHT / 2 - 7 + wobble))))
            water.append((round(LAKE_WIDTH / 2 + x * (LAKE_WIDTH / 2 - 17 + wobble)), round(LAKE_HEIGHT / 2 + y * (LAKE_HEIGHT / 2 - 17 + wobble))))
        pg.draw.polygon(self.lake, (60, 79, 103), rim)
        pg.draw.lines(self.lake, (122, 169, 184), True, rim, 3)
        pg.draw.polygon(self.lake, (30, 57, 80), water)
        pg.draw.polygon(self.lake_mask, (255, 255, 255), water)
        for inset in range(20, 66, 4):
            pg.draw.ellipse(self.lake, (25 + inset // 5, 48 + inset // 6, 69 + inset // 4), (inset, inset, LAKE_WIDTH - inset * 2, LAKE_HEIGHT - inset * 2))
        for index in range(0, len(rim), 3):
            x, y = rim[index]
            inner_x, inner_y = water[index]
            pg.draw.line(self.lake, (155, 192, 200), (x, y), (inner_x, inner_y), 2)
        self.reflection = self.lake.copy()
        self.ripples = [(54 + i * 193 % (LAKE_WIDTH - 119), 45 + i * 83 % (LAKE_HEIGHT - 88), 9 + i * 13 % 27) for i in range(68)]
        self.extra_sprites = []
        for filename in ("BrokenWall", "MusicStand", "KeyCrates", "Metronome"):
            self.extra_sprites.append(pg.image.load(folder / f"{filename}.png").convert_alpha())
        self.extra_sprites.append(sprites[1])
        for name, x, y, index, width in FROST_PROPS:
            sprite = sprites[index]
            height = round(width * sprite.get_height() / sprite.get_width())
            self.props.append(RuinsProp(x, y, 44, pg.transform.scale(sprite, (width, height))))
            if index == 0:
                # The piano sits against the northern wall with its keyboard facing south.
                self.bases.append(pg.Rect(x - width // 2 + 8, CHAMBER_NORTH, width - 16, y - CHAMBER_NORTH + 22))
            else:
                self.bases.append(pg.Rect(x - width // 2 + 9, y - 28, width - 18, 50))

    def add_detail_prop(self, x, y, index, width):

        sprite = self.extra_sprites[index]
        height = round(sprite.get_height() * width / sprite.get_width())
        self.props.append(RuinsProp(x, y, 40, pg.transform.scale(sprite, (width, height))))
        self.bases.append(pg.Rect(x - width // 2 + 6, y - 18, width - 12, 38))

    def populate(self, rooms, corridors):

        for name, x, y, index, width in EXTRA_LANDMARKS:
            self.add_detail_prop(x, y, index, width)
        for name, x, y, index, width in FROST_PROPS:
            if index == 1:
                for side in (-1, 1):
                    for dx, dy, kind in [(31, 27, 0), (52, 35, 3), (16, 43, 1)]:
                        self.scatter.append((x + dx * side, y + dy, kind))

    def draw_scatter(self, screen, camera):

        view = screen.get_rect()
        for x, y, kind in self.scatter:
            x, y = camera.apply(x, y)
            if not view.collidepoint(x, y):
                continue
            if kind == 0:
                pg.draw.polygon(screen, (66, 92, 116), [(x - 10, y + 3), (x - 4, y - 5), (x + 9, y - 3), (x + 16, y + 3), (x + 3, y + 6)])
                pg.draw.line(screen, (115, 146, 160), (x - 4, y - 3), (x + 8, y - 2), 2)
            elif kind == 1:
                pg.draw.lines(screen, (100, 141, 156), False, [(x - 10, y + 6), (x - 4, y), (x + 4, y + 1), (x + 11, y - 6)], 2)
            elif kind == 2:
                pg.draw.rect(screen, (51, 58, 75), (x - 6, y - 4, 12, 7))
                pg.draw.rect(screen, (136, 142, 141), (x - 5, y - 4, 8, 3))
            else:
                for dx, dy in [(-7, 2), (0, -3), (8, 4)]:
                    pg.draw.rect(screen, (112, 146, 163), (x + dx, y + dy, 3, 2))

    def in_lake(self, x, y, radius):

        horizontal = (x - LAKE_X) / (LAKE_WIDTH / 2 + radius)
        vertical = (y - LAKE_Y) / (LAKE_HEIGHT / 2 + radius)
        return horizontal * horizontal + vertical * vertical < 1

    def render_lake(self, screen, camera, player):

        px, py = camera.apply(LAKE_X, LAKE_Y)
        bounds = self.lake.get_rect(center=(px, py))
        if not screen.get_rect().colliderect(bounds):
            return
        screen.blit(self.lake, bounds)
        self.reflection.fill((0, 0, 0, 0))
        for x, y, width in self.ripples:
            drift = round(4 * pg.math.Vector2(1, 0).rotate(pg.time.get_ticks() / 18 + x).y)
            pg.draw.line(self.reflection, (104, 177, 195, 65), (x + drift, y), (x + width + drift, y), 2)
        if self.in_lake(player.x, player.y, 165):
            direction = pg.Vector2(player.x - LAKE_X, player.y - LAKE_Y)
            if direction.length_squared():
                edge = 1 / ((direction.x / (LAKE_WIDTH / 2)) ** 2 + (direction.y / (LAKE_HEIGHT / 2)) ** 2) ** 0.5
                mirror = direction * (2 * edge - 1)
                _, _, crouch, glide = player.art.poses[player.facing]
                pose = player.movement_frame()
                if player.dash_time > 0:
                    pose = glide
                elif player.block_time > 0:
                    pose = crouch
                image = pg.transform.flip(pose, False, True)
                image.set_alpha(105)
                reflection_rect = image.get_rect(midtop=(round(LAKE_WIDTH / 2 + mirror.x), round(LAKE_HEIGHT / 2 + mirror.y - 18)))
                self.reflection.blit(image, reflection_rect)
        self.reflection.blit(self.lake_mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(self.reflection, bounds)

    def blocks(self, x, y, radius):

        if self.in_lake(x, y, radius):
            return True
        for rect in self.bases:
            if rect.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def nearby_readable(self, player):

        for x, y, label, message in FROST_NOTES:
            if abs(player.x - x) < 140 and abs(player.y - y) < 100:
                return label, message
        return None

    def interact(self, player):

        readable = self.nearby_readable(player)
        return readable

    def render_recital_hall(self, screen, camera):

        x, y = camera.apply(ARENA_X, ARENA_Y)
        if not screen.get_rect().colliderect(pg.Rect(x - 1100, y - 1350, 2200, 2450)):
            return
        screen.blit(self.arena_inlay, self.arena_inlay.get_rect(center=(x, y)))
        screen.blit(self.arena_light, self.arena_light.get_rect(center=(x, y)))
        piano_x, piano_y = camera.apply(ARENA_X, PIANO_Y - 20)
        screen.blit(self.piano_halo, self.piano_halo.get_rect(center=(piano_x, piano_y)))
        screen.blit(self.recital_beams, (x - 460, piano_y - 15))
        # Etched staves connect the stage to the floor inlay.
        for offset in (-165, 165):
            for line in range(5):
                path_x = piano_x + offset + line * 7
                pg.draw.line(screen, (74, 104, 135), (path_x, piano_y + 54), (path_x, piano_y + 720), 2)
            for index in range(11):
                note_y = piano_y + 77 + index * 55
                note_x = piano_x + offset + (index % 4) * 7
                pg.draw.ellipse(screen, (126, 148, 171), (note_x - 4, note_y, 9, 6))
                pg.draw.line(screen, (126, 148, 171), (note_x + 3, note_y + 1), (note_x + 3, note_y - 10), 1)
        ticks = pg.time.get_ticks() / 1000
        for i in range(63):
            dx = (i * 117) % 1460 - 730
            dy = (i * 83 - round(ticks * (7 + i % 5))) % 900 - 450
            drift = round(math.sin(ticks + i) * 9)
            colour = (96, 149, 176) if i % 3 else (169, 213, 224)
            pg.draw.rect(screen, colour, (x + dx + drift, y + dy, 2 if i % 3 else 3, 2))

    def render(self, screen, camera):

        self.render_recital_hall(screen, camera)
        self.draw_scatter(screen, camera)
        for name, x, y, index, width in FROST_PROPS:
            if index == 2:
                px, py = camera.apply(x, y)
                screen.blit(self.lantern_glow, (px - 108, py - 120))
        for x, y, label, message in FROST_NOTES:
            px, py = camera.apply(x, y)
            pg.draw.ellipse(screen, (27, 38, 59), (px - 17, py - 5, 38, 17))
            pg.draw.polygon(screen, (117, 155, 183), [(px - 15, py - 7), (px + 12, py - 9), (px + 17, py + 3), (px - 11, py + 7)])
            pg.draw.line(screen, (185, 217, 224), (px - 9, py - 5), (px + 10, py - 6), 2)


