import math
import pygame as pg
from Guitar import GuitarArt

FLUTE_ARENA_X = 20480
FLUTE_ARENA_Y = 10880

FLUTE_HABITATS = [
    ("Chalk Skitter", "Common", 17520, 10645), ("Chalk Skitter", "Common", 18320, 10645),
    ("Reed Wisp", "Strong", 17200, 10920), ("Reed Wisp", "Strong", 18640, 10920),
    ("Chalk Skitter", "Common", 17500, 11370), ("Chalk Skitter", "Common", 18340, 11370),
    ("Reed Wisp", "Strong", 17700, 8455), ("Reed Wisp", "Strong", 18140, 8455),
    ("Chalk Skitter", "Common", 17710, 12950), ("Chalk Skitter", "Common", 18130, 12950),
    ("Reed Wisp", "Strong", 17690, 13260), ("Reed Wisp", "Strong", 18150, 13260),
    ("Chalk Skitter", "Common", 15460, 10730), ("Chalk Skitter", "Common", 15900, 10730)
]

FLUTE_NOTES = [
    (15680, 10930, "Read the waystone", "Follow the breeze through the cloister. The doors here were built to let it pass."),
    (17920, 11110, "Ring the cloister chimes", "The wind carries a thin answer from the recital hall."),
    (17920, 8640, "Read the breath exercise", "Hold one note until the chimes go quiet. Begin again on the next breath."),
    (17920, 13120, "Inspect the reed case", "The apprentice carved reeds here before earning a silver flute."),
    (20480, 10120, "Play the silver flute", "One clear note travels the length of the hall. Nothing echoes back.")
]

FLUTE_PAIRS = [
    # West entrance vestry.
    (15680, 10620, 390, 1, 102), (15680, 11140, 390, 2, 80),
    # Main cloister, with a wide central promenade.
    (17920, 10210, 560, 1, 142), (17920, 10460, 560, 1, 132),
    (17920, 10725, 560, 1, 126), (17920, 11235, 560, 1, 132),
    (17920, 11540, 560, 1, 142), (17920, 10460, 355, 2, 74),
    (17920, 11235, 355, 2, 74),
    # Two quiet side chapels.
    (17920, 8330, 390, 1, 108), (17920, 8850, 390, 2, 76),
    (17920, 12800, 360, 1, 100), (17920, 13380, 360, 2, 74),
    # Recital hall perimeter, leaving a clear middle for the future fight.
    (20480, 10300, 460, 1, 142), (20480, 10530, 540, 2, 90),
    (20480, 11230, 540, 2, 90), (20480, 11450, 460, 1, 142)
]


class FluteArt(GuitarArt):

    def __init__(self, image_folder, ruins_art):

        folder = image_folder / "FluteCloister"
        tile = pg.transform.scale(pg.image.load(folder / "Flagstones.png").convert(), (256, 256))
        self.floors = [("", tile)]
        for name, tint in [
            ("Open Cloister", (222, 229, 225)), ("High Chapel", (195, 211, 230)),
            ("Wind Vestry", (218, 208, 225)), ("Flute Hall", (216, 226, 236)),
            ("Lower Chapel", (202, 223, 215))
        ]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.wall_face = ruins_art.wall_face.copy()
        self.wall_face.fill((177, 196, 185), special_flags=pg.BLEND_RGB_ADD)
        self.wall_face.fill((157, 165, 171), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.wall_face, (139, 151, 151), (0, 0, 128, 4))
        self.wall_banner = ruins_art.wall_banner.copy()
        self.wall_banner.fill((157, 221, 207), special_flags=pg.BLEND_RGB_MULT)
        self.wall_sconce = ruins_art.wall_sconce
        self.lantern_glow = pg.Surface((180, 180), pg.SRCALPHA)
        for radius in range(88, 0, -3):
            alpha = round(38 * (1 - radius / 90) ** 2)
            pg.draw.circle(self.lantern_glow, (139, 190, 174, alpha), (90, 90), radius)
        self.sprites = [pg.image.load(folder / f"{name}.png").convert_alpha() for name in ("Lectern", "Column", "Chimes")]
        self.props = []
        self.bases = []
        self.lanterns = []
        self.ringing_until = 0
        self.populate()

    def populate(self):

        self.add_prop(20480, 10015, 0, 175)
        self.add_prop(17920, 10990, 2, 116)
        for center, y, offset, index, width in FLUTE_PAIRS:
            self.add_prop(center - offset, y, index, width)
            self.add_prop(center + offset, y, index, width)

    def nearby_readable(self, player):

        for x, y, label, message in FLUTE_NOTES:
            if abs(player.x - x) < 135 and abs(player.y - y) < 100:
                return label, message
        return None

    def interact(self, player):

        readable = self.nearby_readable(player)
        if readable and readable[0] in ("Ring the cloister chimes", "Play the silver flute"):
            self.ringing_until = pg.time.get_ticks() + 2600
        return readable

    def render(self, screen, camera):

        view = screen.get_rect()
        region_x, region_y = camera.apply(14900, 7800)
        if not view.colliderect((region_x, region_y, 6400, 6250)):
            return
        x, y = camera.apply(FLUTE_ARENA_X, FLUTE_ARENA_Y)
        if view.colliderect((x - 475, y - 360, 950, 720)):
            for i in range(4):
                pg.draw.ellipse(screen, (89, 114, 115), (x - 448 + 11 * i, y - 305 + 11 * i, 896 - 22 * i, 610 - 22 * i), 2)
            for i in range(16):
                angle = math.tau * i / 16
                px = round(x + math.cos(angle) * 410)
                py = round(y + math.sin(angle) * 272)
                pg.draw.polygon(screen, (132, 150, 144), [(px, py - 7), (px + 5, py), (px, py + 7), (px - 5, py)])
            for i in range(3):
                pg.draw.arc(screen, (113, 142, 136), (x - 175 + i * 85, y - 115 + i * 30, 190, 130), 0.1, 4.2, 3)
        for x, y in self.lanterns:
            px, py = camera.apply(x, y)
            if view.colliderect((px - 90, py - 90, 180, 180)):
                screen.blit(self.lantern_glow, (px - 90, py - 90))
        for y in range(10180, 11600, 46):
            for x in (17650, 18190):
                px, py = camera.apply(x, y)
                pg.draw.line(screen, (104, 121, 117), (px - 16, py), (px + 16, py), 2)
                pg.draw.rect(screen, (120, 133, 128), (px - 2, py - 3, 4, 6))
        for x, y, label, message in FLUTE_NOTES:
            px, py = camera.apply(x, y)
            pg.draw.polygon(screen, (81, 90, 104), [(px - 13, py - 6), (px + 11, py - 9), (px + 15, py + 4), (px - 9, py + 8)])
            pg.draw.line(screen, (162, 181, 174), (px - 8, py - 4), (px + 9, py - 6), 2)
        now = pg.time.get_ticks()
        for i in range(26):
            x = 17010 + (i * 127 + now // 45) % 1820
            y = 10440 + (i * 73) % 860
            px, py = camera.apply(x, y)
            pg.draw.rect(screen, (119, 145, 143), (px, py, 3, 1))
        if self.ringing_until > now:
            for x, y in [(17920, 10990), (20480, 10015)]:
                px, py = camera.apply(x, y)
                for i in range(7):
                    dx = (i * 29 + now // 37) % 92 - 46
                    dy = (i * 23 + now // 31) % 83
                    pg.draw.rect(screen, (156, 207, 192), (px + dx, py - dy, 3, 2))
