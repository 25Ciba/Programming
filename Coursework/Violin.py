import math
import pygame as pg
from Guitar import GuitarArt

VIOLIN_HABITATS = [
    ("Score Swarm", "Common", 10450, 17130), ("Score Swarm", "Common", 11310, 17130),
    ("Score Swarm", "Common", 10400, 18570), ("Score Swarm", "Common", 11360, 18570),
    ("Score Swarm", "Common", 10560, 15750), ("Score Swarm", "Common", 11200, 15750),
    ("Bowshade", "Strong", 10230, 17805), ("Bowshade", "Strong", 11530, 17805),
    ("Bowshade", "Strong", 8470, 18025), ("Bowshade", "Strong", 8850, 18025),
    ("Bowshade", "Strong", 12880, 18025), ("Bowshade", "Strong", 13260, 18025)
]

VIOLIN_NOTES = [
    (10880, 15630, "Read the tuning ledger", "The same string snapped every night. They stopped replacing it when it began to play on its own."),
    (10880, 17920, "Read the seating plan", "The front seats were kept empty so the violinist could hear the room breathe."),
    (8660, 17920, "Inspect the bow rack", "The spare bows still carry a fine dusting of rosin."),
    (13070, 17920, "Read the stage cue", "When the footlights dim, follow the brass inlay back to the main aisle."),
    (10880, 19690, "Play the waiting violin", "A single note hangs in the hall after you lift the bow.")
]

VIOLIN_PAIRS = [
    (10880, 15450, 435, 1, 115), (10880, 15940, 460, 2, 88),
    (10880, 17280, 540, 1, 144), (10880, 17470, 350, 2, 86),
    (10880, 17690, 870, 0, 105), (10880, 18045, 1140, 1, 146),
    (10880, 18270, 870, 0, 105), (10880, 18410, 350, 2, 86),
    (10880, 18660, 540, 1, 144),
    (8660, 17600, 425, 1, 107), (8660, 18140, 425, 2, 79),
    (13070, 17580, 370, 1, 107), (13070, 18230, 370, 2, 79),
    (10880, 19660, 865, 2, 100), (10880, 19950, 1040, 1, 154),
    (10880, 20480, 1040, 1, 154), (10880, 20880, 865, 2, 100)
]


class ViolinArt(GuitarArt):

    def __init__(self, image_folder, ruins_art):

        folder = image_folder / "ViolinHall"
        tile = pg.image.load(folder / "Flagstones.png").convert()
        self.floors = [("", tile)]
        for name, tint in [("Lantern Court", (229, 197, 201)), ("Tuning Room", (219, 205, 231)), ("West Backstage", (197, 170, 201)), ("East Backstage", (220, 183, 178)), ("Performance Hall", (247, 201, 193))]:
            floor = tile.copy()
            floor.fill(tint, special_flags=pg.BLEND_RGB_MULT)
            self.floors.append((name, floor))
        self.wall_face = ruins_art.wall_face.copy()
        self.wall_face.fill((206, 157, 180), special_flags=pg.BLEND_RGB_MULT)
        pg.draw.rect(self.wall_face, (125, 87, 105), (0, 0, 128, 4))
        self.wall_banner = ruins_art.wall_banner.copy()
        self.wall_banner.fill((242, 125, 153), special_flags=pg.BLEND_RGB_MULT)
        self.wall_sconce = ruins_art.wall_sconce
        self.lantern_glow = pg.Surface((180, 180), pg.SRCALPHA)
        for radius in range(88, 0, -3):
            alpha = round(65 * (1 - radius / 90) ** 2)
            pg.draw.circle(self.lantern_glow, (236, 157, 83, alpha), (90, 90), radius)
        self.sprites = [pg.image.load(folder / f"{name}.png").convert_alpha() for name in ("Violin", "Pillar", "Footlight")]
        self.props = []
        self.bases = []
        self.lanterns = []
        self.ringing_until = 0
        self.add_prop(10880, 19535, 0, 126)
        for center, y, offset, index, width in VIOLIN_PAIRS:
            self.add_prop(center - offset, y, index, width)
            self.add_prop(center + offset, y, index, width)

    def nearby_readable(self, player):

        for x, y, label, message in VIOLIN_NOTES:
            if math.hypot(x - player.x, y - player.y) < 78:
                return label, message
        return None

    def interact(self, player):

        readable = self.nearby_readable(player)
        if readable and readable[0] == "Play the waiting violin":
            self.ringing_until = pg.time.get_ticks() + 1900
        return readable

    def render(self, screen, camera):

        view = screen.get_rect()
        x, y = camera.apply(7800, 15000)
        if not view.colliderect((x, y, 6000, 6600)):
            return
        for start, end in [(17060, 18800), (19380, 20960)]:
            for x in (10660, 11100):
                left, top = camera.apply(x, start)
                pg.draw.line(screen, (105, 74, 79), (left, top), (left, top + end - start), 5)
                for offset in range(0, end - start, 62):
                    pg.draw.line(screen, (164, 119, 101), (left - 10, top + offset), (left + 10, top + offset), 3)
        x, y = camera.apply(10880, 20320)
        for width, height, colour in [(1380, 880, (113, 72, 86)), (1340, 840, (161, 114, 105)), (1280, 780, (108, 73, 85))]:
            pg.draw.ellipse(screen, colour, (x - width // 2, y - height // 2, width, height), 3)
        for x, y in self.lanterns:
            px, py = camera.apply(x, y)
            if view.colliderect((px - 90, py - 90, 180, 180)):
                screen.blit(self.lantern_glow, (px - 90, py - 90))
        for x, y, label, message in VIOLIN_NOTES:
            px, py = camera.apply(x, y)
            pg.draw.polygon(screen, (57, 40, 52), [(px - 13, py - 6), (px + 11, py - 9), (px + 15, py + 4), (px - 9, py + 8)])
            pg.draw.line(screen, (192, 150, 119), (px - 8, py - 4), (px + 9, py - 6), 2)
        now = pg.time.get_ticks()
        if self.ringing_until > now:
            px, py = camera.apply(10880, 19535)
            for i in range(3):
                radius = 24 + ((now // 18 + i * 22) % 65)
                pg.draw.arc(screen, (207, 150, 127), (px - radius, py - radius - 30, radius * 2, radius), 0.4, 2.8, 2)
