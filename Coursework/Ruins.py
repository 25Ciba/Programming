import pygame as pg
import random

# The north route from the Blue-Grey Ruins to Frost Organ.
GATEX = 10880
GATEY = 7360
SHRINEX = 10880
SHRINEY = 8500

READABLES = [
    (SHRINEX, SHRINEY, "Read the shrine", "Leave one lantern lit. The orchestra will find its way home."),
    (10880, 10580, "Read the rehearsal slate", "One beat from each section. Leave the final beat for the Overture."),
    (8640, 10630, "Read the torn programme", "Tonight's Overture. The six soloists will enter after the last lantern dims."),
    (13340, 10200, "Read the practice plaque", "Keep time with the Overture. There is a pause after every third strike."),
    (10880, 13290, "Read the waystone", "Follow the dry echoes west. Follow the returning echoes east."),
    (10980, 8160, "Inspect the lamp niche", "A name is scratched into each socket. Only one lantern is missing."),
    (10880, 11420, "Strike the rehearsal chime", "A low note echoes around the plaza. The old lamps answer."),
    (8640, 11085, "Inspect the music crate", "The lid is split. Inside, the strings are coiled in sets of six."),
    (10880, 12820, "Inspect the water gauge", "The lowest mark is labelled Before the Flood.")
]

BENCHES = [
    (10600, 8490), (11160, 8490),
    (10520, 11060), (10520, 11168), (10520, 11276),
    (11240, 11060), (11240, 11168), (11240, 11276)
]

LAMPS = [
    (10715, 8100), (11045, 8100), (10715, 9020), (11045, 9020),
    (10690, 10200), (11070, 10200), (10570, 10800), (11190, 10800),
    (10690, 11520), (11070, 11520), (8440, 10630), (8840, 10630),
    (12820, 10330), (13860, 10330), (12820, 11430), (13860, 11430),
    (10720, 12850), (11040, 12850), (10720, 13320), (11040, 13320)
]


# Name, strength, and home position. Lantern Shelter is a safe room.
HABITATS = [
    ("Slate Scarab", "Common", 10320, 10620),
    ("Slate Scarab", "Common", 10440, 10510),
    ("Slate Scarab", "Common", 11440, 10620),
    ("Slate Scarab", "Common", 11320, 10510),
    ("Echo Bat", "Strong", 8530, 11090),
    ("Slate Scarab", "Common", 8750, 11090),
    ("Echo Bat", "Strong", 10700, 13350),
    ("Slate Scarab", "Common", 11060, 13400),
    ("Slate Scarab", "Common", 10230, 10490),
    ("Echo Bat", "Strong", 10540, 10610),
    ("Slate Scarab", "Common", 11545, 10495),
    ("Slate Scarab", "Common", 11245, 10645),
    ("Echo Bat", "Strong", 8680, 11205),
    ("Slate Scarab", "Common", 10830, 13470),
    ("Overture Keeper", "Overture", 13340, 10880)
]


# Landmark bases are solid. Their short front faces suggest height.
LANDMARKS = [
    ("Lantern stand", 11185, 8750, 64, 64),
    ("Lantern stand", 10575, 8750, 64, 64),
    ("Seating island", 10270, 11100, 156, 86),
    ("Seating island", 11490, 11100, 156, 86),
    ("Broken columns", 8420, 10950, 84, 70),
    ("Broken columns", 8860, 10950, 84, 70),
    ("Practice drum", 12650, 11280, 110, 76),
    ("Practice drum", 14030, 11280, 110, 76),
    ("Waystone pier", 10660, 13020, 96, 88),
    ("Waystone pier", 11100, 13020, 96, 88)
]


def Creatureframes(Imagefolder, name, action, scale):

    if name in ("Slate Scarab", "Rime Beetle", "Glasswing Moth"):
        return Articulatedcreatureframes(Imagefolder, name, action, scale)

    names = [("Slate Scarab", "Scarab.png"), ("Echo Bat", "Bat.png"), ("Overture Keeper", "Keeper.png")]
    for creature, filename in names:
        if creature == name:
            sprite = pg.image.load(Imagefolder / "BlueGrey" / filename).convert_alpha()
            break
    rows = []
    for direction in range(4):
        frames = []
        if direction == 1:
            body = pg.transform.flip(sprite, True, False)
        else:
            body = sprite
        for stretch in (0, 2, 4, 2, 0, -2):
            frame = pg.Surface((scale, scale), pg.SRCALPHA)
            height = scale * 3 // 4
            if action == "Run":
                height += stretch
            elif action == "Attack":
                height += stretch * 2
            width = round(height * body.get_width() / body.get_height())
            pose = pg.transform.scale(body, (width, height))
            if name == "Echo Bat":
                # Wings pivot at the shoulders while the body stays centred.
                center = scale // 2
                Rooty = scale - 34
                for side in (-1, 1):
                    Tipx = center + side * (23 - stretch)
                    Tipy = Rooty - 8 + stretch * 4
                    wing = [(center + side * 4, Rooty), (center + side * 14, Rooty - 8), (Tipx, Tipy), (Tipx - side * 3, Tipy + 13), (center + side * 10, Rooty + 11)]
                    pg.draw.polygon(frame, (35, 28, 53), wing)
                    pg.draw.lines(frame, (100, 79, 128), False, wing[:3], 2)
                middle = pose.get_width() // 2
                Coretop = pose.get_height() // 2
                core = pose.subsurface((middle - 9, Coretop, 18, pose.get_height() - Coretop))
                frame.blit(core, core.get_rect(midbottom=(center, scale - 12)))
            else:
                frame.blit(pose, pose.get_rect(midbottom=(scale // 2, scale - 12)))
            frames.append(frame)
        rows.append(frames)
    return rows


TERRACEBASES = [
    pg.Rect(10690, 8230, 380, 37),
    pg.Rect(10620, 10135, 520, 37),
    pg.Rect(8400, 10520, 480, 37),
    pg.Rect(10670, 12700, 420, 37)
]
for Pillarx, Pillary in [(10580, 10280), (11180, 10280), (10320, 11380), (11440, 11380), (8420, 10720), (8860, 10720)]:
    TERRACEBASES.append(pg.Rect(Pillarx - 27, Pillary - 12, 54, 36))


def Articulatedcreatureframes(Imagefolder, name, action, scale):

    Artfolder = Imagefolder / "FrostPiano" / "MobPoses"
    if name == "Slate Scarab":
        Artfolder = Imagefolder / "BlueGrey" / "MobPoses"
    stem = "Moth"
    if name == "Slate Scarab":
        stem = "Scarab"
    elif name == "Rime Beetle":
        stem = "Beetle"
    sprites = []
    for i in range(3):
        sprite = pg.image.load(Artfolder / f"{stem}{i}.png").convert_alpha()
        width, height = sprite.get_size()
        ratio = min(scale * 0.86 / width, scale * 0.73 / height)
        sprites.append(pg.transform.scale(sprite, (round(width * ratio), round(height * ratio))))
    poses = [(0, 0, 0), (1, 0, 0)]
    if action == "Run":
        poses = [(0, -2, 0), (0, -1, 2), (1, 1, 1), (1, 2, 0), (1, 1, -1), (0, -1, 1)]
        if name == "Glasswing Moth":
            poses = [(0, 0, 1), (0, 0, 0), (1, 0, -1), (2, 0, -2), (2, 0, -1), (1, 0, 0)]
    elif action == "Attack":
        poses = [(0, 0, 4), (0, -2, 3), (2, 3, 0), (2, 5, -1), (2, 2, 0), (1, 0, 1)]
    rows = []
    for direction in range(4):
        frames = []
        for index, x, y in poses:
            frame = pg.Surface((scale, scale), pg.SRCALPHA)
            sprite = sprites[index]
            if direction == 1:
                sprite = pg.transform.flip(sprite, True, False)
                x = -x
            frame.blit(sprite, sprite.get_rect(midbottom=(scale // 2 + x, scale - 10 - y)))
            frames.append(frame)
        rows.append(frames)
    return rows


class RuinsGate:

    def __init__(self):

        self.doorway = pg.Rect(GATEX - 288, GATEY - 20, 576, 40)
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
            px, py = camera.apply(x, GATEY)
            pg.draw.rect(screen, (24, 29, 42), (px - 16, py - 57, 32, 108))
            pg.draw.rect(screen, (84, 99, 115), (px - 12, py - 55, 24, 36))
            pg.draw.rect(screen, (197, 155, 87), (px - 5, py - 32, 10, 8))


class RuinsProp:

    def __init__(self, x, y, height, sprite):

        self.x = x
        self.y = y
        self.height = height
        self.sprite = sprite

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        rect = self.sprite.get_rect(midbottom=(x, y + self.height // 2))
        if camera.screen.get_rect().colliderect(rect):
            camera.screen.blit(self.sprite, rect)


class RuinsArt:

    def __init__(self, Imagefolder):

        stone = pg.image.load(Imagefolder / "BlueGrey" / "WallStone.png").convert()
        self.Wallface = pg.transform.scale(stone, (128, 48))
        self.Wallface.fill((190, 186, 209), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.Wallface, (35, 34, 52), (0, 41, 128, 7))
        pg.draw.rect(self.Wallface, (125, 120, 140), (0, 0, 128, 4))
        pg.draw.rect(self.Wallface, (81, 79, 104), (0, 4, 128, 4))
        self.Wallbanner = pg.Surface((34, 54), pg.SRCALPHA)
        pg.draw.polygon(self.Wallbanner, (28, 27, 44), [(3, 5), (33, 5), (32, 45), (20, 53), (6, 46)])
        pg.draw.polygon(self.Wallbanner, (91, 62, 92), [(5, 5), (29, 5), (29, 43), (17, 49), (5, 43)])
        pg.draw.lines(self.Wallbanner, (155, 115, 79), False, [(8, 8), (8, 41), (17, 46), (26, 41), (26, 8)], 2)
        pg.draw.line(self.Wallbanner, (207, 166, 98), (1, 5), (33, 5), 3)
        pg.draw.lines(self.Wallbanner, (194, 152, 92), False, [(13, 19), (13, 27), (21, 27), (21, 19)], 2)
        pg.draw.line(self.Wallbanner, (194, 152, 92), (17, 27), (17, 36), 2)
        self.Wallsconce = pg.Surface((30, 38), pg.SRCALPHA)
        pg.draw.polygon(self.Wallsconce, (34, 30, 44), [(5, 22), (25, 22), (20, 35), (10, 35)])
        pg.draw.polygon(self.Wallsconce, (144, 99, 66), [(7, 22), (23, 22), (18, 31), (12, 31)])
        pg.draw.polygon(self.Wallsconce, (220, 127, 66), [(10, 22), (9, 15), (16, 5), (21, 16), (20, 22)])
        pg.draw.polygon(self.Wallsconce, (255, 214, 126), [(12, 22), (12, 17), (16, 12), (18, 19), (18, 22)])
        self.props = []
        sprites = []
        for filename, width in [("Bench", 110), ("Column", 82), ("Drum", 92), ("Pier", 92), ("Planter", 156), ("LanternStand", 64)]:
            sprite = pg.image.load(Imagefolder / "BlueGrey" / "Props" / f"{filename}.png").convert_alpha()
            height = round(width * sprite.get_height() / sprite.get_width())
            sprites.append(pg.transform.scale(sprite, (width, height)))
        for x, y in BENCHES:
            self.props.append(RuinsProp(x, y, 28, sprites[0]))
        for name, x, y, width, height in LANDMARKS:
            index = 1
            if name == "Practice drum":
                index = 2
            elif name == "Waystone pier":
                index = 3
            elif name == "Seating island":
                index = 4
            elif name == "Lantern stand":
                index = 5
            self.props.append(RuinsProp(x, y, height, sprites[index]))
        column = pg.transform.scale(sprites[1], (54, round(sprites[1].get_height() * 54 / sprites[1].get_width())))
        for base in TERRACEBASES[4:]:
            self.props.append(RuinsProp(base.centerx, base.centery, base.height, column))

        self.Chimerung = False
        self.Coolpool = pg.Surface((320, 320), pg.SRCALPHA)
        for radius in range(158, 0, -2):
            opacity = round(35 * (1 - radius / 160) ** 1.4)
            pg.draw.circle(self.Coolpool, (101, 123, 174, opacity), (160, 160), radius)
        self.masonry = []
        self.scatter = []
        self.tile = pg.image.load(Imagefolder / "BlueGrey" / "Flagstones.png").convert()
        self.tile = pg.transform.scale(self.tile, (256, 256))
        self.tile.fill((193, 202, 214), special_flags=pg.BLEND_RGB_MULT)
        self.Lanternglow = pg.Surface((216, 216), pg.SRCALPHA)
        for radius in range(106, 8, -2):
            opacity = round(42 * (1 - radius / 108) ** 2)
            pg.draw.circle(self.Lanternglow, (230, 149, 75, opacity), (108, 108), radius)
        self.floors = []
        for name, tint in [
            ("", (215, 221, 234)), ("Lantern Shelter", (222, 207, 213)),
            ("Rehearsal Plaza", (217, 216, 235)), ("Broken Stage", (232, 209, 202)),
            ("Overture Arena", (203, 211, 233)), ("South Passage", (197, 219, 218))
        ]:
            floor = self.tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.Detailfloor(floor, name)
            self.floors.append((name, floor))
        self.lamp = pg.Surface((72, 72), pg.SRCALPHA)
        pg.draw.ellipse(self.lamp, (25, 26, 40, 165), (22, 42, 34, 15))
        pg.draw.polygon(self.lamp, (34, 30, 41), [(24, 44), (27, 32), (28, 23), (36, 17), (44, 23), (45, 32), (48, 44)])
        pg.draw.polygon(self.lamp, (120, 83, 60), [(27, 42), (29, 31), (43, 31), (45, 42)])
        pg.draw.rect(self.lamp, (239, 163, 72), (31, 28, 10, 12))
        pg.draw.rect(self.lamp, (255, 220, 133), (34, 29, 4, 9))
        pg.draw.line(self.lamp, (88, 62, 53), (36, 27), (36, 41), 2)
        pg.draw.polygon(self.lamp, (157, 123, 84), [(27, 26), (36, 19), (45, 26)])
        pg.draw.line(self.lamp, (213, 169, 105), (31, 23), (38, 21), 2)
        self.shrine = None
        Shrinepath = Imagefolder / "BlueGrey" / "Shrine.png"
        if Shrinepath.is_file():
            self.shrine = pg.image.load(Shrinepath).convert_alpha()

    def Drawwalls(self, screen, camera, edges):

        view = screen.get_rect()
        for x, y, length, side in edges:
            px, py = camera.apply(x, y)
            if side == "north":
                rect = pg.Rect(px, py, length, 48)
                if not view.colliderect(rect):
                    continue
                pg.draw.rect(screen, (29, 29, 45), (px, py + 43, length, 8))
                for offset in range(0, length, 128):
                    width = min(128, length - offset)
                    screen.blit(self.Wallface, (px + offset, py), (0, 0, width, 48))
                for i, offset in enumerate(range(96, length - 40, 160)):
                    if i % 3 == 1:
                        screen.blit(self.Wallbanner, (px + offset - 17, py + 5))
                    else:
                        screen.blit(self.Lanternglow, (px + offset - 108, py - 76))
                        screen.blit(self.Wallsconce, (px + offset - 15, py + 6))
            elif side == "south":
                rect = pg.Rect(px, py - 13, length, 13)
                if view.colliderect(rect):
                    pg.draw.rect(screen, (50, 48, 68), rect)
                    pg.draw.line(screen, (125, 117, 138), rect.topleft, (rect.right - 1, rect.top), 3)
                    for offset in range(0, length, 34):
                        pg.draw.line(screen, (35, 34, 51), (px + offset, py - 10), (px + offset, py - 1), 2)
            else:
                if side == "east":
                    px -= 13
                rect = pg.Rect(px, py, 13, length)
                if view.colliderect(rect):
                    pg.draw.rect(screen, (51, 49, 69), rect)
                    pg.draw.line(screen, (106, 104, 128), rect.topleft, (px, rect.bottom - 1), 3)
                    for offset in range(0, length, 28):
                        pg.draw.line(screen, (36, 35, 53), (px + 2, py + offset), (px + 12, py + offset), 2)

    def Detailfloor(self, floor, room):

        if room == "Lantern Shelter":
            # Fine, pale repairs between the older flagstones.
            for x, y in [(34, 45), (143, 62), (77, 171), (201, 207)]:
                pg.draw.line(floor, (113, 101, 113), (x, y), (x + 19, y + 3), 2)
                pg.draw.line(floor, (71, 66, 84), (x + 4, y + 3), (x + 23, y + 5), 2)
        elif room == "Rehearsal Plaza":
            for x, y in [(57, 72), (185, 187)]:
                pg.draw.polygon(floor, (99, 91, 115), [(x, y - 6), (x + 7, y), (x, y + 6), (x - 7, y)], 2)
        elif room == "Broken Stage":
            for x, y in [(31, 84), (144, 33), (188, 176), (69, 219)]:
                pg.draw.line(floor, (106, 81, 82), (x, y), (x + 18, y - 8), 3)
                pg.draw.line(floor, (74, 58, 69), (x + 4, y + 3), (x + 16, y - 2), 2)
        elif room == "Overture Arena":
            for x, y in [(42, 125), (177, 52), (208, 192)]:
                pg.draw.line(floor, (105, 104, 128), (x, y), (x + 11, y + 8), 2)
                pg.draw.line(floor, (62, 64, 88), (x + 11, y + 8), (x + 21, y + 1), 2)
        elif room == "South Passage":
            for x, y in [(41, 37), (151, 97), (83, 204)]:
                pg.draw.ellipse(floor, (62, 80, 93), (x, y, 28, 8))
                pg.draw.line(floor, (91, 110, 119), (x + 6, y + 2), (x + 18, y + 2), 2)

    def Placemasonry(self, rooms, corridors):

        for center, y, offset, width in [(10880, 9670, 380, 106), (10880, 11650, 820, 142), (8640, 10400, 395, 130), (10880, 13600, 380, 110)]:
            for side in (-1, 1):
                x = center + side * offset
                rect = pg.Rect(x - width // 2, y, width, 55)
                if any(region == 0 and floor.contains(rect) for name, region, floor in rooms):
                    self.masonry.append(rect)
                    self.scatter.append((x + side * 35, y + 65, 2))
                    self.scatter.append((x + side * 55, y + 77, 1))

    def Drawmasonry(self, screen, camera):

        view = screen.get_rect()
        for x, y, style in self.scatter:
            px, py = camera.apply(x, y)
            if not view.collidepoint(px, py):
                continue
            pg.draw.rect(screen, (34, 42, 54), (px, py + 4, 20 + style * 5, 10))
            pg.draw.rect(screen, (78, 88, 100), (px, py, 11 + style * 3, 7))
            pg.draw.rect(screen, (93, 103, 112), (px + 2, py, 6 + style * 3, 2))
            pg.draw.rect(screen, (64, 79, 78), (px + 16, py + 8, 8, 4))

        for stone in self.masonry:
            rect = pg.Rect(camera.apply(stone.x, stone.y), stone.size)
            if not view.colliderect(rect.inflate(32, 32)):
                continue
            pg.draw.rect(screen, (27, 34, 46), rect.move(9, 11))
            pg.draw.rect(screen, (41, 49, 63), rect)
            top = rect.inflate(-6, -6)
            top.height -= 10
            masonry = pg.transform.scale(self.Wallface, top.size)
            screen.blit(masonry, top)
            pg.draw.line(screen, (80, 76, 97), (rect.left + 4, rect.bottom - 9), (rect.right - 4, rect.bottom - 9), 2)
            pg.draw.line(screen, (103, 114, 126), top.topleft, top.topright, 3)
            for x in range(top.left + 14, top.right - 4, 24):
                pg.draw.line(screen, (53, 63, 79), (x, top.bottom - 4), (x, rect.bottom - 2), 2)
            pg.draw.rect(screen, (87, 105, 102), (top.x + 6, top.y + 6, 13, 5))
            pg.draw.line(screen, (43, 51, 65), (top.centerx - 5, top.top + 2), (top.centerx + 3, top.centery), 2)
            pg.draw.line(screen, (43, 51, 65), (top.centerx + 3, top.centery), (top.centerx - 3, top.bottom - 1), 2)

    def Drawfurnishings(self, screen, camera):

        # The boards, rugs and chalk are drawn flat against the floor.
        x, y = camera.apply(8640, 10880)
        pg.draw.rect(screen, (33, 32, 42), (x - 204, y - 172, 408, 292))
        pg.draw.rect(screen, (87, 68, 63), (x - 200, y - 168, 400, 284))
        pg.draw.rect(screen, (52, 35, 44), (x - 200, y + 105, 400, 16))
        pg.draw.line(screen, (158, 110, 79), (x - 197, y + 104), (x + 196, y + 104), 4)
        for board in range(14):
            Boardy = y - 166 + board * 20
            pg.draw.line(screen, (57, 47, 51), (x - 196, Boardy), (x + 195, Boardy), 3)
            pg.draw.line(screen, (104, 79, 66), (x - 195, Boardy + 4), (x + 195, Boardy + 4), 2)
            for offset in (-132 + board * 7, 36 - board * 4, 125):
                pg.draw.line(screen, (110, 81, 65), (x + offset, Boardy + 9), (x + offset + 22, Boardy + 10), 2)
                pg.draw.rect(screen, (49, 38, 45), (x + offset - 3, Boardy + 6, 3, 3))
        pg.draw.polygon(screen, (39, 43, 55), [(x + 80, y + 118), (x + 90, y + 78), (x + 150, y + 80), (x + 160, y + 118)])
        pg.draw.rect(screen, (104, 74, 73), (x - 164, y - 136, 76, 180))
        pg.draw.rect(screen, (117, 86, 78), (x - 160, y - 132, 68, 172), 3)

        x, y = camera.apply(13340, 10880)
        for radius in (350, 368):
            pg.draw.circle(screen, (115, 116, 110), (x, y), radius, 3)
        for dx, dy in ((-385, 0), (385, 0), (0, -385), (0, 385)):
            pg.draw.rect(screen, (153, 123, 78), (x + dx - 6, y + dy - 6, 12, 12))

        for Worldx, Worldy, label, message in READABLES[1:]:
            x, y = camera.apply(Worldx, Worldy)
            pg.draw.ellipse(screen, (28, 30, 44), (x - 22, y + 3, 51, 15))
            if "programme" in label:
                pg.draw.polygon(screen, (184, 151, 109), [(x - 18, y - 11), (x + 15, y - 14), (x + 20, y + 5), (x + 9, y + 9), (x - 16, y + 11)])
                pg.draw.polygon(screen, (237, 204, 148), [(x - 15, y - 10), (x + 14, y - 12), (x + 17, y + 4), (x - 13, y + 6)])
            else:
                pg.draw.polygon(screen, (47, 48, 63), [(x - 21, y - 10), (x + 18, y - 13), (x + 22, y + 9), (x - 17, y + 15)])
                pg.draw.polygon(screen, (104, 102, 120), [(x - 20, y - 13), (x + 15, y - 17), (x + 20, y + 1), (x - 17, y + 7)])
                pg.draw.line(screen, (164, 150, 148), (x - 17, y - 13), (x + 14, y - 16), 2)
            for dy in (-8, -3, 2):
                pg.draw.line(screen, (86, 67, 70), (x - 10, y + dy), (x + 8, y + dy - 2), 2)

        for Worldx, Worldy in LAMPS:
            x, y = camera.apply(Worldx, Worldy)
            screen.blit(self.lamp, (x - 36, y - 36))

    def Drawcourtyards(self, screen, camera):

        # Short vertical faces sit below the bright top ledges.
        for Worldx, Worldy, width in [(10880, 8230, 380), (10880, 10135, 520), (8640, 10520, 480), (10880, 12700, 420)]:
            x, y = camera.apply(Worldx, Worldy)
            left = x - width // 2
            pg.draw.polygon(screen, (30, 31, 47), [(left, y + 25), (left + width, y + 25), (left + width + 18, y + 59), (left + 14, y + 59)])
            pg.draw.rect(screen, (46, 43, 61), (left, y, width, 37))
            for course in range(3):
                Rowy = y + course * 12
                for offset in range(-16 * (course % 2), width, 32):
                    start = max(0, offset)
                    length = min(offset + 30, width) - start
                    if length <= 0:
                        continue
                    shade = 11 * ((offset + course * 3) % 5) // 4
                    stone = pg.Rect(left + start, Rowy, length, 10)
                    pg.draw.rect(screen, (72 + shade, 70 + shade, 92 + shade), stone)
                    pg.draw.line(screen, (110 + shade, 105 + shade, 120 + shade), stone.topleft, stone.topright, 2)
                    pg.draw.line(screen, (54, 50, 72), (stone.left + length // 2, stone.y + 6), (stone.right - 2, stone.y + 7), 2)

        x, y = camera.apply(10880, 11420)
        pg.draw.rect(screen, (31, 37, 51), (x - 34, y - 32, 68, 58))
        pg.draw.rect(screen, (103, 84, 68), (x - 28, y - 29, 56, 43))
        for offset, length in [(-17, 27), (-6, 22), (5, 17), (16, 12)]:
            pg.draw.rect(screen, (190, 151, 91), (x + offset, y - 21, 6, length))
        if self.Chimerung:
            for offset in (-52, 52):
                screen.blit(self.lamp, (x + offset - 36, y - 36))

    def interact(self, player):

        readable = self.Nearbyreadable(player)
        if readable and readable[0] == "Strike the rehearsal chime":
            self.Chimerung = True
        return readable

    def Renderlighting(self, screen, camera):

        for x, y in [(10880, 10580), (8640, 10880), (13120, 10880), (10880, 13010)]:
            px, py = camera.apply(x, y)
            screen.blit(self.Coolpool, (px - 160, py - 160))
        for x, y in LAMPS:
            px, py = camera.apply(x, y)
            screen.blit(self.Lanternglow, (px - 108, py - 108))

    def blocks(self, x, y, radius):

        for base in TERRACEBASES:
            if base.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        for stone in self.masonry:
            if stone.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        for name, Centerx, Centery, width, height in LANDMARKS:
            base = pg.Rect(Centerx - width // 2, Centery - height // 2, width, height)
            if base.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        for Benchx, Benchy in BENCHES:
            bench = pg.Rect(Benchx - 48, Benchy - 13, 96, 28)
            if bench.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def Drawfloor(self, screen, rect, view, origin, room):

        visible = rect.clip(view)
        if not visible.width or not visible.height:
            return
        tile = self.floors[0][1]
        for name, floor in self.floors:
            if room == name:
                tile = floor
                break
        screen.set_clip(visible)
        Startx = visible.left - (visible.left - origin[0]) % 256
        Starty = visible.top - (visible.top - origin[1]) % 256
        for y in range(Starty, visible.bottom, 256):
            for x in range(Startx, visible.right, 256):
                screen.blit(tile, (x, y))
        screen.set_clip(view)

    def render(self, screen, camera):

        self.Drawmasonry(screen, camera)
        self.Drawfurnishings(screen, camera)
        self.Drawcourtyards(screen, camera)
        x, y = camera.apply(SHRINEX, SHRINEY)
        if self.shrine is not None:
            screen.blit(self.shrine, self.shrine.get_rect(center=(x, y)))

    def Nearbyreadable(self, player):

        for x, y, label, message in READABLES:
            if abs(player.x - x) < 160 and abs(player.y - y) < 135:
                return label, message
        return None






