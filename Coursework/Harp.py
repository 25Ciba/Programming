import math
import pygame as pg
from Guitar import GuitarArt

HARP_ARENA_X = 17920
HARP_ARENA_Y = 20160

HARP_HABITATS = [
    ("Mossback Snapper", "Common", 17520, 17120), ("Mossback Snapper", "Common", 18320, 17120),
    ("Mossback Snapper", "Common", 17570, 18590), ("Mossback Snapper", "Common", 18270, 18590),
    ("Ripple Wisp", "Strong", 17190, 17525), ("Ripple Wisp", "Strong", 18650, 17525),
    ("Ripple Wisp", "Strong", 17180, 18540), ("Ripple Wisp", "Strong", 18660, 18540),
    ("Mossback Snapper", "Common", 15480, 18080), ("Mossback Snapper", "Common", 15880, 18080),
    ("Ripple Wisp", "Strong", 19930, 17780), ("Ripple Wisp", "Strong", 20390, 17780)
]

HARP_NOTES = [
    (17920, 17920, "Read the tide marker", "The floor was built above the highest tide. The water has risen since then."),
    (17920, 15680, "Read the causeway inscription", "Follow the green lights when the lower paths disappear."),
    (15680, 17920, "Inspect the pump register", "The last keeper wrote down the tide by ear."),
    (20160, 17920, "Read the flooded inventory", "Four strings were found in the shallows. The rest are still singing."),
    (17920, 19775, "Pluck the submerged harp", "A soft note rises from below the water and fades into the stone."),
    (17920, 17615, "Listen to the reservoir", "Water strikes the old steps in the same rhythm as the harp.")
]

HARP_PAIRS = [
    (17920, 15490, 335, 1, 112), (17920, 15990, 335, 2, 80),
    (17920, 17240, 740, 1, 135), (17920, 17490, 355, 2, 82),
    (17920, 17920, 1040, 1, 142), (17920, 18490, 410, 2, 86),
    (17920, 18760, 700, 1, 136), (17920, 19010, 350, 2, 82),
    (15680, 17540, 300, 1, 108), (15680, 18310, 300, 2, 75),
    (20160, 17590, 355, 1, 108), (20160, 18200, 355, 2, 75),
    (17920, 19730, 810, 1, 138), (17920, 19970, 885, 2, 86),
    (17920, 20420, 885, 2, 86), (17920, 20710, 810, 1, 145)
]


class HarpArt(GuitarArt):

    def __init__(self, image_folder, ruins_art):

        folder = image_folder / "HarpReservoir"
        tile = pg.transform.scale(pg.image.load(folder / "Flagstones.png").convert(), (256, 256))
        self.floors = [("", tile)]
        for name, tint in [
            ("Dark Reservoir", (196, 226, 223)), ("Raised Causeway", (197, 219, 228)),
            ("Pump Room", (172, 203, 209)), ("Harp Chamber", (193, 215, 233)),
            ("Sunken Hall", (180, 213, 206))
        ]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.wall_face = ruins_art.wall_face.copy()
        self.wall_face.fill((64, 107, 106), special_flags=pg.BLEND_RGB_ADD)
        self.wall_face.fill((170, 203, 215), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.wall_face, (108, 145, 146), (0, 0, 128, 4))
        self.wall_banner = ruins_art.wall_banner.copy()
        self.wall_banner.fill((132, 199, 190), special_flags=pg.BLEND_RGB_MULT)
        self.wall_sconce = ruins_art.wall_sconce
        self.lantern_glow = pg.Surface((180, 180), pg.SRCALPHA)
        for radius in range(88, 0, -3):
            alpha = round(38 * (1 - radius / 90) ** 2)
            pg.draw.circle(self.lantern_glow, (91, 173, 174, alpha), (90, 90), radius)
        self.sprites = [pg.image.load(folder / f"{name}.png").convert_alpha() for name in ("Harp", "Column", "Lantern")]
        self.props = []
        self.bases = []
        self.lanterns = []
        self.ringing_until = 0
        self.populate()
        self.pools = []
        for x in (17245, 18595):
            self.pools.append(pg.Rect(x - 243, 17670, 486, 720))
        self.water = pg.Surface((486, 720), pg.SRCALPHA)
        for inset in range(0, 64, 4):
            colour = (22 + inset // 6, 49 + inset // 8, 64 + inset // 7)
            pg.draw.ellipse(self.water, colour, (inset, inset, 486 - inset * 2, 720 - inset * 2))
        pg.draw.ellipse(self.water, (89, 141, 143), self.water.get_rect().inflate(-4, -4), 3)
        pg.draw.ellipse(self.water, (46, 95, 109), self.water.get_rect().inflate(-14, -14), 3)

    def render_arena(self, screen, camera):

        x, y = camera.apply(HARP_ARENA_X, HARP_ARENA_Y)
        for width, height, colour in [(1140, 860, (45, 83, 87)), (1100, 820, (84, 121, 116)), (1020, 740, (46, 86, 94))]:
            pg.draw.ellipse(screen, colour, (x - width // 2, y - height // 2, width, height), 4)
        for index in range(-2, 3):
            end_x = x + index * 55
            pg.draw.line(screen, (68, 103, 105), (end_x, y - 150), (end_x, y + 150), 3)

    def populate(self):

        self.add_prop(17920, 19635, 0, 156)
        self.add_prop(17920, 17750, 2, 108)
        for center, y, offset, index, width in HARP_PAIRS:
            self.add_prop(center - offset, y, index, width)
            self.add_prop(center + offset, y, index, width)

    def blocks(self, x, y, radius):

        for pool in self.pools:
            dx = (x - pool.centerx) / (pool.width / 2 + radius)
            dy = (y - pool.centery) / (pool.height / 2 + radius)
            if dx * dx + dy * dy < 1:
                return True
        return super().blocks(x, y, radius)

    def nearby_readable(self, player):

        for x, y, label, message in HARP_NOTES:
            if abs(player.x - x) < 135 and abs(player.y - y) < 100:
                return label, message
        return None

    def interact(self, player):

        readable = self.nearby_readable(player)
        if readable and readable[0] in ("Listen to the reservoir", "Pluck the submerged harp"):
            self.ringing_until = pg.time.get_ticks() + 2600
        return readable

    def render(self, screen, camera):

        view = screen.get_rect()
        region_x, region_y = camera.apply(14900, 14800)
        if not view.colliderect((region_x, region_y, 6400, 6500)):
            return
        x, y = camera.apply(HARP_ARENA_X, HARP_ARENA_Y)
        if view.colliderect((x - 475, y - 360, 950, 720)):
            for i in range(4):
                pg.draw.ellipse(screen, (80, 118, 119), (x - 448 + 11 * i, y - 305 + 11 * i, 896 - 22 * i, 610 - 22 * i), 2)
            for i in range(16):
                angle = math.tau * i / 16
                px = round(x + math.cos(angle) * 410)
                py = round(y + math.sin(angle) * 272)
                pg.draw.polygon(screen, (135, 164, 153), [(px, py - 7), (px + 5, py), (px, py + 7), (px - 5, py)])
            for i in range(3):
                pg.draw.arc(screen, (108, 145, 146), (x - 175 + i * 85, y - 115 + i * 30, 190, 130), 0.1, 4.2, 3)
        now = pg.time.get_ticks()
        for pool in self.pools:
            x, y = camera.apply(pool.x, pool.y)
            if not view.colliderect((x, y, pool.width, pool.height)):
                continue
            screen.blit(self.water, (x, y))
            for i in range(28):
                dx = (i * 47) % 284 - 142
                dy = (i * 71) % 468 - 234
                drift = round(math.sin(now / 580 + i) * 8)
                pg.draw.line(screen, (62, 112, 124), (x + 243 + dx + drift, y + 360 + dy), (x + 260 + dx + drift, y + 360 + dy), 2)
        for x, y in self.lanterns:
            px, py = camera.apply(x, y)
            if view.colliderect((px - 90, py - 90, 180, 180)):
                screen.blit(self.lantern_glow, (px - 90, py - 90))
        for y in range(17100, 18850, 54):
            for x in (17705, 18135):
                px, py = camera.apply(x, y)
                pg.draw.line(screen, (89, 124, 128), (px - 16, py), (px + 16, py), 2)
                pg.draw.rect(screen, (114, 149, 144), (px - 2, py - 3, 4, 6))
        for x, y, label, message in HARP_NOTES:
            px, py = camera.apply(x, y)
            pg.draw.polygon(screen, (63, 88, 96), [(px - 13, py - 6), (px + 11, py - 9), (px + 15, py + 4), (px - 9, py + 8)])
            pg.draw.line(screen, (155, 179, 168), (px - 8, py - 4), (px + 9, py - 6), 2)
        now = pg.time.get_ticks()
        for i in range(26):
            x = 17010 + (i * 127 + now // 45) % 1820
            y = 17440 + (i * 73) % 920
            px, py = camera.apply(x, y)
            pg.draw.rect(screen, (100, 152, 150), (px, py, 3, 1))
        if self.ringing_until > now:
            for x, y in [(17920, 17750), (17920, 19635)]:
                px, py = camera.apply(x, y)
                for i in range(7):
                    dx = (i * 29 + now // 37) % 92 - 46
                    dy = (i * 23 + now // 31) % 83
                    pg.draw.rect(screen, (153, 210, 203), (px + dx, py - dy, 3, 2))
