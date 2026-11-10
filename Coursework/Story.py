import math
from pathlib import Path
import pygame as pg
from BossMotion import Bosspixelframe
from StoryPictures import Storypicture

ASSETS = Path(__file__).resolve().parent / "Images" / "Story"
TUTORIAL = pg.Rect(2500, 27000, 1540, 1620)
ASCENT = pg.Rect(9400, 28500, 1100, 2520)
TUTORIALSTART = (3270, 28350)
ALTAR = (9950, 28860)
REQUIRED = ("Primordial Instrument Blueprint", "Piano Fragment", "Guitar Fragment", "Flute Fragment", "Cello Fragment", "Harp Fragment", "Violin Fragment")
PAGES = [
    ("Before the mist", "Once, six songs kept the dark from the roads.", "Even the smallest town knew its part."),
    ("The altar", "At the high altar, the six became one.", "Something beyond the stars bent down to listen."),
    ("The breaking", "When the players quarrelled, the chord broke.", "Six kept a fragment. The Keeper hid the plans."),
    ("The traveller", "The old song waits at Lantern Shelter.", "Bring the six fragments and the Keeper's plans.")
]
LESSONS = [
    ((3270, 28190), "Movement", "Use WASD or the arrow keys. Press Space to dash."),
    ((3020, 27900), "Combat", "Left click to attack. Right click to block. Try striking the practice post."),
    ((3520, 27900), "Class skills", "Aim with the mouse and use 1 to 4 for your class abilities. Skills spend mana."),
    ((3000, 27570), "Supplies", "Press I to inspect and equip items. Press H to drink a healing potion."),
    ((3540, 27570), "Exploration", "Press E to speak, read, open doors or collect loot. M opens your map.")
]
LOREPOINTS = [
    ((10880, 8740), "The first waystone", "The Keeper cut the first stair to the high altar. Seven seals remain on the waystone."),
    ((10880, 4400), "A tune under the ice", "The pianist froze the river to carry the first fragment home. The thaw never reached the chamber."),
    ((3840, 11380), "The luthier's debt", "The guitarist repaired the town's bells without asking payment. He refused to mend the broken chord."),
    ((17920, 11360), "The breath between notes", "The flutist left gaps in her part so the other towns could answer. The mist has filled those gaps."),
    ((3840, 18260), "The cellist's last seat", "The cellist waited until the hall was empty. The sand kept the shape of every chair."),
    ((17920, 18585), "The flood ledger", "The harpist heard an answering note beneath the water and followed it down."),
    ((10880, 18390), "The final programme", "The violinist reserved the last place on the stage for the person who could bring all six parts back.")
]


def Playprologue(display, screen, frame):

    images = [Storypicture(index) for index in range(len(PAGES))]
    font = pg.font.SysFont("consolas", 25, bold=True)
    small = pg.font.SysFont("consolas", 17)
    clock = pg.time.Clock()
    page = 0
    visible = 0.0
    panel = pg.Rect(139, 518, 922, 164)
    while page < len(PAGES):
        dt = clock.tick(60)/1000
        _, first, second = PAGES[page]
        length = len(first) + len(second)
        visible = min(length, visible + dt*47)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.VIDEORESIZE:
                scale = min(event.w / screen.get_width(), event.h / screen.get_height())
                frame.size = (round(screen.get_width() * scale), round(screen.get_height() * scale))
                frame.center = display.get_rect().center
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True
                if event.key == pg.K_SPACE:
                    if visible < length:
                        visible = length
                    else:
                        page += 1
                        visible = 0
                        break
        if page >= len(PAGES):
            break
        _, first, second = PAGES[page]
        length = len(first) + len(second)
        screen.fill((7, 5, 9))
        screen.blit(images[page], (384, 60))
        pg.draw.rect(screen, (224, 211, 196), panel, 3)
        count = int(visible)
        for index, line in enumerate((first[:count], second[:max(0, count-len(first))])):
            text = font.render(line, False, (238, 225, 208))
            screen.blit(text, (panel.x+32, panel.y+31+index*48))
        if visible >= length:
            x, y = panel.right-25, panel.bottom-21
            pg.draw.polygon(screen, (240, 184, 92), [(x-6, y-3), (x+6, y-3), (x, y+5)])
        hint = small.render(f"{page+1}/{len(PAGES)}   SPACE / CONTINUE     ESC / SKIP", False, (147, 123, 113))
        screen.blit(hint, hint.get_rect(midtop=(600, 712)))
        display.fill((0, 0, 0))
        display.blit(pg.transform.scale(screen, frame.size), frame)
        pg.display.flip()
    return True


class Story:

    def __init__(self, Gamemap):

        for name, room in [("Traveller's Passage", TUTORIAL), ("Primordial Ascent", ASCENT)]:
            Gamemap.rooms.append((name, 0, room))
            if room == ASCENT:
                Gamemap.Roomfloors.append((name, 0, pg.Rect(room.x, room.y, room.width, 565)))
                Gamemap.Roomfloors.append((name, 0, pg.Rect(room.centerx-206, room.y+540, 412, room.height-540)))
            else:
                Gamemap.Roomfloors.append((name, 0, room))
        self.deity = Bosspixelframe(pg.image.load(ASSETS / "Deity.png").convert_alpha())
        self.ending = None
        self.Testingfinale = False
        self.Practiceflash = 0
        self.Practicehit = False
        self.waystone = (10660, 8790)

    def target(self, player):

        x, y = player.x, player.y
        if TUTORIAL.collidepoint(x, y):
            if math.hypot(x-3270, y-27180) <= 94:
                return "Leave the training passage", "exit"
            for point, title, message in LESSONS:
                if math.hypot(x-point[0], y-point[1]) <= 85:
                    return title, message
        elif ASCENT.collidepoint(x, y):
            if math.hypot(x-ALTAR[0], y-ALTAR[1]) <= 105:
                return "Play the Primordial Instrument", "ending"
        else:
            if math.hypot(x-self.waystone[0], y-self.waystone[1]) <= 78:
                return "Examine the Primordial Waystone", "waystone"
            for point, title, message in LOREPOINTS:
                if math.hypot(x-point[0], y-point[1]) <= 68:
                    return title, message
        return None

    def interact(self, player, inventory, start):

        target = self.target(player)
        if not target:
            return None
        title, action = target
        if action == "exit":
            self.move(player, start)
            return "Lantern Shelter. The Keeper waits in the Overture Arena."
        if action == "waystone":
            missing = sum(inventory.get(item, 0) <= 0 for item in REQUIRED)
            if missing:
                return f"The waystone needs the Keeper's blueprint and all six fragments. Missing {missing} of seven."
            self.move(player, (9950, 30780))
            return "The seven seals open the Primordial Ascent. Follow the stairs to the altar."
        if action == "ending":
            if self.Testingfinale or all(inventory.get(item, 0) > 0 for item in REQUIRED):
                self.move(player, (9950, 29015))
                player.facing = 4
                self.ending = 0.0
                return "The Primordial Instrument is assembled."
            return "The instrument is incomplete."
        return action

    def move(self, player, point):

        player.x, player.y = point
        player.Attackstage = player.Attackanimationtime = player.Blocktime = player.Dashtime = 0
        player.Attackqueued = False
        player.Attacktargets.clear()
        player.shots.clear()
        player.Dashtrail.clear()
        if player.powers:
            player.powers.Leavearea()

    def practice(self, player):

        if TUTORIAL.collidepoint(player.x, player.y) and math.hypot(player.x-3270, player.y-27940)<235:
            self.Practicehit = True
            self.Practiceflash = 0.32

    def update(self, dt):

        self.Practiceflash = max(0, self.Practiceflash-dt)

    def render(self, screen, camera):

        view = screen.get_rect()
        for room in (TUTORIAL, ASCENT):
            x, y = camera.apply(room.x, room.y)
            bounds = pg.Rect(x, y, room.width, room.height)
            if not view.colliderect(bounds):
                continue
            if room == TUTORIAL:
                pg.draw.rect(screen, (66, 59, 79), bounds, 9)
            if room == ASCENT:
                pg.draw.rect(screen, (66, 59, 79), (x, y, room.width, 565), 7)
                cx, _ = camera.apply(ALTAR[0], ALTAR[1])
                pg.draw.rect(screen, (55, 49, 66), (cx-168, y+180, 336, room.height-285))
                for height in range(545, room.height-130, 44):
                    sy = y+height
                    if -40<sy<view.bottom+40:
                        pg.draw.rect(screen, (94, 82, 99), (cx-170, sy, 340, 29))
                        pg.draw.line(screen, (151, 134, 126), (cx-169, sy), (cx+169, sy), 2)
                        for side in (-1, 1):
                            pg.draw.rect(screen, (139, 106, 88), (cx+side*159-4, sy, 8, 23))
                ax, ay = camera.apply(*ALTAR)
                pg.draw.ellipse(screen, (140, 117, 105), (ax-174, ay-105, 348, 210), 3)
                pg.draw.rect(screen, (48, 39, 56), (ax-62, ay-31, 124, 55))
                pg.draw.rect(screen, (144, 109, 92), (ax-58, ay-31, 116, 19))
                pg.draw.rect(screen, (225, 179, 103), (ax-40, ay-28, 80, 3))
                pg.draw.lines(screen, (217, 170, 101), True, [(ax-13, ay-17), (ax-2, ay-46), (ax+15, ay-37), (ax+12, ay-17)], 3)
                for offset in (-5, 0, 5):
                    pg.draw.line(screen, (239, 207, 149), (ax+offset, ay-20), (ax+offset+4, ay-37), 1)
        markers = [(point, (184, 153, 115)) for point, _, _ in LESSONS + LOREPOINTS]
        markers.extend([(self.waystone, (218, 178, 103)), ((3270, 27180), (165, 200, 179))])
        for point, colour in markers:
            x, y=camera.apply(*point)
            if view.inflate(35, 35).collidepoint(x, y):
                pg.draw.rect(screen, (32, 27, 44), (x-14, y-11, 28, 19))
                pg.draw.rect(screen, colour, (x-11, y-8, 22, 11), 2)
        x, y=camera.apply(3270, 27940)
        if view.inflate(50, 50).collidepoint(x, y):
            pg.draw.ellipse(screen, (39, 32, 45), (x-28, y-6, 56, 18))
            pg.draw.rect(screen, (102, 65, 57), (x-8, y-50, 16, 55))
            pg.draw.circle(screen, (247, 212, 160) if self.Practiceflash else (160, 117, 86), (x, y-32), 22)
            pg.draw.circle(screen, (94, 60, 67), (x, y-32), 12, 3)

    def finish(self, screen, camera, player, dt):

        self.ending += dt
        time = self.ending
        if time >= 6.5:
            screen.fill((0, 0, 0))
            if time >= 11.5:
                title = pg.font.Font(None, 58).render("The End", True, (235, 220, 190))
                thanks = pg.font.Font(None, 29).render("Thank you for playing", True, (211, 197, 177))
                screen.blit(title, title.get_rect(center=(600, 188)))
                screen.blit(thanks, thanks.get_rect(center=(600, 243)))
            return time < 21.5
        ax, ay = camera.apply(*ALTAR)
        progress = min(1, max(0, (time-0.6)/2.8))
        if progress:
            spirit = self.deity.copy()
            spirit.set_alpha(round(255*progress))
            descent = round((1-progress)**2 * 155)
            screen.blit(spirit, spirit.get_rect(midbottom=(ax, ay+11-descent)))
        if time >= 2.0:
            px, py = camera.apply(player.x, player.y)
            glow = pg.Surface(screen.get_size(), pg.SRCALPHA)
            strength = min(1, (time-2)/1.8)
            for radius in range(122, 8, -9):
                alpha = round(strength * (1-radius/130)*34)
                pg.draw.circle(glow, (250, 194, 88, alpha), (px, py-22), radius)
            screen.blit(glow, (0, 0))
        if time >= 4.0:
            flash = pg.Surface(screen.get_size(), pg.SRCALPHA)
            if time <= 5.55:
                flash.fill((255, 255, 255, round(255*min(1, (time-4)/1.2))))
            else:
                flash.fill((0, 0, 0, round(255*min(1, (time-5.55)/.95))))
                screen.fill((255, 255, 255))
            screen.blit(flash, (0, 0))
        return True
