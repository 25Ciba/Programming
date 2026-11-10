import pygame as pg
from Ruins import RuinsArt, RuinsProp

GUITARARENAX = 1220
GUITARARENAY = 10880

GUITARHABITATS = [
    ("Copper Crawler", "Common", 3320, 10520),
    ("Copper Crawler", "Common", 3430, 10440),
    ("Rustwing Bat", "Strong", 3450, 10600),
    ("Copper Crawler", "Common", 4320, 11160),
    ("Copper Crawler", "Common", 4460, 11260),
    ("Rustwing Bat", "Strong", 4200, 11280),
    ("Rustwing Bat", "Strong", 3710, 8400),
    ("Copper Crawler", "Common", 3930, 8320),
    ("Copper Crawler", "Common", 3980, 8500),
    ("Rustwing Bat", "Strong", 6080, 11160),
    ("Copper Crawler", "Common", 5910, 10760),
    ("Copper Crawler", "Common", 6250, 10760),
    ("Rustwing Bat", "Strong", 3590, 13270),
    ("Copper Crawler", "Common", 3680, 13400),
    ("Copper Crawler", "Common", 3940, 13350),
    ("Rustwing Bat", "Strong", 4090, 13280)
]

GUITARNOTES = [
    (3840, 10880, "Read the copper marker", "The western cavern carries every plucked note twice. The second echo comes from deeper down."),
    (3840, 8640, "Inspect the string spool", "Copper wire and silk. The luthier used both when the old strings went quiet."),
    (6080, 10635, "Pluck the workshop guitar", "The string still holds its tuning. A second note answers from the rock."),
    (3840, 13120, "Read the vault inventory", "Six strings delivered. One returned, worn smooth where a hand kept bending it."),
    (1220, 10380, "Read the recital marker", "Leave the lowest string ringing until the stone stops answering."),
    (3550, 11070, "Check the ore cart", "The luthier chose copper by tapping it and listening for a clean note."),
    (5750, 10680, "Inspect the instrument rack", "All the necks are marked for six strings. One has deep grooves from retuning."),
    (4090, 12890, "Pump the resonance bellows", "A pulse of warm air passes through the old tuning pipes."),
    (4100, 8670, "Check the wire crates", "The coils are sorted by pitch. The lowest strings are missing."),
    (3425, 12880, "Stoke the furnace", "Embers flare in the old smelter. The copper fittings start to hum."),
    (3270, 11545, "Turn the loading winch", "The cable tightens and the loading signals light up along the track."),
    (3470, 8220, "Inspect the copper seam", "The exposed copper rings faintly under your hand."),
    (6080, 11285, "Test the spare strings", "Three spare strings are still tuned. Someone was ready to come back.")
]

GUITARLANDMARKS = [
    (6080, 10490, 0, 166),
    (3600, 10690, 2, 66),
    (4080, 10690, 2, 66),
    (3550, 8680, 1, 120),
    (4010, 8850, 2, 62),
    (3540, 13160, 1, 132),
    (4060, 13020, 2, 70),
    (710, 10340, 2, 82),
    (1730, 10340, 2, 82),
    (710, 11420, 1, 164),
    (1730, 11420, 1, 164),
    (3550, 10965, 5, 146),
    (4090, 12780, 6, 130),
    (4100, 8560, 3, 120)
]


# Each group has a purpose and keeps the middle of the travel lanes clear.
GUITARGROUPS = [
    # String Hollow: loading bay, parked carts, and storage alongside the track.
    [
        (3550, 11470, 5, 141), (3380, 11025, 3, 79),
        (3360, 11122, 3, 72), (3390, 11375, 3, 88),
        (3710, 11330, 2, 60), (3710, 11520, 2, 60),
        (3040, 10210, 1, 154), (3040, 10320, 2, 58),
        (4560, 10210, 1, 154), (4560, 10320, 2, 58),
        (4600, 11540, 3, 100), (4720, 11540, 3, 92),
        (3380, 11495, 8, 135), (3230, 11430, 3, 100),
        (3230, 11295, 3, 86), (3710, 11015, 2, 58)
    ],
    # Low Tunnel: wire store on the east side and supports along the west.
    [
        (3335, 8290, 1, 116), (3335, 8520, 1, 116),
        (3335, 8780, 1, 116), (3415, 8570, 2, 50),
        (4250, 8560, 3, 87), (4240, 8755, 3, 88),
        (4120, 8755, 4, 104), (4160, 9060, 2, 58),
        (3470, 8120, 9, 156), (3625, 8110, 9, 104),
        (3350, 8120, 2, 54), (3530, 8320, 3, 70)
    ],
    # Workshop: leave the centre aisle open and mirror the work bays.
    [
        (5750, 10570, 4, 108), (6410, 10570, 4, 108),
        (5700, 10835, 3, 74), (6460, 10835, 3, 74),
        (5700, 11020, 2, 59), (6460, 11020, 2, 59),
        (5870, 11250, 4, 97), (6290, 11250, 4, 97)
    ],
    # Ember Vault: fuel stock and copper fittings along the bellows wall.
    [
        (4260, 12780, 3, 96), (4375, 12780, 3, 88),
        (4230, 12900, 2, 57), (4370, 12900, 3, 93),
        (3320, 12980, 1, 131), (3320, 13090, 2, 62),
        (3335, 13310, 3, 105), (3445, 13310, 3, 75),
        (4250, 13430, 3, 101), (4360, 13430, 3, 88),
        (3430, 12765, 7, 180), (3335, 12815, 3, 59),
        (3560, 12765, 3, 66), (3560, 12870, 2, 58)
    ],
    # Resonance Arena: only mirrored perimeter lights.
    [(755, 11560, 2, 72), (1685, 11560, 2, 72)]
]


def Creatureposeframes(folder, stem, scale, airborne):

    sprites = []
    for index in range(4):
        sprites.append(pg.image.load(folder / f"{stem}{index}.png").convert_alpha())
    # Use one scale for the full set so a wider stance stays wider.
    width = max(sprite.get_width() for sprite in sprites)
    height = max(sprite.get_height() for sprite in sprites)
    ratio = min(scale * 0.89 / width, scale * 0.79 / height)
    for index, sprite in enumerate(sprites):
        sprites[index] = pg.transform.scale(sprite, (round(sprite.get_width() * ratio), round(sprite.get_height() * ratio)))
    move = [(0, -2, 0), (0, -1, 1), (1, 1, 1), (1, 2, 0), (1, 1, 0), (0, 0, 1)]
    if airborne:
        move = [(0, 0, 2), (0, 0, 1), (1, 0, 0), (1, 0, -2), (2, 0, -1), (1, 0, 0)]
    animations = [
        [(0, 0, 0), (0, 0, 1)],
        move,
        [(2, 3, 0), (2, 5, 0), (2, 2, 1), (1, 1, 1), (1, 0, 0), (0, 0, 0)],
        [(0, -2, -2), (0, -4, -3), (1, -3, -2)],
        [(2, 1, 0), (3, 0, -2), (3, 0, -3)]
    ]
    if stem == "Scorpion":
        animations[1] = [(0, -2, 0), (0, -1, 1), (0, 0, 2), (1, 1, 1), (1, 2, 0), (1, 1, 0), (0, 0, 1), (0, -1, 0)]
        animations[2] = [(2, 2, 1), (2, 5, 1), (2, 3, 0), (2, 1, 0), (1, 0, 1), (0, 0, 0)]
        animations[3] = [(0, 0, 0), (1, -2, -1), (1, -4, -2), (2, -2, 0)]
    elif stem == "Snapper":
        animations[1] = [(0, -1, 0), (0, 0, 1), (1, 1, 2), (1, 2, 1), (1, 1, 0), (0, 0, 1)]
        animations[2] = [(2, 4, 1), (2, 8, 0), (2, 6, 0), (1, 3, 0), (1, 1, 0), (0, 0, 0)]
        animations[3] = [(0, 0, 0), (0, 0, -1), (1, 0, -2), (1, 0, -3)]
        animations[4] = [(2, 0, 0), (3, 0, -1), (3, 0, -2)]
    elif stem == "Wisp" and folder.parent.name == "HarpReservoir":
        animations[1] = [(0, 0, 0), (0, 0, 2), (1, 0, 4), (1, 0, 6), (1, -1, 4), (0, -1, 2)]
        animations[2] = [(2, 2, 5), (2, 4, 7), (2, 2, 5), (1, 1, 3), (1, 0, 2), (0, 0, 0)]
        animations[3] = [(0, 0, 0), (1, 0, 2), (1, 0, 4), (2, 0, 5)]
        animations[4] = [(1, 0, 2), (3, 0, 0), (3, 0, -3)]
    elif stem == "Spirit":
        animations[1] = [(0, 0, 0), (0, 1, 1), (1, 1, 2), (1, 0, 3), (1, -1, 2), (1, -1, 1), (0, 0, 0), (0, 1, -1)]
        animations[2] = [(2, 3, 3), (2, 4, 2), (2, 2, 1), (1, 0, 0), (1, -1, 1), (0, 0, 1)]
        animations[3] = [(0, 0, 1), (1, -1, 2), (1, -3, 4), (2, -2, 4)]
    result = []
    for animation in animations:
        rows = []
        for direction in range(4):
            frames = []
            for index, x, y in animation:
                frame = pg.Surface((scale, scale), pg.SRCALPHA)
                sprite = sprites[index]
                if (stem == "Scorpion" and direction == 2) or (stem != "Scorpion" and direction == 1):
                    sprite = pg.transform.flip(sprite, True, False)
                if direction == 1:
                    x = -x
                if stem == "Scorpion" and direction == 0:
                    x, y = x // 2, y - x
                elif stem == "Scorpion" and direction == 3:
                    sprite = pg.transform.rotate(pg.transform.flip(sprite, True, False), 85)
                    x, y = x // 2, y + x
                frame.blit(sprite, sprite.get_rect(midbottom=(scale // 2 + x, scale - 8 - y)))
                frames.append(frame)
            rows.append(frames)
        result.append(rows)
    return result


class GuitarArt(RuinsArt):

    def __init__(self, Imagefolder, Ruinsart):

        folder = Imagefolder / "GuitarCaverns"
        tile = pg.transform.scale(pg.image.load(folder / "Flagstones.png").convert(), (256, 256))
        self.floors = [("", tile)]
        for name, tint in [
            ("String Hollow", (223, 212, 205)),
            ("Low Tunnel", (181, 184, 194)),
            ("Resonance Arena", (202, 183, 178)),
            ("Luthier's Workshop", (245, 221, 198)),
            ("Ember Vault", (232, 192, 177))
        ]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.Wallface = Ruinsart.Wallface.copy()
        self.Wallface.fill((245, 183, 153), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.Wallface, (143, 104, 85), (0, 0, 128, 4))
        self.Wallbanner = Ruinsart.Wallbanner.copy()
        self.Wallbanner.fill((255, 204, 143), special_flags=pg.BLEND_RGB_MULT)
        self.Wallsconce = Ruinsart.Wallsconce
        self.Lanternglow = Ruinsart.Lanternglow
        self.sprites = []
        for name in ("Workbench", "Arch", "Lantern", "Spools", "Rack", "Cart", "Bellows", "Furnace", "Winch", "OreSeam"):
            self.sprites.append(pg.image.load(folder / f"{name}.png").convert_alpha())
        self.rosette = pg.image.load(folder / "ResonanceRosette.png").convert_alpha()
        self.rosette = pg.transform.scale(self.rosette, (1100, 850))
        self.props = []
        self.bases = []
        self.lanterns = []
        self.fragments = []
        self.Bellowsuntil = 0
        self.Furnaceuntil = 0
        self.Signalsuntil = 0

    def Addprop(self, x, y, index, width):

        sprite = self.sprites[index]
        height = round(sprite.get_height() * width / sprite.get_width())
        self.props.append(RuinsProp(x, y, 45, pg.transform.scale(sprite, (width, height))))
        self.bases.append(pg.Rect(x - width // 2 + 7, y - 20, width - 14, 42))
        if index == 2:
            self.lanterns.append((x, y))

    def populate(self):

        for x, y, index, width in GUITARLANDMARKS:
            self.Addprop(x, y, index, width)
        for group in GUITARGROUPS:
            for x, y, index, width in group:
                self.Addprop(x, y, index, width)
        # Chips and loose hardware sit next to their source props.
        for prop in self.props:
            for dx, dy, size in [(-23, 27, 6), (16, 31, 9), (29, 21, 4)]:
                self.fragments.append((prop.x + dx, prop.y + dy, size))

    def blocks(self, x, y, radius):

        for base in self.bases:
            if base.inflate(radius * 2, radius * 2).collidepoint(x, y):
                return True
        return False

    def Nearbyreadable(self, player):

        for x, y, label, message in GUITARNOTES:
            if abs(player.x - x) < 135 and abs(player.y - y) < 100:
                return label, message
        return None

    def interact(self, player):

        readable = self.Nearbyreadable(player)
        if readable and readable[0] == "Pump the resonance bellows":
            self.Bellowsuntil = pg.time.get_ticks() + 2200
        elif readable and readable[0] == "Stoke the furnace":
            self.Furnaceuntil = pg.time.get_ticks() + 5000
        elif readable and readable[0] == "Turn the loading winch":
            self.Signalsuntil = pg.time.get_ticks() + 5000
        return readable

    def Renderworkshopfloor(self, screen, camera):

        view = screen.get_rect()
        for Centerx, Centery, width, height in [(6080, 10510, 270, 138), (5750, 10600, 180, 132), (6410, 10600, 180, 132), (5740, 10875, 145, 120), (6420, 10875, 145, 120), (5870, 11270, 170, 104), (6290, 11270, 170, 104)]:
            x, y = camera.apply(Centerx, Centery)
            area = pg.Rect(x - width // 2, y - height // 2, width, height)
            if not view.colliderect(area):
                continue
            # Low, dark stone pads under the work surfaces.
            pad = pg.Surface(area.size, pg.SRCALPHA)
            w, h = pad.get_size()
            outline = [(0, 15), (15, 0), (w - 16, 0), (w - 1, 15), (w - 1, h - 15), (w - 16, h - 1), (15, h - 1), (0, h - 15)]
            pg.draw.polygon(pad, (41, 29, 35, 110), outline)
            pg.draw.lines(pad, (131, 91, 68, 140), True, outline, 2)
            for offset in range(26, width - 17, 30):
                pg.draw.line(pad, (113, 75, 61, 126), (offset, 5), (offset, 14), 2)
                pg.draw.line(pad, (113, 75, 61, 126), (offset, height - 13), (offset, height - 4), 2)
            screen.blit(pad, area)
            for dx, dy in [(-36, 31), (24, 39), (44, 17), (-19, 47)]:
                pg.draw.lines(screen, (151, 101, 64), False, [(x + dx, y + dy), (x + dx + 5, y + dy - 2), (x + dx + 9, y + dy + 1)], 2)
            for dx in (-54, 49):
                pg.draw.arc(screen, (150, 94, 62), (x + dx - 8, y + 28, 16, 10), 0.15, 5.6, 2)
                pg.draw.line(screen, (186, 130, 81), (x + dx + 6, y + 34), (x + dx + 13, y + 37), 1)
            for dx in (-47, 42):
                pg.draw.rect(screen, (45, 33, 41), (x + dx, y + 14, 10, 5))
                pg.draw.line(screen, (167, 121, 78), (x + dx + 1, y + 14), (x + dx + 6, y + 14), 2)

    def render(self, screen, camera):

        view = screen.get_rect()
        Regionx, Regiony = camera.apply(600, 7750)
        if not view.colliderect((Regionx, Regiony, 6500, 6500)):
            return
        Lightview = view.inflate(216, 216)
        self.Renderworkshopfloor(screen, camera)
        Arenacenter = camera.apply(GUITARARENAX, GUITARARENAY)
        Arenarect = self.rosette.get_rect(center=Arenacenter)
        if view.colliderect(Arenarect):
            screen.blit(self.rosette, Arenarect)
        # Both carts share one loading track. A crossbar marks the dead end.
        x, y = camera.apply(3550, 10965)
        for offset in range(-30, 546, 18):
            pg.draw.line(screen, (58, 41, 42), (x - 42, y + offset + 3), (x + 42, y + offset + 3), 7)
            pg.draw.line(screen, (111, 75, 52), (x - 39, y + offset), (x + 39, y + offset), 5)
        for rail in (-27, 27):
            pg.draw.line(screen, (64, 49, 54), (x + rail + 3, y - 32), (x + rail + 3, y + 552), 6)
            pg.draw.line(screen, (153, 111, 73), (x + rail, y - 32), (x + rail, y + 552), 3)
        pg.draw.line(screen, (120, 82, 56), (x - 37, y + 552), (x + 37, y + 552), 8)
        # Worn thresholds frame the workshop and vault entrances.
        for Worldx, Worldy, width in [(5670, 10880, 174), (3840, 12655, 235), (3840, 9120, 202)]:
            px, py = camera.apply(Worldx, Worldy)
            for offset in range(-width // 2, width // 2, 22):
                pg.draw.rect(screen, (69, 51, 51), (px + offset, py - 4, 20, 12))
                pg.draw.rect(screen, (126, 87, 64), (px + offset, py - 4, 20, 2))
        if self.Bellowsuntil > pg.time.get_ticks():
            x, y = camera.apply(4090, 12780)
            screen.blit(self.Lanternglow, (x - 108, y - 108))
            for i in range(5):
                shift = (pg.time.get_ticks() // 26 + i * 13) % 65
                pg.draw.rect(screen, (204, 122, 61), (x + i * 7 - 14, y - shift, 3, 3))
        now = pg.time.get_ticks()
        if self.Furnaceuntil > now:
            x, y = camera.apply(3430, 12765)
            screen.blit(self.Lanternglow, (x - 108, y - 105))
            for i in range(15):
                lift = (now // 24 + i * 11) % 97
                drift = (i * 19) % 73 - 36
                if i % 3:
                    colour = (211, 132, 67)
                else:
                    colour = (245, 179, 92)
                pg.draw.rect(screen, colour, (x + drift, y - lift, 2 + i % 2, 3))
        for i, Worldy in enumerate((11000, 11180, 11360, 11530)):
            x, y = camera.apply(3598, Worldy)
            pg.draw.rect(screen, (45, 39, 49), (x - 5, y - 5, 13, 13))
            active = self.Signalsuntil > now and (now // 180 + i) % 5 < 4
            if active:
                color = (245, 174, 83)
            else:
                color = (107, 77, 62)
            pg.draw.rect(screen, color, (x - 2, y - 2, 7, 7))
        for x, y, size in self.fragments:
            px, py = camera.apply(x, y)
            if view.collidepoint(px, py):
                pg.draw.rect(screen, (68, 49, 48), (px - 2, py + 2, size + 4, 4))
                pg.draw.line(screen, (126, 93, 73), (px, py), (px + size, py + 2), 2)
        for x, y in self.lanterns:
            px, py = camera.apply(x, y)
            if Lightview.collidepoint(px, py):
                screen.blit(self.Lanternglow, (px - 108, py - 122))
        for x, y, label, message in GUITARNOTES:
            px, py = camera.apply(x, y)
            pg.draw.ellipse(screen, (34, 31, 40), (px - 19, py - 4, 41, 14))
            pg.draw.polygon(screen, (135, 102, 77), [(px - 15, py - 7), (px + 13, py - 10), (px + 17, py + 3), (px - 12, py + 7)])
            pg.draw.line(screen, (198, 155, 98), (px - 10, py - 4), (px + 11, py - 6), 2)



