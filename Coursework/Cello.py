import math
import pygame as pg
from Guitar import GuitarArt

CELLO_ARENA_X = 3840
CELLO_ARENA_Y = 20160

CELLO_HABITATS = [
    ("Silt Scorpion", "Common", 3430, 17470), ("Silt Scorpion", "Common", 4250, 17470),
    ("Rosin Spirit", "Strong", 3260, 17910), ("Rosin Spirit", "Strong", 4420, 17910),
    ("Silt Scorpion", "Common", 3420, 18410), ("Silt Scorpion", "Common", 4260, 18410),
    ("Rosin Spirit", "Strong", 3600, 15555), ("Rosin Spirit", "Strong", 4080, 15555),
    ("Silt Scorpion", "Common", 1380, 17790), ("Silt Scorpion", "Common", 1820, 17790),
    ("Rosin Spirit", "Strong", 1380, 18125), ("Rosin Spirit", "Strong", 1820, 18125),
    ("Silt Scorpion", "Common", 5845, 18080), ("Silt Scorpion", "Common", 6315, 18080)
]

CELLO_NOTES = [
    (3840, 17920, "Read the silt marker", "Sand buried the seats first. The last chair was still facing the stage."),
    (3840, 15680, "Inspect the bow case", "The hair has gone slack. Someone wrapped the handle to stop it slipping."),
    (1600, 17920, "Read the crypt inscription", "Play for those who left before the final movement."),
    (6080, 17920, "Read the rosin ledger", "The cellist wore through a fresh cake every winter."),
    (3840, 19765, "Draw the cello bow", "A low note moves through the stone long after the bow stops."),
    (3840, 17610, "Listen at the brazier", "The brazier hums at a low pitch whenever sand shifts beneath the court.")
]

CELLO_PAIRS = [
    (3840, 15400, 435, 1, 114), (3840, 15920, 435, 2, 80),
    (3840, 17160, 730, 1, 138), (3840, 17440, 555, 2, 82),
    (3840, 17780, 710, 1, 136), (3840, 18190, 710, 1, 136),
    (3840, 18480, 555, 2, 82), (3840, 18730, 730, 1, 138),
    (1600, 17590, 345, 1, 105), (1600, 18300, 345, 2, 74),
    (6080, 17590, 370, 1, 105), (6080, 18300, 370, 2, 76),
    (3840, 19760, 545, 1, 145), (3840, 19945, 615, 2, 82),
    (3840, 20420, 615, 2, 82), (3840, 20620, 545, 1, 145)
]


class CelloArt(GuitarArt):

    def __init__(self, image_folder, ruins_art):

        folder = image_folder / "CelloCatacombs"
        tile = pg.transform.scale(pg.image.load(folder / "Flagstones.png").convert(), (256, 256))
        self.floors = [("", tile)]
        for name, tint in [
            ("Silt Court", (235, 220, 193)), ("Bow Landing", (218, 195, 173)),
            ("Side Crypt", (204, 182, 171)), ("Cello Amphitheatre", (228, 198, 178)),
            ("Rosin Gallery", (244, 216, 179))
        ]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.wall_face = ruins_art.wall_face.copy()
        self.wall_face.fill((100, 69, 58), special_flags=pg.BLEND_RGB_ADD)
        self.wall_face.fill((211, 176, 146), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.wall_face, (154, 118, 90), (0, 0, 128, 4))
        self.wall_banner = ruins_art.wall_banner.copy()
        self.wall_banner.fill((237, 156, 134), special_flags=pg.BLEND_RGB_MULT)
        self.wall_sconce = ruins_art.wall_sconce
        self.lantern_glow = pg.Surface((180, 180), pg.SRCALPHA)
        for radius in range(88, 0, -3):
            alpha = round(38 * (1 - radius / 90) ** 2)
            pg.draw.circle(self.lantern_glow, (220, 137, 77, alpha), (90, 90), radius)
        self.sprites = [pg.image.load(folder / f"{name}.png").convert_alpha() for name in ("Cello", "Column", "Brazier")]
        self.props = []
        self.bases = []
        self.lanterns = []
        self.ringing_until = 0
        self.populate()

    def populate(self):

        self.add_prop(3840, 19635, 0, 156)
        self.add_prop(3840, 17750, 2, 108)
        for center, y, offset, index, width in CELLO_PAIRS:
            self.add_prop(center - offset, y, index, width)
            self.add_prop(center + offset, y, index, width)

    def nearby_readable(self, player):

        for x, y, label, message in CELLO_NOTES:
            if abs(player.x - x) < 135 and abs(player.y - y) < 100:
                return label, message
        return None

    def interact(self, player):

        readable = self.nearby_readable(player)
        if readable and readable[0] in ("Listen at the brazier", "Draw the cello bow"):
            self.ringing_until = pg.time.get_ticks() + 2600
        return readable

    def render(self, screen, camera):

        view = screen.get_rect()
        region_x, region_y = camera.apply(750, 15000)
        if not view.colliderect((region_x, region_y, 6400, 6500)):
            return
        x, y = camera.apply(CELLO_ARENA_X, CELLO_ARENA_Y)
        if view.colliderect((x - 475, y - 360, 950, 720)):
            for i in range(4):
                pg.draw.ellipse(screen, (130, 91, 76), (x - 448 + 11 * i, y - 305 + 11 * i, 896 - 22 * i, 610 - 22 * i), 2)
            for i in range(16):
                angle = math.tau * i / 16
                px = round(x + math.cos(angle) * 410)
                py = round(y + math.sin(angle) * 272)
                pg.draw.polygon(screen, (177, 129, 92), [(px, py - 7), (px + 5, py), (px, py + 7), (px - 5, py)])
            for i in range(3):
                pg.draw.arc(screen, (156, 109, 89), (x - 175 + i * 85, y - 115 + i * 30, 190, 130), 0.1, 4.2, 3)
        for x, y in self.lanterns:
            px, py = camera.apply(x, y)
            if view.colliderect((px - 90, py - 90, 180, 180)):
                screen.blit(self.lantern_glow, (px - 90, py - 90))
        for y in range(17030, 18850, 54):
            for x in (3560, 4120):
                px, py = camera.apply(x, y)
                pg.draw.line(screen, (124, 97, 83), (px - 16, py), (px + 16, py), 2)
                pg.draw.rect(screen, (148, 112, 92), (px - 2, py - 3, 4, 6))
        for x, y, label, message in CELLO_NOTES:
            px, py = camera.apply(x, y)
            pg.draw.polygon(screen, (91, 65, 60), [(px - 13, py - 6), (px + 11, py - 9), (px + 15, py + 4), (px - 9, py + 8)])
            pg.draw.line(screen, (183, 143, 107), (px - 8, py - 4), (px + 9, py - 6), 2)
        now = pg.time.get_ticks()
        for i in range(26):
            x = 2910 + (i * 127 + now // 45) % 1820
            y = 17440 + (i * 73) % 920
            px, py = camera.apply(x, y)
            pg.draw.rect(screen, (164, 126, 94), (px, py, 3, 1))
        if self.ringing_until > now:
            for x, y in [(3840, 17750), (3840, 19635)]:
                px, py = camera.apply(x, y)
                for i in range(7):
                    dx = (i * 29 + now // 37) % 92 - 46
                    dy = (i * 23 + now // 31) % 83
                    pg.draw.rect(screen, (218, 167, 112), (px + dx, py - dy, 3, 2))
