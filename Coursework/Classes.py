import pygame as pg
import random
import math
from BossArena import ArenaArt
from MobMotion import Facingrow, Mobframes
from BossMotion import Loadbosssteps, Originalkeepersteps, Bossposeoffset, Bosspixelframe, Bossidleframes
from Violin import ViolinArt, VIOLINHABITATS
from Harp import HarpArt, HARPHABITATS
from Cello import CelloArt, CELLOHABITATS
from Flute import FluteArt, FLUTEHABITATS
from Guitar import GuitarArt, GUITARHABITATS
from Frost import FrostArt, FROSTHABITATS
from RogueArt import RogueArt, DIRECTIONS
from pathlib import Path
from Settlements import Settlements, WORLDWIDTH, WORLDHEIGHT
from Story import ALTAR, ASCENT, Story
from Menus import held
from Items import ITEMS, STARTSHIELD, STARTWEAPON
from Ruins import RuinsArt, RuinsGate, GATEX, GATEY, HABITATS, Creatureframes
from DungeonLayout import REGIONS, ROOMS, CORRIDORS, GATES, BOSSROOMS, STARTX, STARTY

###

IMAGEFOLDER = Path(__file__).resolve().parent / "Images"

MAPWIDTH = WORLDWIDTH
MAPHEIGHT = WORLDHEIGHT

###

def Loadenemyanimation(Slimenumber, action, scale=128):

    path = IMAGEFOLDER / f"Enemy/Slime{Slimenumber}/With_shadow/Slime{Slimenumber}_{action}_with_shadow.png"
    sheet = pg.image.load(path).convert_alpha()
    Framesize = 64
    Framesbydirection = []
    for row in range(sheet.get_height() // Framesize):
        Rowframes = []
        for x in range(0, sheet.get_width(), Framesize):
            frame = sheet.subsurface((x, row * Framesize, Framesize, Framesize)).copy()
            frame = pg.transform.scale(frame, (scale, scale))
            Rowframes.append(frame)
        Framesbydirection.append(Rowframes)
    return Framesbydirection

#================================================

#Map

#================================================

# Map

class Map:

    def __init__(self):

        self.gate = RuinsGate()
        self.Ruinsart = RuinsArt(IMAGEFOLDER)
        self.Frostart = FrostArt(IMAGEFOLDER, self.Ruinsart)
        self.Guitarart = GuitarArt(IMAGEFOLDER, self.Ruinsart)
        self.Fluteart = FluteArt(IMAGEFOLDER, self.Ruinsart)
        self.Celloart = CelloArt(IMAGEFOLDER, self.Ruinsart)
        self.Harpart = HarpArt(IMAGEFOLDER, self.Ruinsart)
        self.Violinart = ViolinArt(IMAGEFOLDER, self.Ruinsart)
        self.rooms = []
        self.Roomfloors = []
        self.corridors = []
        for name, region, x, y, width, height in ROOMS:
            rect = pg.Rect(x, y, width, height)
            self.rooms.append((name, region, rect))
            shape = (len(self.rooms) + region) % 4
            if name in ("Overture Arena", "Resonance Arena", "Flute Hall", "Cello Amphitheatre", "Harp Chamber", "Performance Hall"):
                shape = 1
            for floor in self.Roomshape(rect, shape):
                self.Roomfloors.append((name, region, floor))
        for region, x, y, width, height in CORRIDORS:
            self.corridors.append((region, pg.Rect(x, y, width, height)))
        self.Arenaart = ArenaArt(self.rooms, IMAGEFOLDER)
        self.Ruinsart.Placemasonry(self.Roomfloors, self.corridors)
        self.Frostart.populate(self.Roomfloors, self.corridors)
        self.Guitarart.populate()
        self.Ruinsedges = []
        self.Frostedges = []
        self.Guitaredges = []
        self.Fluteedges = []
        self.Celloedges = []
        self.Harpedges = []
        self.Violinedges = []
        for name, region, rect in self.Roomfloors:
            if region == 0:
                self.Addruinsedges(rect, self.Ruinsedges)
            elif region == 1:
                self.Addruinsedges(rect, self.Frostedges)
            elif region == 2:
                self.Addruinsedges(rect, self.Guitaredges)
            elif region == 3:
                self.Addruinsedges(rect, self.Fluteedges)
            elif region == 4:
                self.Addruinsedges(rect, self.Celloedges)
            elif region == 5:
                self.Addruinsedges(rect, self.Harpedges)
            elif region == 6:
                self.Addruinsedges(rect, self.Violinedges)
        for region, rect in self.corridors:
            if region == 0:
                self.Addruinsedges(rect, self.Ruinsedges)
            elif region == 1:
                self.Addruinsedges(rect, self.Frostedges)
            elif region == 2:
                self.Addruinsedges(rect, self.Guitaredges)
            elif region == 3:
                self.Addruinsedges(rect, self.Fluteedges)
            elif region == 4:
                self.Addruinsedges(rect, self.Celloedges)
            elif region == 5:
                self.Addruinsedges(rect, self.Harpedges)
            elif region == 6:
                self.Addruinsedges(rect, self.Violinedges)

        self.settlements = Settlements(self)
        self.story = Story(self)

    #

    def Roomshape(self, rect, shape):

        x, y, width, height = rect
        Insetx = width // 6
        Insety = height // 6
        if shape == 0:
            # Stepped oval.
            return [
                pg.Rect(x + Insetx * 2, y, width - Insetx * 4, height),
                pg.Rect(x + Insetx, y + Insety // 2, width - Insetx * 2, height - Insety),
                pg.Rect(x, y + Insety * 2, width, height - Insety * 4)
            ]
        if shape == 1:
            # Wide middle with clipped corners.
            return [
                pg.Rect(x + Insetx, y, width - Insetx * 2, height),
                pg.Rect(x, y + Insety, width, height - Insety * 2)
            ]
        if shape == 2:
            # Offset chambers, with a notch in opposite corners.
            return [
                pg.Rect(x, y, width - Insetx, height - Insety),
                pg.Rect(x + Insetx, y + Insety, width - Insetx, height - Insety)
            ]
        # Broad lower chamber with a narrow upper end.
        return [
            pg.Rect(x + Insetx, y, width - Insetx * 2, height),
            pg.Rect(x, y + Insety * 2, width, height - Insety * 3)
        ]

    #

    def Iswalkable(self, x, y):

        for name, region, rect in self.Roomfloors:
            if rect.collidepoint(x, y):
                return True
        for region, rect in self.corridors:
            if rect.collidepoint(x, y):
                return True
        return False

    #

    def Locationname(self, x, y):

        for name, region, rect in self.Roomfloors:
            if rect.collidepoint(x, y):
                return f"{REGIONS[region][0]}  /  {name}"
        return "Connecting passage"

    #

    def Canmovecircle(self, x, y, radius):

        # Check the gate and the solid objects in each region
        if self.gate.blocks(x, y, radius):
            return False
        if self.Ruinsart.blocks(x, y, radius):
            return False
        if self.Frostart.blocks(x, y, radius):
            return False
        if self.Guitarart.blocks(x, y, radius):
            return False
        if self.Fluteart.blocks(x, y, radius):
            return False
        if self.Celloart.blocks(x, y, radius):
            return False
        if self.Harpart.blocks(x, y, radius):
            return False
        if self.Violinart.blocks(x, y, radius):
            return False
        if self.Arenaart.blocks(x, y, radius):
            return False
        if hasattr(self, "settlements") and self.settlements.blocks(x, y, radius):
            return False
        points = [(x - radius, y), (x + radius, y), (x, y - radius), (x, y + radius)]
        for Pointx, Pointy in points:
            if not self.Iswalkable(Pointx, Pointy):
                return False
        return True

    #

    def Clearenemypath(self, x, y, Targetx, Targety, radius):

        distance = math.hypot(Targetx - x, Targety - y)
        steps = max(1, math.ceil(distance / 16))
        for step in range(1, steps + 1):
            Checkx = x + (Targetx - x) * step / steps
            Checky = y + (Targety - y) * step / steps
            if not self.Canmovecircle(Checkx, Checky, radius):
                return False
        return True

    #

    def Randomenemyspawnposition(self, Playerx=None, Playery=None):

        for attempt in range(100):
            name, region, rect = random.choice(self.rooms)
            x = random.randint(rect.left + 50, rect.right - 50)
            y = random.randint(rect.top + 50, rect.bottom - 50)
            if not self.Canmovecircle(x, y, 40):
                continue
            if Playerx is None or Playery is None:
                return x, y
            distance = math.hypot(x - Playerx, y - Playery)
            if distance > 900:
                return x, y
        return rect.center

    #

    def render(self, screen, camera):
        view = screen.get_rect()
        origin = camera.apply(0, 0)
        for region, rect in self.corridors:
            Wallrect = pg.Rect(camera.apply(rect.x, rect.y), rect.size).inflate(24, 24)
            if view.colliderect(Wallrect):
                pg.draw.rect(screen, (26, 29, 42), Wallrect)
        for name, region, rect in self.Roomfloors:
            Wallrect = pg.Rect(camera.apply(rect.x, rect.y), rect.size).inflate(24, 24)
            if view.colliderect(Wallrect):
                pg.draw.rect(screen, (26, 29, 42), Wallrect)
        for region, rect in self.corridors:
            Visiblerect = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if view.colliderect(Visiblerect):
                colour = (48, 52, 65)
                if region >= 0:
                    red, green, blue = REGIONS[region][1]
                    colour = (red * 3 // 4, green * 3 // 4, blue * 3 // 4)
                pg.draw.rect(screen, colour, Visiblerect)
                if region == 0:
                    self.Ruinsart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 1:
                    self.Frostart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 2:
                    self.Guitarart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 3:
                    self.Fluteart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 4:
                    self.Celloart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 5:
                    self.Harpart.Drawfloor(screen, Visiblerect, view, origin, '')
                elif region == 6:
                    self.Violinart.Drawfloor(screen, Visiblerect, view, origin, '')
        for name, region, rect in self.Roomfloors:
            Visiblerect = pg.Rect(camera.apply(rect.x, rect.y), rect.size)
            if view.colliderect(Visiblerect):
                pg.draw.rect(screen, REGIONS[region][1], Visiblerect)
                if region == 0:
                    self.Ruinsart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 1:
                    self.Frostart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 2:
                    self.Guitarart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 3:
                    self.Fluteart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 4:
                    self.Celloart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 5:
                    self.Harpart.Drawfloor(screen, Visiblerect, view, origin, name)
                elif region == 6:
                    self.Violinart.Drawfloor(screen, Visiblerect, view, origin, name)
        self.Ruinsart.Drawwalls(screen, camera, self.Ruinsedges)
        self.Frostart.Drawwalls(screen, camera, self.Frostedges)
        self.Guitarart.Drawwalls(screen, camera, self.Guitaredges)
        self.Fluteart.Drawwalls(screen, camera, self.Fluteedges)
        self.Celloart.Drawwalls(screen, camera, self.Celloedges)
        self.Harpart.Drawwalls(screen, camera, self.Harpedges)
        self.Violinart.Drawwalls(screen, camera, self.Violinedges)
        for Firstregion, Secondregion, x, y in GATES:
            if (x, y) == (GATEX, GATEY):
                continue
            Gatex, Gatey = camera.apply(x, y)
            pg.draw.rect(screen, (197, 168, 105), (Gatex - 6, Gatey - 6, 12, 12))
        self.Ruinsart.render(screen, camera)
        self.Ruinsart.Renderlighting(screen, camera)
        self.Frostart.render(screen, camera)
        self.Guitarart.render(screen, camera)
        self.Fluteart.render(screen, camera)
        self.Celloart.render(screen, camera)
        self.Harpart.Renderarena(screen, camera)
        self.Harpart.render(screen, camera)
        self.Violinart.render(screen, camera)
        self.gate.render(screen, camera)
        self.Arenaart.render(screen, camera)
        self.settlements.render(screen, camera)
        self.story.render(screen, camera)

    #

    def Addruinsedges(self, rect, edges):

        # Group exposed floor boundaries into continuous wall runs.
        for side, boundary, outside in [("north", rect.top, rect.top - 1), ("south", rect.bottom, rect.bottom)]:
            start = None
            for x in range(rect.left, rect.right + 1):
                exposed = x < rect.right and not self.Iswalkable(x, outside)
                if exposed and start is None:
                    start = x
                if not exposed and start is not None:
                    edges.append((start, boundary, x - start, side))
                    start = None
        for side, boundary, outside in [("west", rect.left, rect.left - 1), ("east", rect.right, rect.right)]:
            start = None
            for y in range(rect.top, rect.bottom + 1):
                exposed = y < rect.bottom and not self.Iswalkable(outside, y)
                if exposed and start is None:
                    start = y
                if not exposed and start is not None:
                    edges.append((boundary, start, y - start, side))
                    start = None

    #

#================================================

# Player

#================================================

# Player

class Player(pg.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.clan = "Rogue"
        self.progress = None
        self.x = STARTX
        self.y = STARTY
        self.speed = 520
        self.size = 30
        self.visionRadius = 300

        self.Maxhp = 100
        self.Currenthp = self.Maxhp
        self.Maxmana = 100
        self.Currentmana = self.Maxmana

        self.defence = 50

        self.attack = 20
        self.Attackrange = 100
        self.Attackcooldown = 0
        self.Attackdelay = 0.42

        self.Maxlives = 7
        self.Currentlives = self.Maxlives
        self.facing = 0
        self.Attackfacing = 0
        self.Rangedaim = pg.Vector2(0, 1)
        self.Walkdistance = 0
        self.stride = 0
        self.Idletime = 0
        self.moving = False
        self.Animationtime = 0
        self.Attackanimationtime = 0
        self.enemies = []
        self.Attacktargets = []
        self.Attackstage = 0
        self.Attackqueued = False
        self.Swingduration = self.Attackdelay
        self.Attackmap = None

        self.Blockduration = 0.5
        self.Blockcooldownlength = 1.5
        self.Blocktime = 0
        self.Blockcooldown = 0

        self.Dashduration = 0.5
        self.Dashcooldownlength = 2.0
        self.Dashspeed = 840
        self.Dashtime = 0
        self.Dashcooldown = 0
        self.Dashdirection = pg.Vector2(0, 0)

        self.powers = None
        self.Mainhand = STARTWEAPON
        self.Offhand = STARTSHIELD
        self.armour = None
        self.charm = None
        self.Guardmultiplier = 0.2
        self.shots = []
        self.art = RogueArt()
        self.Dashtrail = []
        self.Dashbraking = False

    #

    def Directionkeys(self):

        keys = pg.key.get_pressed()
        dx = int(held(keys, "Move right", pg.K_RIGHT)) - int(held(keys, "Move left", pg.K_LEFT))
        dy = int(held(keys, "Move down", pg.K_DOWN)) - int(held(keys, "Move up", pg.K_UP))
        return dx, dy

    #

    def Beginblock(self):

        if self.Blockcooldown > 0 or self.Dashtime > 0 or self.Attackanimationtime > 0:
            return False
        self.Blocktime = self.Blockduration
        self.Blockcooldown = self.Blockcooldownlength
        return True

    #

    def Begindash(self):

        if self.powers and (self.powers.familiar is not None or self.powers.active("Stab")):
            return False

        if self.Dashcooldown > 0 or self.Dashtime > 0 or self.Blocktime > 0:
            return False
        direction = self.Directionkeys()
        if direction != (0, 0):
            self.facing = DIRECTIONS.index(direction)
        self.Dashdirection = pg.Vector2(DIRECTIONS[self.facing]).normalize()
        self.Dashtime = self.Dashduration
        self.Dashcooldown = self.Dashcooldownlength
        self.Attackanimationtime = 0
        self.Attacktargets = []
        self.Attackstage = 0
        self.Attackqueued = False
        self.Dashtrail = []
        self.Dashbraking = False
        return True

    #

    def keybinds(self, dt, Gamemap):

        if self.powers and (self.powers.familiar is not None or self.powers.active("Stab")):
            self.moving = False
            self.Settlestride(dt)
            return

        if self.Dashtime > 0:
            self.Movedash(dt, Gamemap)
            self.stride = 0
            self.Idletime = 0
            return
        direction = self.Directionkeys()
        self.moving = False
        if direction == (0, 0):
            self.Settlestride(dt)
            return
        if self.Attackanimationtime <= 0 and self.Blocktime <= 0:
            self.facing = DIRECTIONS.index(direction)
        speed = self.speed * (self.powers.Speedfactor() if self.powers else 1)
        if self.Attackanimationtime > 0:
            speed *= 0.52
        move = pg.Vector2(direction).normalize() * speed * dt
        Oldx, Oldy = self.x, self.y
        self._move(move.x, move.y, Gamemap)
        distance = math.hypot(self.x - Oldx, self.y - Oldy)
        self.Walkdistance += distance
        self.moving = distance > 0
        if self.moving:
            self.stride = min(1, self.stride + dt / 0.12)
            self.Idletime = 0
        else:
            self.Settlestride(dt)

    def Settlestride(self, dt):

        self.stride = max(0, self.stride - dt / 0.16)
        if self.stride == 0:
            self.Walkdistance = 0
            self.Idletime += dt

    def Movementframe(self):

        return self.art.Movementframe(self.facing, self.Walkdistance, self.stride, self.Idletime)


    #

    def Movedash(self, dt, Gamemap):

        self.moving = False
        elapsed = self.Dashduration - self.Dashtime
        self.Dashtime = max(0, self.Dashtime - dt)
        if elapsed < 0.08 or self.Dashbraking:
            return
        speed = self.Dashspeed
        if self.Dashtime < 0.10:
            speed *= self.Dashtime / 0.10
        move = self.Dashdirection * speed * dt
        steps = max(1, math.ceil(move.length() / 10))
        self.Dashtrail.append((self.x, self.y))
        self.Dashtrail = self.Dashtrail[-6:]
        for step in range(steps):
            x = self.x + move.x / steps
            y = self.y + move.y / steps
            if not self.Canmoveto(x, y, Gamemap):
                self.Dashbraking = True
                self.Dashtime = min(self.Dashtime, 0.10)
                break
            self.x, self.y = x, y

    #

    def _move(self, Movex, Movey, Gamemap):

        if self.Canmoveto(self.x + Movex, self.y, Gamemap):
            self.x += Movex
        if self.Canmoveto(self.x, self.y + Movey, Gamemap):
            self.y += Movey

    #

    def Canmoveto(self, x, y, Gamemap):

        if not Gamemap.Canmovecircle(x, y, self.size):
            return False
        if hasattr(Gamemap, "Arenaart") and not Gamemap.Arenaart.Allowscrossing(self, x, y):
            return False
        Oldoverlap = 0
        Newoverlap = 0
        for enemy in self.enemies:
            if enemy.Currenthp <= 0:
                continue
            after = enemy.Bodyoverlap(x, y, self.size)
            if after <= 0:
                continue
            before = enemy.Bodyoverlap(self.x, self.y, self.size)
            if before <= 0:
                return False
            Oldoverlap += before
            Newoverlap += after
        # Let the Rogue back out if an enemy is already overlapping.
        return Newoverlap == 0 or Newoverlap < Oldoverlap

    # An existing overlap must get smaller. New overlaps still block movement.
        return Newoverlap == 0 or Newoverlap < Oldoverlap

    #

    def render(self, camera):

        _, _, crouch, glide = self.art.poses[self.facing]
        x, y = camera.apply(self.x, self.y)
        frame = self.Movementframe()
        for position, direction, remaining, damage, colour, targets, Gamemap in self.shots:
            point = pg.Vector2(camera.apply(position.x, position.y))
            pg.draw.line(self.screen, colour, point - direction * 12, point, 3)
        if self.Dashtime > 0:
            if self.Dashtime > self.Dashduration - 0.08 or self.Dashtime < 0.10:
                frame = crouch
            else:
                frame = glide
            side = pg.Vector2(-self.Dashdirection.y, self.Dashdirection.x)
            for i, (Worldx, Worldy) in enumerate(self.Dashtrail):
                px, py = camera.apply(Worldx, Worldy)
                start = pg.Vector2(px, py) + side * ((i % 3) - 1) * 9
                end = start - self.Dashdirection * (14 + i * 4)
                pg.draw.line(self.screen, (73 + i * 12, 74 + i * 10, 110 + i * 13), start, end, 2 + i // 3)
        elif self.Blocktime > 0 or (self.powers and self.powers.active("Sneak")):
            frame = crouch
        elif self.Attackanimationtime > 0:
            progress = 1 - self.Attackanimationtime / self.Swingduration
            Framenumber = min(23, int(progress * 24))
            if self.Attackstage == 2:
                frames = self.art.Returncuts
            else:
                frames = self.art.attacks
            frame = frames[self.Attackfacing][Framenumber]
            frame = self.art.Heldgear(frame, self.Attackfacing, None, self.Offhand)
            self.screen.blit(frame, frame.get_rect(center=(x, y)))
            return
        frame = self.art.Heldgear(frame, self.facing, self.Mainhand, self.Offhand, self.Blocktime > 0)
        self.screen.blit(frame, frame.get_rect(midbottom=(x, y + 24)))
        if self.Blocktime > 0:
            direction = pg.Vector2(DIRECTIONS[self.facing]).normalize()
            self.art.guard(self.screen, x, y, direction, 1 - self.Blocktime / self.Blockduration)

    #

    def pvector2(self):
        return pg.Vector2(self.x, self.y)

    #

    def pvisionRadius(self):
        return self.visionRadius

    #

    def Takedamage(self, Incomingdamage):

        if self.powers and self.powers.active("Shield"):
            return 0
        Damagemultiplier = self.Maxhp / (self.Maxhp + self.defence)
        if self.powers and self.powers.familiar is not None:
            Damagemultiplier *= .6
        if self.powers and self.powers.active("Buff"):
            Damagemultiplier *= .75
        Actualdamage = max(1, round(Incomingdamage * Damagemultiplier))
        if self.Blocktime > 0:
            Actualdamage = max(1, round(Actualdamage * self.Guardmultiplier))
        if self.progress is not None:
            self.progress.Damagetaken += min(self.Currenthp, Actualdamage)
        self.Currenthp = max(0, self.Currenthp - Actualdamage)
        if self.Currenthp == 0:
            self.Currentlives = max(0, self.Currentlives - 1)
            if self.Currentlives > 0:
                self.Currenthp = self.Maxhp
        return Actualdamage

    #

    def Usesrangedweapon(self):

        return ITEMS[self.Mainhand][1] in ("Bow", "Focus")

    def Aimdirection(self, target):

        direction = pg.Vector2(target) - (self.x, self.y)
        if not direction.length_squared():
            direction = pg.Vector2(DIRECTIONS[self.facing])
        return direction.normalize()

    def Attackenemies(self, enemies, Gamemap=None, target=None):

        if self.Dashtime > 0 or self.Blocktime > 0 or (self.powers and self.powers.familiar is not None and not self.Usesrangedweapon()):
            return
        if self.Attackstage == 1 and not self.Usesrangedweapon():
            self.Attackqueued = True
            return
        if self.Attackstage or self.Attackcooldown > 0:
            return
        self.Attackfacing = self.facing
        if self.Usesrangedweapon():
            if target is not None:
                self.Rangedaim = self.Aimdirection(target)
            else:
                self.Rangedaim = pg.Vector2(DIRECTIONS[self.facing]).normalize()
            self.Attackfacing = max(range(len(DIRECTIONS)), key=lambda index: self.Rangedaim.dot(pg.Vector2(DIRECTIONS[index]).normalize()))
            self.facing = self.Attackfacing
        self.Attacktargets = enemies
        self.Attackmap = Gamemap
        self.Startswing(1)

    def Startswing(self, stage):

        self.Attackstage = stage
        if stage == 1:
            self.Swingduration = self.Attackdelay
        else:
            self.Swingduration = self.Attackdelay / 2
        self.Attackanimationtime = self.Swingduration
        self.Attackcooldown = self.Swingduration

    def Landattack(self):

        direction = pg.Vector2(DIRECTIONS[self.Attackfacing]).normalize()
        if self.powers and self.powers.active("True Strike"):
            target = self.powers.marked
            self.powers.effects.pop("True Strike")
            if target and target.Currenthp > 0 and math.hypot(target.x - self.x, target.y - self.y) <= 650:
                self.powers.hit(target, self.attack)
                self.powers.Casttrails.append((pg.Vector2(self.x, self.y), pg.Vector2(target.x, target.y), (228, 188, 131), .27, .27))
                return
        if self.Usesrangedweapon():
            direction = self.Rangedaim
            position = pg.Vector2(self.x, self.y)
            self.shots.append((position, direction, self.Attackrange, self.attack + (ITEMS[self.charm][3] if self.charm else 0), ITEMS[self.Mainhand][2], self.Attacktargets, self.Attackmap))
            return
        start = pg.Vector2(self.x, self.y)
        for enemy in self.Meleetargets(self.Attacktargets, start, direction, self.Attackrange, self.Attackmap):
            damage = self.attack + (ITEMS[self.charm][3] if self.charm else 0)
            if self.Attackstage != 1:
                damage = max(1, damage // 2)
            if self.powers:
                self.powers.hit(enemy, damage)
            else:
                enemy.Takedamage(damage)

    def Meleetargets(self, enemies, start, direction, reach, Gamemap):

        for enemy in enemies:
            if getattr(enemy, 'Currenthp', 1) <= 0:
                continue
            offset = pg.Vector2(enemy.x, enemy.y) - start
            if offset.length() > reach + enemy.size:
                continue
            if offset.length_squared() and direction.dot(offset.normalize()) < 0.35:
                continue
            if Gamemap is None or Gamemap.Clearenemypath(start.x, start.y, enemy.x, enemy.y, 4):
                yield enemy

    #

    def Updateshots(self, dt):

        active = []
        for position, direction, remaining, damage, colour, targets, Gamemap in self.shots:
            distance = min(remaining, (790 if self.clan == "Marksman" else 620) * dt)
            end = position + direction * distance
            nearest = None
            Nearestdistance = distance
            for enemy in targets:
                if enemy.Currenthp <= 0:
                    continue
                offset = pg.Vector2(enemy.x, enemy.y) - position
                along = offset.dot(direction)
                radius = enemy.Bodyradius() + 5
                side = abs(offset.cross(direction))
                if side > radius:
                    continue
                half = math.sqrt(radius * radius - side * side)
                contact = max(0, along - half)
                if along + half >= 0 and contact <= Nearestdistance:
                    nearest, Nearestdistance = enemy, contact
            impact = position + direction * Nearestdistance
            if Gamemap and not Gamemap.Clearenemypath(position.x, position.y, impact.x, impact.y, 3):
                continue
            if nearest:
                if self.powers:
                    self.powers.hit(nearest, damage)
                else:
                    nearest.Takedamage(damage)
            elif remaining > distance:
                active.append((end, direction, remaining - distance, damage, colour, targets, Gamemap))
        self.shots = active

    def update(self, dt):

        self.Updateshots(dt)
        if self.powers:
            self.powers.update(dt)
        self.Animationtime += dt
        self.Attackcooldown = max(0, self.Attackcooldown - dt)
        if self.Attackstage:
            Previoustime = self.Attackanimationtime
            self.Attackanimationtime = max(0, Previoustime - dt)
            contact = self.Swingduration * 0.58
            if Previoustime > contact >= self.Attackanimationtime:
                self.Landattack()
            if self.Attackanimationtime == 0:
                if self.Attackstage == 1 and self.Attackqueued:
                    self.Startswing(2)
                elif self.Attackstage == 2:
                    self.Startswing(3)
                else:
                    self.Attackstage = 0
                    self.Attackqueued = False
                    self.Attacktargets = []
                if self.Attackstage:
                    self.Attackanimationtime -= dt - Previoustime
                    self.Attackcooldown = self.Attackanimationtime
        self.Blocktime = max(0, self.Blocktime - dt)
        self.Blockcooldown = max(0, self.Blockcooldown - dt)
        self.Dashcooldown = max(0, self.Dashcooldown - dt)

#================================================

# Camera

#================================================

# Camera

class Camera:

    def __init__(self, screen, Worldwidth, Worldheight):

        self.screen = screen
        self.Screenwidth, self.Screenheight = screen.get_size()
        self.Worldwidth = Worldwidth
        self.Worldheight = Worldheight
        self.offset = pg.Vector2(0, 0)
        self.Leftborder = 470
        self.Rightborder = 470
        self.Topborder = 320
        self.Bottomborder = 285

    #

    def update(self, player):

        Screenx = player.x - self.offset.x
        Screeny = player.y - self.offset.y
        if Screenx < self.Leftborder:
            self.offset.x = player.x - self.Leftborder
        elif Screenx > self.Screenwidth - self.Rightborder:
            self.offset.x = player.x - (self.Screenwidth - self.Rightborder)
        if Screeny < self.Topborder:
            self.offset.y = player.y - self.Topborder
        elif Screeny > self.Screenheight - self.Bottomborder:
            self.offset.y = player.y - (self.Screenheight - self.Bottomborder)
        if ASCENT.collidepoint(player.x, player.y):
            self.offset.x = ALTAR[0] - self.Screenwidth // 2
        Maxoffsetx = max(0, self.Worldwidth - self.Screenwidth)
        Maxoffsety = max(0, self.Worldheight - self.Screenheight)
        self.offset.x = max(0, min(self.offset.x, Maxoffsetx))
        self.offset.y = max(-self.Topborder, min(self.offset.y, Maxoffsety + self.Bottomborder))

    #

    def apply(self, x, y):
        return round(x - self.offset.x), round(y - self.offset.y)

#================================================

# Projectile

#================================================

# Projectile

class Projectile:

    def __init__(self, screen, x, y, direction, damage):

        self.screen = screen
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1000
        self.damage = damage
        self.size = 12
        self.colour = (190, 225, 255)

    #

    def update(self, dt):
        self.x += self.direction.x * self.speed * dt
        self.y += self.direction.y * self.speed * dt

    #

    def render(self, camera):
        Screenposition = camera.apply(self.x, self.y)
        pg.draw.circle(self.screen, self.colour, Screenposition, self.size)

    #

    def Collideswithplayer(self, player):
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance <= player.size + self.size

    #

    def Isonscreen(self):
        return (-50 <= self.x <= MAPWIDTH + 50 and -50 <= self.y <= MAPHEIGHT + 50)

#================================================

# Enemy

PIXELBOSSES = ("Piano", "Guitar", "Flute", "Cello", "Harp", "Violin")


#================================================

# Enemy

class Enemy:
    def __init__(self, screen, Enemytype, player, Gamemap=None, name=None, home=None):

        self.screen = screen
        self.player = player
        self.Gamemap = Gamemap
        self.Enemytype = Enemytype
        self.name = name or Enemytype
        self.home = home
        if home is None:
            self.x, self.y = self.Randomspawnposition()
        else:
            self.x, self.y = home
        self.Setstats()
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            self.size = 23
        if self.name in ("Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            self.Attacktype = "projectile"
            if self.name == "Rosin Spirit":
                self.Attackrange = 155
            else:
                self.Attackrange = 175
            if self.name in ("Ripple Wisp", "Bowshade"):
                self.Attackrange = 195
        self.Nameimage = pg.font.Font(None, 20).render(self.name, True, (235, 228, 209))
        self.moving = False
        self.strikes = 0
        self.windup = 0
        self.Winduplength = 1
        self.Lungetime = 0
        self.Lungehit = False
        self.Deathtime = 0
        self.Rewardclaimed = False
        self.Movename = ''
        self.aim = pg.Vector2(0, 1)
        self.Attackcooldown = 0
        self.Attackdelay = 2.0
        self.projectiles = []
        self.Animationtime = random.random()
        self.Attackanimationtime = 0
        self.Facingrow = 0
        self.Windupframes = []
        self.Deathframes = []
        self.Directionalmob = self.home is not None and self.Enemytype in ("Common", "Strong")
        if self.Directionalmob:
            self.Idleframes, self.Runframes, self.Attackframes, self.Windupframes, self.Deathframes = Mobframes(IMAGEFOLDER, self.name)
        self.Keeperposes = []
        self.Bosssteps = []
        self.walked = 0
        if self.Enemytype == "Overture":
            for index in range(8):
                pose = pg.image.load(IMAGEFOLDER / "BlueGrey" / "KeeperPoses" / f"{index}.png").convert_alpha()
                pose = pg.transform.scale(pose, (round(pose.get_width() * 2.5), round(pose.get_height() * 2.5)))
                self.Keeperposes.append(pose)
            self.Bosssteps = Originalkeepersteps(self.Keeperposes[0])
        if self.Enemytype in PIXELBOSSES:
            Regionfolder = "FrostPiano"
            if self.Enemytype == "Guitar":
                Regionfolder = "GuitarCaverns"
            elif self.Enemytype == "Flute":
                Regionfolder = "FluteCloister"
            elif self.Enemytype == "Cello":
                Regionfolder = "CelloCatacombs"
            elif self.Enemytype == "Harp":
                Regionfolder = "HarpReservoir"
            elif self.Enemytype == "Violin":
                Regionfolder = "ViolinHall"
            if self.Enemytype == "Violin":
                Posescale = 0.90
            else:
                Posescale = 1.23
            for index in range(8):
                pose = pg.image.load(IMAGEFOLDER / Regionfolder / "BossPoses" / f"{index}.png").convert_alpha()
                pose = pg.transform.scale(pose, (round(pose.get_width() * Posescale), round(pose.get_height() * Posescale)))
                self.Keeperposes.append(pose)
            if self.Enemytype == "Guitar":
                self.Bosssteps = Loadbosssteps(IMAGEFOLDER / "GuitarCaverns" / "BossPoses", self.Keeperposes[0])
            if self.Enemytype == "Cello":
                self.Bosssteps = Originalkeepersteps(self.Keeperposes[0])
            self.Keeperposes = [Bosspixelframe(pose) for pose in self.Keeperposes]
            self.Bosssteps = [Bosspixelframe(pose) for pose in self.Bosssteps]
            self.Bossidle = Bossidleframes(self.Keeperposes[0], self.Enemytype)
            self.Idleframes = [[self.Keeperposes[0]]] * 4
            self.Runframes = self.Idleframes
            self.Attackframes = self.Idleframes
            return
        if self.Windupframes:
            return
        if self.home is not None:
            scale = 94
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                scale = 66
            if self.Enemytype == "Overture":
                scale = 138
            self.Idleframes = Creatureframes(IMAGEFOLDER, self.name, "Idle", scale)
            self.Runframes = Creatureframes(IMAGEFOLDER, self.name, "Run", scale)
            self.Attackframes = Creatureframes(IMAGEFOLDER, self.name, "Attack", scale)
        else:
            self.Idleframes = Loadenemyanimation(self.Slimenumber, "Idle", self.Spritescale)
            self.Runframes = Loadenemyanimation(self.Slimenumber, "Run", self.Spritescale)
            self.Attackframes = Loadenemyanimation(self.Slimenumber, "Attack", self.Spritescale)

    #

    def Setstats(self):

        if self.Enemytype == "Common":
            self.Maxhp = random.randint(25, 50)
            self.attack = random.randint(5, 10)
            self.speed = random.randint(125, 300)
            self.size = 24
            self.Slimenumber = 1
            self.Spritescale = 128
            self.Attackrange = 25
            self.Attacktype = "melee"

        elif self.Enemytype == "Strong":
            self.Maxhp = random.randint(50, 80)
            self.attack = random.randint(10, 15)
            self.speed = random.randint(100, 275)
            self.size = 32
            self.Slimenumber = 2
            self.Spritescale = 144
            self.Attackrange = 50
            self.Attacktype = random.choice(["melee", "projectile"])

        elif self.Enemytype == "Elite":
            self.Maxhp = random.randint(150, 200)
            self.attack = random.randint(20, 30)
            self.speed = random.randint(75, 250)
            self.size = 46
            self.Slimenumber = 3
            self.Spritescale = 160
            self.Attackrange = 75
            self.Attacktype = random.choice(["melee", "projectile"])

        elif self.Enemytype == "Overture":
            self.Maxhp = 600
            self.attack = 42
            self.speed = 175
            self.size = 42
            self.Attackrange = 45
            self.Attacktype = "melee"

        else:
            self.Maxhp = self.player.Maxhp * 5
            self.attack = self.player.attack * 2
            self.speed = random.randint(50, 200)
            self.size = 64
            self.Slimenumber = 3
            self.Spritescale = 224
            self.Attackrange = 100
            self.Attacktype = "projectile"

        self.Currenthp = self.Maxhp

    #

    def Randomspawnposition(self):

        if self.Gamemap is not None:
            return self.Gamemap.Randomenemyspawnposition(self.player.x, self.player.y)
        return random.randint(0, MAPWIDTH), random.randint(0, MAPHEIGHT)

    #

    def update(self, dt):

        if self.Currenthp <= 0:
            self.Deathtime += dt
            return
        self.Animationtime += dt
        self.Attackcooldown = max(0, self.Attackcooldown - dt)
        self.Attackanimationtime = max(0, self.Attackanimationtime - dt)
        self.moving = False
        if self.windup > 0:
            self.windup = max(0, self.windup - dt)
            if self.windup == 0:
                self.Releaseattack()
            return
        if self.Lungetime > 0:
            self.Skitterlunge(dt)
            return
        if self.projectiles:
            self.Updateprojectiles(dt)
        if self.Enemytype == "Overture":
            if not self.Gamemap.Locationname(self.player.x, self.player.y).endswith("Overture Arena"):
                self.Movetowards(self.home[0], self.home[1], dt, 3)
                return
        elif self.home is not None:
            Playerdistance = math.hypot(self.player.x - self.x, self.player.y - self.y)
            Homedistance = math.hypot(self.player.x - self.home[0], self.player.y - self.home[1])
            if self.player.clan == "Familiar":
                detection = 1050
            else:
                detection = 410
            if self.player.powers and self.player.clan == "Assassin":
                if self.player.powers.active("Sneak"):
                    detection = 165
                else:
                    detection = 310
            if Playerdistance > detection or Homedistance > 560:
                self.Movetowards(self.home[0], self.home[1], dt, 3)
                return
        if self.Attackanimationtime <= 0:
            Stopdistance = self.Attackrange
            if self.Attacktype == "melee":
                Stopdistance += self.player.size + self.size - 6
            self.Movetowards(self.player.x, self.player.y, dt, Stopdistance)
        self.Checkattack()

    #

    def footprint(self):

        # Horizontal radius, vertical radius, and offset to the feet.
        if self.Enemytype == "Piano":
            return 41, 19, 9
        if self.Enemytype == "Overture":
            return 46, 22, 8
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            return 16, 12, 0
        return round(self.size * 0.84), round(self.size * 0.64), 4

    def Bodyradius(self):

        width, height, offset = self.footprint()
        return width

    def Bodyoverlap(self, x, y, radius, Centerx=None, Centery=None):

        width, height, offset = self.footprint()
        if Centerx is None:
            Centerx = self.x
            Centery = self.y
        dx = (x - Centerx) / (width + radius)
        dy = (y - Centery - offset) / (height + radius)
        return 1 - math.hypot(dx, dy)

    def Blocksplayer(self, x, y, Playerradius):

        return self.Bodyoverlap(x, y, Playerradius) > 0

    def Canstep(self, x, y):

        if self.Enemytype == "Overture":
            room = "Overture Arena"
        else:
            room = getattr(self, "Arenaroom", None)
        if room and not self.Gamemap.Locationname(x, y).endswith(room):
            return False
        if self.player.clan == "Familiar":
            targets = (self.player, self.player.owner.player)
        else:
            targets = (self.player,)
        for target in targets:
            overlap = self.Bodyoverlap(target.x, target.y, target.size, x, y)
            if overlap > 0 and overlap >= self.Bodyoverlap(target.x, target.y, target.size):
                return False
        return self.Gamemap.Canmovecircle(x, y, self.Bodyradius())

    #

    def Movetowards(self, Targetx, Targety, dt, Stopdistance):

        dx = Targetx - self.x
        dy = Targety - self.y
        direction = pg.Vector2(dx, dy)
        if direction.length() == 0:
            return
        if self.Directionalmob:
            self.Facingrow = Facingrow(dx, dy)
        elif abs(dx) > abs(dy):
            self.Facingrow = 2 if dx > 0 else 1
        else:
            self.Facingrow = 0 if dy > 0 else 3
        distance = direction.length()
        direction = direction.normalize()
        Movex = direction.x * self.speed * dt
        Movey = direction.y * self.speed * dt
        if distance > Stopdistance:
            Oldx, Oldy = self.x, self.y
            if self.Gamemap is None:
                self.x += Movex
                self.y += Movey
            else:
                if self.Canstep(self.x + Movex, self.y):
                    self.x += Movex
                if self.Canstep(self.x, self.y + Movey):
                    self.y += Movey
            Distancemoved = math.hypot(self.x - Oldx, self.y - Oldy)
            self.moving = Distancemoved > 0
            if self.moving and self.Directionalmob:
                self.Facingrow = Facingrow(self.x - Oldx, self.y - Oldy)
            self.walked += Distancemoved

    #
    
    def Checkattack(self):

        distance = math.hypot(self.player.x - self.x, self.player.y - self.y)
        if self.Attackcooldown > 0 or self.Attackanimationtime > 0:
            return
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if self.Enemytype == "Overture":
            self.Movename = ["Resonance stomp", "Fork thrust", "Three-note volley"][self.strikes % 3]
            reach = [185, 280, 390][self.strikes % 3]
            self.Winduplength = [0.72, 0.65, 0.85][self.strikes % 3]
        else:
            if self.Attacktype == "projectile":
                self.Movename = "Sonic dart"
            else:
                self.Movename = "Lunge"
            reach = self.Attackrange + self.player.size + self.size
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat"):
                self.Winduplength = 0.32
            else:
                self.Winduplength = 0.42
            if self.name == "Chalk Skitter":
                reach += 29
            elif self.name == "Score Swarm":
                reach = 96
                self.Winduplength = 0.58
            elif self.name in ("Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                self.Winduplength = 0.48
            elif self.name in ("Silt Scorpion", "Mossback Snapper"):
                self.Winduplength = 0.44
        if distance <= reach and self.Canreachplayer():
            if offset.length_squared():
                self.aim = offset.normalize()
            if self.Directionalmob:
                self.Facingrow = Facingrow(self.aim.x, self.aim.y)
            self.windup = self.Winduplength

    def Releaseattack(self):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        distance = offset.length()
        self.Attackanimationtime = 0.3
        self.Attackcooldown = self.Attackdelay
        if self.name == "Chalk Skitter":
            self.Lungetime = 0.14
            self.Lungehit = False
            return
        if self.name == "Score Swarm":
            if distance <= 96 and self.Canreachplayer():
                self.player.Takedamage(self.attack)
            return
        if self.Movename == "Three-note volley":
            for angle in (-23, 0, 23):
                self.projectiles.append(Projectile(self.screen, self.x, self.y, self.aim.rotate(angle), self.attack))
        elif self.Movename == "Sonic dart":
            dart = Projectile(self.screen, self.x, self.y, self.aim, self.attack)
            if self.name == "Rosin Spirit":
                dart.speed = 365
                dart.size = 10
                dart.colour = (229, 155, 97)
            elif self.name == "Ripple Wisp":
                dart.speed = 295
                dart.size = 12
                dart.colour = (111, 225, 215)
            elif self.name == "Bowshade":
                dart.speed = 355
                dart.size = 10
                dart.colour = (200, 164, 241)
            elif self.name == "Reed Wisp":
                dart.speed = 420
                dart.size = 8
                dart.colour = (173, 218, 194)
            self.projectiles.append(dart)
        else:
            hit = distance <= self.Attackrange + self.player.size + self.size
            if self.Movename == "Resonance stomp":
                hit = distance <= 185
            elif self.Movename == "Fork thrust":
                hit = 0 <= offset.dot(self.aim) <= 280 and abs(offset.cross(self.aim)) < 50
            elif self.Movename == "Lunge":
                hit = hit and offset.dot(self.aim) >= 0 and abs(offset.cross(self.aim)) < 43
            if hit and self.Canreachplayer():
                self.player.Takedamage(self.attack)
        if self.Enemytype == "Overture":
            self.strikes += 1
            if self.strikes % 3:
                self.Attackcooldown = 1.10
            else:
                self.Attackcooldown = 2.0

    def Skitterlunge(self, dt):

        elapsed = min(dt, self.Lungetime)
        self.Lungetime -= elapsed
        move = self.aim * 410 * elapsed
        steps = max(1, math.ceil(move.length() / 6))
        for _ in range(steps):
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if not self.Lungehit and 0 <= offset.dot(self.aim) <= 68 and abs(offset.cross(self.aim)) <= 37 and self.Canreachplayer():
                self.player.Takedamage(self.attack)
                self.Lungehit = True
            x, y = self.x + move.x / steps, self.y + move.y / steps
            if not self.Canstep(x, y):
                self.Lungetime = 0
                break
            self.x, self.y = x, y

    def Drawwarning(self, x, y):

        if self.windup:
            color = (231, 156, 80)
        else:
            color = (251, 210, 127)
        origin = pg.Vector2(x, y)
        if self.name == "Score Swarm":
            if self.windup:
                colour = (190, 155, 202)
            else:
                colour = (231, 191, 215)
            pg.draw.circle(self.screen, colour, (x, y), 96, 2)
            return
        if self.name in ("Silt Scorpion", "Mossback Snapper"):
            point = origin + self.aim * 65
            side = self.aim.rotate(90)
            if self.windup:
                color = (213, 151, 107)
            else:
                color = (248, 195, 130)
            if self.windup:
                pg.draw.lines(self.screen, color, False, [point - self.aim * 16 + side * 13, point, point - self.aim * 16 - side * 13], 3)
            else:
                strength = self.Attackanimationtime / 0.3
                for i in range(3):
                    front = origin + self.aim * (35 + 11 * i)
                    back = front - self.aim * (13 + round(8 * strength))
                    pg.draw.line(self.screen, color, back + side * (i - 1) * 8, front, 2)
            return
        if self.name in ("Rosin Spirit", "Ripple Wisp"):
            point = origin + self.aim * 23
            point.y -= 15
            if self.windup:
                charge = 1 - self.windup / self.Winduplength
            else:
                charge = 1
            radius = 4 + round(charge * 7)
            pg.draw.circle(self.screen, (69, 152, 165) if self.name == "Ripple Wisp" else (170, 99, 82), (round(point.x), round(point.y)), radius, 2)
            pg.draw.circle(self.screen, (155, 247, 222) if self.name == "Ripple Wisp" else (243, 177, 109), (round(point.x), round(point.y)), max(2, radius // 3))
            for i in (-1, 1):
                spark = point + self.aim.rotate(i * 65) * (17 - charge * 7)
                pg.draw.rect(self.screen, (236, 166, 102), (round(spark.x), round(spark.y), 3, 3))
            return
        if self.name in ("Reed Wisp", "Bowshade"):
            point = origin + self.aim * 20
            point.y -= 19
            if self.windup:
                charge = 1 - self.windup / self.Winduplength
            else:
                charge = 1
            radius = 4 + round(charge * 7)
            center = (round(point.x), round(point.y))
            if self.name == "Bowshade":
                colour = (197, 158, 229)
            else:
                colour = (118, 184, 164)
            pg.draw.circle(self.screen, colour, center, radius, 2)
            pg.draw.circle(self.screen, (219, 243, 222), center, max(2, radius // 3))
            if self.windup:
                for i in (-1, 0, 1):
                    end = point + self.aim.rotate(i * 38) * (22 - charge * 8)
                    pg.draw.line(self.screen, (154, 198, 179), end, end - self.aim * 6, 2)
            return
        if self.name == "Chalk Skitter":
            tip = origin + self.aim * 72
            side = self.aim.rotate(90)
            if self.windup:
                pg.draw.lines(self.screen, (197, 177, 138), False, [tip - self.aim * 15 + side * 12, tip, tip - self.aim * 15 - side * 12], 2)
            elif self.Lungetime > 0:
                for angle in (-32, 32):
                    claw = origin + self.aim.rotate(angle) * 36
                    pg.draw.line(self.screen, (223, 216, 186), claw, claw + self.aim * 11, 2)
            return
        if self.Movename == "Resonance stomp":
            if self.windup:
                progress = 1 - self.windup / self.Winduplength
            else:
                progress = 1
            for angle in range(0, 360, 24):
                point = origin + pg.Vector2(150, 0).rotate(angle)
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 2 + round(progress * 2))
        elif self.Movename == "Fork thrust":
            for distance in range(65, 281, 35):
                point = origin + self.aim * distance
                tail = point - self.aim * 9
                side = self.aim.rotate(90) * 5
                pg.draw.lines(self.screen, color, False, [tail + side, point, tail - side], 2)
        elif self.Movename == "Three-note volley":
            for angle in (-23, 0, 23):
                direction = self.aim.rotate(angle)
                for distance in (75, 125, 175, 225):
                    point = origin + direction * distance
                    pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 3)
        else:
            pg.draw.line(self.screen, color, origin + self.aim * 22, origin + self.aim * 74, 3)

    def Bossrestframe(self):

        if self.Bosssteps and self.moving:
            if self.Enemytype == "Guitar":
                Steplength = 13
            else:
                Steplength = 36
            index = 1 + int(self.walked / Steplength) % (len(self.Bosssteps) - 1)
            frame = self.Bosssteps[index]
        elif self.Enemytype == "Overture" and self.Bosssteps and math.sin(self.Animationtime * 2.6) > 0.2:
            frame = self.Bosssteps[0]
        else:
            frame = self.Keeperposes[0]
        if self.moving:
            Facingleft = self.Facingrow == 1
        else:
            Facingleft = self.aim.x < 0
        if Facingleft:
            frame = pg.transform.flip(frame, True, False)
        return frame

    def Keeperframe(self):

        index = 0
        if self.windup or self.Attackanimationtime:
            windup, impact = [(1, 2), (3, 4), (5, 6)][["Resonance stomp", "Fork thrust", "Three-note volley"].index(self.Movename)]
            if self.windup:
                index = windup
            elif self.Attackanimationtime > 0.12:
                index = impact
            else:
                index = 7
        if index == 0:
            return self.Bossrestframe()
        frame = self.Keeperposes[index]
        if self.aim.x < 0:
            return pg.transform.flip(frame, True, False)
        return frame

    def Canreachplayer(self):

        if self.Gamemap is None:
            return True
        return self.Gamemap.Clearenemypath(self.x, self.y, self.player.x, self.player.y, 4)

    #

    def shoot(self):

        direction = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if direction.length() == 0:
            return
        direction = direction.normalize()
        projectile = Projectile(self.screen, self.x, self.y, direction, self.attack)
        self.projectiles.append(projectile)

    #

    def Updateprojectiles(self, dt):

        Projectilestoupdate = self.projectiles[:]
        for projectile in Projectilestoupdate:
            projectile.update(dt)
            if self.Gamemap is not None and not self.Gamemap.Canmovecircle(projectile.x, projectile.y, projectile.size):
                self.projectiles.remove(projectile)
            elif projectile.Collideswithplayer(self.player):
                self.player.Takedamage(projectile.damage)
                self.projectiles.remove(projectile)
            elif not projectile.Isonscreen():
                self.projectiles.remove(projectile)

    #

    def render(self, camera):

        if self.Currenthp <= 0:
            x, y = camera.apply(self.x, self.y)
            if self.Keeperposes:
                frame = self.Keeperposes[7]
            else:
                frame = self.Idleframes[self.Facingrow][0]
            progress = min(1, self.Deathtime / 0.65)
            if self.Deathframes:
                poses = self.Deathframes[self.Facingrow]
                frame = poses[min(len(poses) - 1, int(progress * (len(poses) + 1)))].copy()
                if self.name in ("Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                    y -= round(max(0, 1 - progress * (2.2 if self.name == "Ripple Wisp" else 4)) * 14)
            elif self.Enemytype in PIXELBOSSES:
                frame = frame.copy()
                y += round(progress * 10)
            else:
                frame = pg.transform.scale(frame, (frame.get_width(), max(2, round(frame.get_height() * (1 - progress * 0.82)))))
            frame.set_alpha(round(255 * (1 - progress)))
            self.screen.blit(frame, frame.get_rect(midbottom=(x, y + 14)))
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                spread = round(14 + 45 * progress)
                pg.draw.rect(self.screen, (181 - round(progress * 100), 129 - round(progress * 70), 79), (x + dx * spread, y + dy * spread, 3, 3))
            return

        if self.windup > 0 and self.Windupframes:
            frames = self.Windupframes[self.Facingrow]
            progress = 1 - self.windup / self.Winduplength
            frame = frames[min(len(frames) - 1, int(progress * len(frames)))]
        elif self.Attackanimationtime > 0:
            frames = self.Attackframes[self.Facingrow]
            Framenumber = int((0.3 - self.Attackanimationtime) * 16)
            if self.Directionalmob:
                Framenumber = int((1 - self.Attackanimationtime / 0.3) * len(frames))
            Framenumber = min(len(frames) - 1, Framenumber)
            frame = frames[Framenumber]
        else:
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                frames = self.Runframes[self.Facingrow]
                frame = frames[int(self.Animationtime * (10 if self.name == "Ripple Wisp" else 15)) % len(frames)]
            elif self.moving:
                frames = self.Runframes[self.Facingrow]
                phase = self.Animationtime * 10
                if self.name in ("Chalk Skitter", "Silt Scorpion", "Mossback Snapper", "Score Swarm"):
                    phase = self.walked / (8 if self.name == "Mossback Snapper" else 11)
                frame = frames[int(phase) % len(frames)]
            else:
                frames = self.Idleframes[self.Facingrow]
                frame = frames[int(self.Animationtime * 5) % len(frames)]
        if self.Keeperposes:
            frame = self.Keeperframe()
        Screenx, Screeny = camera.apply(self.x, self.y)
        if self.windup > 0:
            self.Drawwarning(Screenx, Screeny)
            if not self.Keeperposes and not self.Windupframes:
                frame = pg.transform.scale(frame, (frame.get_width() + 6, max(1, frame.get_height() - 9)))
        elif self.Attackanimationtime > 0 and self.Movename:
            self.Drawwarning(Screenx, Screeny)
        if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
            pg.draw.ellipse(self.screen, (27, 30, 46), (Screenx - 14, Screeny - 4, 28, 10))
            Screeny -= 14 + round(math.sin(self.Animationtime * 8) * 3)
        if self.Attackanimationtime > 0 and self.Movename and not self.Directionalmob and self.Enemytype not in PIXELBOSSES:
            progress = 1 - self.Attackanimationtime / 0.3
            force = math.sin(progress * math.pi)
            push = self.aim * force * (17 if self.Enemytype == "Overture" else 11)
            frame = pg.transform.scale(frame, (frame.get_width() + round(force * 8), frame.get_height() + round(force * 12)))
            Screenx += round(push.x)
            Screeny += round(push.y)
            if self.name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade"):
                Screeny += round(force * 12)
        if self.Keeperposes:
            Footoffset = 21
        else:
            Footoffset = 14
        if self.Enemytype == "Violin":
            Footoffset = 16
        if self.Enemytype in PIXELBOSSES:
            if not (self.moving or self.windup or self.Attackanimationtime or self.encore or self.Teleporttime or self.volley):
                if self.Enemytype in ("Guitar", "Violin"):
                    pace = 5
                else:
                    pace = 4
                frame = self.Bossidle[int(self.Animationtime * pace) % len(self.Bossidle)]
                if self.aim.x < 0:
                    frame = pg.transform.flip(frame, True, False)
            else:
                Offsetx, Offsety = Bossposeoffset(self)
                Screenx += Offsetx
                Screeny += Offsety
        Spriterect = frame.get_rect(midbottom=(Screenx, Screeny + Footoffset))
        self.screen.blit(frame, Spriterect)
        Spritetop = Spriterect.top + frame.get_bounding_rect().top
        Barwidth = self.size * 2
        Barx = Screenx - Barwidth // 2
        Bary = Spritetop - 12
        Namerect = self.Nameimage.get_rect(midbottom=(Screenx, Bary - 3))
        pg.draw.rect(self.screen, (20, 24, 34), Namerect.inflate(8, 2))
        self.screen.blit(self.Nameimage, Namerect)
        pg.draw.rect(self.screen, (27, 31, 41), (Barx, Bary, Barwidth, 7))
        pg.draw.rect(self.screen, (145, 190, 220), (Barx, Bary, Barwidth * self.Currenthp / self.Maxhp, 7))
        for projectile in self.projectiles:
            projectile.render(camera)

    #

    def Takedamage(self, damage):
        if self.player.clan == "Familiar":
            player = self.player.owner.player
        else:
            player = self.player
        if player.progress is not None and self.Currenthp > 0:
            dealt = min(damage, self.Currenthp)
            player.progress.Damagedealt += dealt
            player.progress.Highesthit = max(player.progress.Highesthit, dealt)
        self.Currenthp -= damage
        if self.Currenthp <= 0:
            self.Currenthp = 0
            return True
        return False

#================================================

# Enemy manager

#================================================

# Enemy manager

class Habitat:

    def __init__(self, name):

        self.name = name
        self.members = []
        self.Respawntimer = 3.0


class EnemyManager:

    def __init__(self, screen, player, Gamemap=None):

        self.screen = screen
        self.player = player
        self.Gamemap = Gamemap
        self.enemies = []
        self.player.enemies = self.enemies
        self.Spawntimer = 0
        self.Spawndelay = 2.0
        self.habitats = []
        if self.Gamemap is not None:
            from Bosses import CelloBoss, FluteBoss, GuitarBoss, HarpBoss, PianoBoss, ViolinBoss

            for name, Enemytype, x, y in HABITATS + FROSTHABITATS + GUITARHABITATS + FLUTEHABITATS + CELLOHABITATS + HARPHABITATS + VIOLINHABITATS:
                enemy = Enemy(screen, Enemytype, player, Gamemap, name, (x, y))
                self.enemies.append(enemy)
                if enemy.Directionalmob:
                    habitat = Gamemap.Locationname(x, y)
                    if habitat == "Connecting passage":
                        habitat = (x//1400, y//1400)
                    for group in self.habitats:
                        if group.name == habitat:
                            break
                    else:
                        group = Habitat(habitat)
                        self.habitats.append(group)
                    group.members.append((name, Enemytype, x, y))
            self.enemies.append(PianoBoss(screen, player, Gamemap))
            self.enemies.append(GuitarBoss(screen, player, Gamemap))
            self.enemies.append(FluteBoss(screen, player, Gamemap))
            self.enemies.append(CelloBoss(screen, player, Gamemap))
            self.enemies.append(HarpBoss(screen, player, Gamemap))
            self.enemies.append(ViolinBoss(screen, player, Gamemap))

    #

    def update(self, dt):

        self.Spawntimer -= dt
        if self.Gamemap is None and self.Spawntimer <= 0:
            self.Spawnenemy()
            self.Spawntimer = self.Spawndelay
        Enemiestoupdate = self.enemies[:]
        for enemy in Enemiestoupdate:
            if self.player.powers and enemy in self.player.powers.stunned:
                continue
            target = self.Targetfor(enemy)
            enemy.player = target
            try:
                enemy.update(dt)
            finally:
                enemy.player = self.player
            if enemy.Deathtime >= 0.65:
                self.enemies.remove(enemy)
        if self.Gamemap is not None:
            self.Respawnmobs(dt)
    
    #

    def Respawnmobs(self, dt):

        living = {(enemy.name, *enemy.home) for enemy in self.enemies if enemy.Directionalmob and enemy.Currenthp > 0}
        for habitat in self.habitats:
            members = habitat.members
            for name, kind, x, y in members:
                if (name, x, y) in living:
                    habitat.Respawntimer = 3.0
                    break
            else:
                habitat.Respawntimer = max(0, habitat.Respawntimer - dt)
                if habitat.Respawntimer == 0:
                    self.Respawnhabitat(habitat)

    #

    def Respawnhabitat(self, habitat):

        members = habitat.members
        positions = []
        for name, kind, x, y in members:
            position = self.Respawnposition(x, y, positions)
            if position is None:
                return
            positions.append(position)
        for (name, kind, x, y), position in zip(members, positions):
            enemy = Enemy(self.screen, kind, self.player, self.Gamemap, name, (x, y))
            enemy.x, enemy.y = position
            self.enemies.append(enemy)
        habitat.Respawntimer = 3.0

    def Respawnposition(self, x, y, positions):

        for dx, dy in [(0, 0), (52, 0), (-52, 0), (0, 52), (0, -52), (75, 55), (-75, -55)]:
            point = (x+dx, y+dy)
            if math.hypot(point[0]-self.player.x, point[1]-self.player.y) < 64:
                continue
            if any(math.hypot(point[0]-px, point[1]-py)<48 for px, py in positions):
                continue
            if self.Gamemap.Canmovecircle(*point, 28):
                return point
        return None

    def Targetfor(self, enemy):

        powers = self.player.powers
        if not powers or powers.familiar is None or self.Gamemap is None:
            return self.player
        familiar = powers.Familiaractor
        if math.hypot(enemy.x-familiar.x, enemy.y-familiar.y) > 1050:
            return self.player
        if enemy.Enemytype == "Overture":
            arena = "Overture Arena"
        else:
            arena = getattr(enemy, "Arenaroom", None)
        if arena and not self.Gamemap.Locationname(familiar.x, familiar.y).endswith(arena):
            return self.player
        if not self.Gamemap.Clearenemypath(enemy.x, enemy.y, familiar.x, familiar.y, 4):
            return self.player
        return familiar

    def Renderenemy(self, enemy, camera):

        enemy.player = self.Targetfor(enemy)
        try:
            enemy.render(camera)
        finally:
            enemy.player = self.player

    def Spawnenemy(self):

        roll = random.randint(1, 100)
        if roll <= 70:
            Enemytype = "Common"
        elif roll <= 90:
            Enemytype = "Strong"
        elif roll <= 98:
            Enemytype = "Elite"
        else:
            Enemytype = "Boss"

        enemy = Enemy(self.screen, Enemytype, self.player, self.Gamemap)
        self.enemies.append(enemy)

    #

    def render(self, camera):
        for enemy in self.enemies:
            enemy.render(camera)

#================================================
