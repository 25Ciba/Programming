import pygame as pg
import random

# The north route from the Blue-Grey Ruins to Frost Organ.
GATE_X = 10880
GATE_Y = 7360
SHRINE_X = 11060
SHRINE_Y = 8500

# Floor markings give each starter room a recognisable landmark.
INLAYS = [
    (10880, 10880, 92),
    (8640, 10880, 68),
    (13120, 10880, 108),
    (10880, 13120, 52)
]


READABLES = [
    (SHRINE_X, SHRINE_Y, "Read the shrine", "Leave one lantern lit. The orchestra will find its way home."),
    (10880, 10580, "Read the rehearsal slate", "One beat from each section. Leave the final beat for the Overture."),
    (8640, 10630, "Read the torn programme", "Tonight's Overture. The six soloists will enter after the last lantern dims."),
    (13120, 10600, "Read the practice plaque", "Keep time with the Overture. There is a pause after every third strike."),
    (10880, 13290, "Read the waystone", "Follow the dry echoes west. Follow the returning echoes east.")
]

BENCHES = [
    (10600, 8490), (10600, 8790),
    (10520, 11060), (10520, 11168), (10520, 11276),
    (11240, 11060), (11240, 11168), (11240, 11276)
]

LAMPS = [
    (10715, 8100), (11045, 8100), (10715, 9020), (11045, 9020),
    (10690, 10200), (11070, 10200), (10570, 10800), (11190, 10800),
    (10690, 11520), (11070, 11520), (8440, 10630), (8840, 10630),
    (12930, 10600), (13310, 10600), (12930, 11160), (13310, 11160),
    (10720, 12850), (11040, 12850), (10720, 13320), (11040, 13320)
]


class RuinsGate:

    def __init__(self):

        self.doorway = pg.Rect(GATE_X - 288, GATE_Y - 20, 576, 40)
        self.nearby = self.doorway.inflate(100, 560)
        self.progress = 0
        self.hold = 0
        self.panel = pg.Surface((288, 64), pg.SRCALPHA)
        pg.draw.rect(self.panel, (17, 21, 32), (0, 4, 288, 60))
        pg.draw.rect(self.panel, (65, 79, 96), (0, 4, 288, 12))
        pg.draw.rect(self.panel, (124, 100, 64), (0, 20, 288, 4))
        pg.draw.rect(self.panel, (42, 51, 70), (0, 30, 288, 22))
        for x in range(12, 288, 24):
            pg.draw.rect(self.panel, (90, 106, 119), (x, 25, 5, 31))
            pg.draw.rect(self.panel, (156, 125, 76), (x, 24, 5, 5))

    def update(self, dt, player):

        if self.nearby.collidepoint(player.x, player.y):
            self.hold = 0.45
        else:
            self.hold = max(0, self.hold - dt)

        if self.hold > 0:
            self.progress = min(1, self.progress + dt * 2.5)
        else:
            self.progress = max(0, self.progress - dt * 2)

    def panels(self):

        width = round(self.panel.get_width() * (1 - self.progress))
        left = pg.Rect(self.doorway.left, self.doorway.top, width, self.doorway.height)
        right = pg.Rect(self.doorway.right - width, self.doorway.top, width, self.doorway.height)
        return left, right

    def blocks(self, x, y, radius):

        if self.progress == 1 or not self.doorway.inflate(radius * 2, radius * 2).collidepoint(x, y):
            return False
        for panel in self.panels():
            if panel.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def render(self, screen, camera):

        left, right = self.panels()
        if left.width > 0:
            screen.blit(self.panel, camera.apply(left.x, left.y - 20), (288 - left.width, 0, left.width, 64))
            screen.blit(self.panel, camera.apply(right.x, right.y - 20), (0, 0, right.width, 64))
        for x in (self.doorway.left, self.doorway.right):
            px, py = camera.apply(x, GATE_Y)
            pg.draw.rect(screen, (24, 29, 42), (px - 16, py - 57, 32, 108))
            pg.draw.rect(screen, (84, 99, 115), (px - 12, py - 55, 24, 36))
            pg.draw.rect(screen, (197, 155, 87), (px - 5, py - 32, 10, 8))


class RuinsArt:

    def __init__(self, image_folder):

        self.tile = pg.Surface((128, 128))
        self.tile.fill((35, 44, 58))
        rng = random.Random(9)
        for y in range(-16, 128, 32):
            shift = 32 if y % 64 == 16 else 0
            for x in range(-64 + shift, 128, 64):
                shade = rng.randint(0, 8)
                pg.draw.rect(self.tile, (47 + shade, 58 + shade, 73 + shade), (x, y, 61, 29))
                pg.draw.line(self.tile, (65, 77, 92), (x + 2, y + 2), (x + 57, y + 2), 2)
                pg.draw.rect(self.tile, (57, 72, 79), (x + rng.randrange(6, 48, 2), y + 18, 10, 3))
        self.lamp = pg.Surface((72, 72), pg.SRCALPHA)
        for radius in range(35, 6, -1):
            pg.draw.circle(self.lamp, (221, 153, 77, (36 - radius) * 3), (36, 36), radius)
        pg.draw.rect(self.lamp, (40, 40, 50), (28, 28, 16, 16))
        pg.draw.rect(self.lamp, (190, 126, 64), (31, 31, 10, 10))
        pg.draw.rect(self.lamp, (255, 212, 132), (34, 34, 4, 4))
        self.shrine = None
        shrine_path = image_folder / "BlueGrey" / "Shrine.png"
        if shrine_path.is_file():
            self.shrine = pg.image.load(shrine_path).convert_alpha()

    def draw_furnishings(self, screen, camera):

        # The boards, rugs and chalk are drawn flat against the floor.
        x, y = camera.apply(8640, 10880)
        pg.draw.rect(screen, (33, 32, 42), (x - 204, y - 172, 408, 292))
        pg.draw.rect(screen, (87, 68, 63), (x - 200, y - 168, 400, 284))
        for board in range(14):
            board_y = y - 166 + board * 20
            pg.draw.line(screen, (57, 47, 51), (x - 196, board_y), (x + 195, board_y), 3)
            pg.draw.line(screen, (104, 79, 66), (x - 195, board_y + 4), (x + 195, board_y + 4), 2)
        pg.draw.polygon(screen, (39, 43, 55), [(x + 80, y + 118), (x + 90, y + 78), (x + 150, y + 80), (x + 160, y + 118)])
        pg.draw.rect(screen, (104, 74, 73), (x - 164, y - 136, 76, 180))
        pg.draw.rect(screen, (117, 86, 78), (x - 160, y - 132, 68, 172), 3)

        for world_x, world_y, width, height in [(10880, 8680, 112, 320), (10880, 11140, 156, 392), (10880, 13120, 120, 388)]:
            x, y = camera.apply(world_x, world_y)
            rug = pg.Rect(0, 0, width, height)
            rug.center = (x, y)
            pg.draw.rect(screen, (38, 38, 53), rug.inflate(8, 8))
            pg.draw.rect(screen, (71, 61, 83), rug)
            pg.draw.rect(screen, (117, 99, 97), rug.inflate(-12, -12), 3)
            for edge in (rug.top + 15, rug.bottom - 15):
                pg.draw.line(screen, (142, 120, 102), (rug.left + 12, edge), (rug.right - 12, edge), 3)

        x, y = camera.apply(13120, 10880)
        for radius in (144, 158):
            pg.draw.circle(screen, (115, 116, 110), (x, y), radius, 3)
        for dx, dy in ((-180, 0), (180, 0), (0, -180), (0, 180)):
            pg.draw.rect(screen, (153, 123, 78), (x + dx - 6, y + dy - 6, 12, 12))

        for world_x, world_y in BENCHES:
            x, y = camera.apply(world_x, world_y)
            pg.draw.rect(screen, (24, 30, 42), (x - 52, y - 15, 104, 34))
            pg.draw.rect(screen, (76, 59, 56), (x - 48, y - 13, 96, 28))
            pg.draw.rect(screen, (117, 89, 72), (x - 45, y - 9, 90, 5))
            for dx in (-40, 36):
                pg.draw.rect(screen, (160, 124, 73), (x + dx, y - 8, 4, 16))

        for world_x, world_y, label, message in READABLES[1:]:
            x, y = camera.apply(world_x, world_y)
            pg.draw.rect(screen, (25, 31, 43), (x - 21, y - 15, 42, 30))
            pg.draw.rect(screen, (159, 132, 91), (x - 16, y - 11, 32, 22))
            for dy in (-6, 0, 6):
                pg.draw.line(screen, (98, 76, 65), (x - 10, y + dy), (x + 9, y + dy), 2)

        for world_x, world_y in LAMPS:
            x, y = camera.apply(world_x, world_y)
            screen.blit(self.lamp, (x - 36, y - 36))

    def blocks(self, x, y, radius):

        for bench_x, bench_y in BENCHES:
            bench = pg.Rect(bench_x - 48, bench_y - 13, 96, 28)
            if bench.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def draw_floor(self, screen, rect, view, origin):

        visible = rect.clip(view)
        if not visible.width or not visible.height:
            return
        screen.set_clip(visible)
        start_x = visible.left - (visible.left - origin[0]) % 128
        start_y = visible.top - (visible.top - origin[1]) % 128
        for y in range(start_y, visible.bottom, 128):
            for x in range(start_x, visible.right, 128):
                screen.blit(self.tile, (x, y))
        screen.set_clip(view)

    def render(self, screen, camera):

        for x, y, size in INLAYS:
            px, py = camera.apply(x, y)
            pg.draw.rect(screen, (35, 46, 60), (px - size, py - size, size * 2, size * 2))
            pg.draw.rect(screen, (85, 105, 115), (px - size, py - size, size * 2, size * 2), 4)
            pg.draw.rect(screen, (117, 98, 69), (px - size + 12, py - size + 12, size * 2 - 24, size * 2 - 24), 3)
            for offset in (-12, 12):
                pg.draw.rect(screen, (123, 112, 81), (px + offset - 2, py - 28, 5, 37))
            pg.draw.rect(screen, (123, 112, 81), (px - 14, py + 8, 29, 5))
            pg.draw.rect(screen, (123, 112, 81), (px - 2, py + 8, 5, 21))

        self.draw_furnishings(screen, camera)
        x, y = camera.apply(SHRINE_X, SHRINE_Y)
        if self.shrine is not None:
            screen.blit(self.shrine, self.shrine.get_rect(center=(x, y)))

    def nearby_readable(self, player):

        for x, y, label, message in READABLES:
            if abs(player.x - x) < 160 and abs(player.y - y) < 135:
                return label, message
        return None
