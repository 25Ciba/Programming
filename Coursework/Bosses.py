import math
import pygame as pg
from Classes import Enemy, Projectile
from BossMotion import Bossposeoffset, Drawfrostfold
from Frost import ARENAX, ARENAY
from Guitar import GUITARARENAX, GUITARARENAY
from Flute import FLUTEARENAX, FLUTEARENAY
from Cello import CELLOARENAX, CELLOARENAY
from Harp import HARPARENAX, HARPARENAY


# Piano Ultra Boss

class PianoNote(Projectile):

    def __init__(self, screen, x, y, direction, damage):

        super().__init__(screen, x, y, direction, damage)
        self.speed = 580

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        for distance, size in [(25, 3), (15, 5), (8, 6)]:
            px = round(x - self.direction.x * distance)
            py = round(y - self.direction.y * distance)
            pg.draw.rect(self.screen, (70, 149, 189), (px - size // 2, py - size // 2, size, size))
        pg.draw.ellipse(self.screen, (89, 182, 211), (x - 9, y - 5, 16, 12))
        pg.draw.ellipse(self.screen, (214, 250, 251), (x - 6, y - 3, 11, 7))
        pg.draw.lines(self.screen, (214, 250, 251), False, [(x + 4, y + 1), (x + 4, y - 12), (x + 11, y - 8)], 3)


class PianoBoss(Enemy):

    Arenaroom = "Piano Chamber"
    Regionfolder = "FrostPiano"
    instrument = "Piano"
    Homeposition = (ARENAX, ARENAY)

    def __init__(self, screen, player, Gamemap):

        super().__init__(screen, self.instrument, player, Gamemap, f"{self.instrument} Ultra Boss", self.Homeposition)
        self.pattern = 0
        self.chord = []
        self.lanes = []
        self.volley = []
        self.Beattimer = 0
        self.engaged = False
        self.recovery = 0
        self.echoes = []
        self.wave = None
        self.Wavey = 0
        self.Wavegap = ARENAX
        self.Wavehit = False
        self.encore = 0
        self.Secondphase = False
        self.Teleporttime = 0
        self.Teleportindex = 0
        self.Teleportorigin = self.Homeposition
        self.Teleporttarget = self.Homeposition

    def Setstats(self):

        self.Maxhp = 1100
        self.Currenthp = self.Maxhp
        self.attack = 47
        self.size = 82

    def update(self, dt):

        self.Animationtime += dt
        if self.Currenthp <= 0:
            self.Deathtime += dt
            return
        if not self.Gamemap.Locationname(self.player.x, self.player.y).endswith(self.Arenaroom):
            self.engaged = False
            self.windup = 0
            self.Attackanimationtime = 0
            self.projectiles.clear()
            self.volley.clear()
            self.echoes.clear()
            self.wave = None
            self.encore = 0
            self.Teleporttime = 0
            self.recovery = 0
            return
        if not self.engaged:
            self.engaged = True
            self.recovery = 0.8
        if self.instrument in ("Piano", "Flute", "Harp", "Violin") and self.Updateteleport(dt):
            return
        self.Updateprojectiles(dt)
        self.Updatefloorattacks(dt)
        if self.Currenthp <= self.Maxhp / 2 and not self.Secondphase:
            self.Secondphase = True
            self.encore = 1.1
            self.windup = 0
            self.Attackanimationtime = 0
            self.echoes.clear()
            self.volley.clear()
            self.projectiles.clear()
            self.wave = None
        if self.encore > 0:
            self.encore = max(0, self.encore - dt)
            return
        if self.windup > 0:
            self.windup = max(0, self.windup - dt)
            if self.windup == 0:
                self.Releaseattack()
            return
        self.Attackanimationtime = max(0, self.Attackanimationtime - dt)
        if self.volley:
            self.Beattimer -= dt
            if self.Beattimer <= 0:
                angle = self.volley.pop(0)
                shot = self.Makenote(self.aim.rotate(angle))
                self.projectiles.append(shot)
                self.Beattimer += 0.105
        self.recovery = max(0, self.recovery - dt)
        if self.recovery == 0 and not self.echoes and self.wave is None:
            self.Startphrase()

    def Teleportanchor(self):

        anchors = [
            (ARENAX - 570, ARENAY - 240), (ARENAX + 570, ARENAY - 240),
            (ARENAX - 570, ARENAY + 250), (ARENAX + 570, ARENAY + 250),
            (ARENAX, ARENAY + 320)
        ]
        for step in range(len(anchors)):
            x, y = anchors[(step + self.Teleportindex * 2) % len(anchors)]
            if math.hypot(x - self.x, y - self.y) < 180:
                continue
            if math.hypot(x - self.player.x, y - self.player.y) < 145:
                continue
            if self.Canstep(x, y):
                return x, y
        return None

    def Updateteleport(self, dt):

        thresholds = (0.75, 0.50, 0.25)
        if self.Teleporttime == 0:
            if self.Teleportindex == len(thresholds) or self.Currenthp > self.Maxhp * thresholds[self.Teleportindex]:
                return False
            target = self.Teleportanchor()
            if target is None:
                return False
            self.Teleporttime = 1.0
            self.Teleportorigin = (self.x, self.y)
            self.Teleporttarget = target
            self.windup = 0
            self.Attackanimationtime = 0
            self.echoes.clear()
            self.volley.clear()
            self.projectiles.clear()
            self.wave = None
        previous = self.Teleporttime
        self.Teleporttime = max(0, self.Teleporttime - dt)
        if previous > 0.50 >= self.Teleporttime:
            x, y = self.Teleporttarget
            if not self.Canstep(x, y) or self.Bodyoverlap(self.player.x, self.player.y, self.player.size, x, y) > 0:
                target = self.Teleportanchor()
                if target is None:
                    self.Teleporttime = 0
                    return True
                self.Teleporttarget = target
            self.x, self.y = self.Teleporttarget
            self.Teleportindex += 1
        if self.Teleporttime == 0:
            self.recovery = 0.85
        return True

    def Makenote(self, direction):

        return PianoNote(self.screen, self.x, self.y, direction, self.attack)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Frozen Chord", "Black-Key Sweep", "Rising Arpeggio", "Echo Notes", "Glissando"][self.pattern]
        self.Winduplength = [0.92, 0.86, 0.98, 0.76, 1.05][self.pattern]
        if self.Currenthp <= self.Maxhp / 2:
            self.Winduplength *= 0.82
        self.windup = self.Winduplength
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - pg.Vector2(self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target + side * shift for shift in (-126, 0, 126)]
        # Alternate lanes, leaving a wide gap between each pair.
        center = round((target.x - ARENAX) / 160) * 160 + ARENAX
        self.lanes = [pg.Rect(center + step * 320 - 49, ARENAY - 520, 110, 1040) for step in (-2, -1, 0, 1, 2)]
        if self.pattern == 3:
            self.chord = [target + side * shift for shift in (-145, 0, 145)]
        if self.pattern == 4:
            shift = 165 if target.x <= ARENAX else -165
            self.Wavegap = max(ARENAX - 545, min(ARENAX + 545, target.x + shift))
            self.Wavey = ARENAY - 390

    def Releaseattack(self):

        self.Attackanimationtime = 0.3
        self.strikes += 1
        if self.Currenthp > self.Maxhp / 2:
            self.recovery = 1.25
        else:
            self.recovery = 1.0
        if self.pattern == 0:
            if any(point.distance_to((self.player.x, self.player.y)) <= 110 + self.player.size for point in self.chord):
                self.player.Takedamage(self.attack)
        elif self.pattern == 1:
            if any(lane.inflate(self.player.size * 2, self.player.size * 2).collidepoint(self.player.x, self.player.y) for lane in self.lanes):
                self.player.Takedamage(self.attack + 7)
        elif self.pattern == 2:
            self.volley = [-30, -15, 0, 15, 30]
            self.Beattimer = 0
            self.recovery += 0.42
        elif self.pattern == 3:
            self.echoes = [(point, 0.28 + index * 0.29) for index, point in enumerate(self.chord)]
        else:
            self.wave = self.Wavey
            self.Wavehit = False

    def Updatefloorattacks(self, dt):

        active = []
        for point, remaining in self.echoes:
            remaining -= dt
            if remaining > 0:
                active.append((point, remaining))
            else:
                if point.distance_to((self.player.x, self.player.y)) <= 68 + self.player.size:
                    self.player.Takedamage(self.attack - 9)
        self.echoes = active
        if self.wave is not None:
            speed = 650 if self.Secondphase else 540
            self.wave += speed * dt
            Inwidth = abs(self.player.x - ARENAX) <= 720
            Ingap = abs(self.player.x - self.Wavegap) <= 95 - self.player.size
            if Inwidth and not Ingap and not self.Wavehit and abs(self.player.y - self.wave) <= self.player.size + 15:
                self.player.Takedamage(self.attack + 3)
                self.Wavehit = True
            if self.wave >= ARENAY + 425:
                self.wave = None

    def render(self, camera):

        if self.Currenthp > 0:
            if self.Teleporttime > 0:
                self.Renderteleport(camera)
            for point, remaining in self.echoes:
                x, y = camera.apply(point.x, point.y)
                pg.draw.circle(self.screen, (114, 169, 226), (x, y), 68, 2)
                pg.draw.circle(self.screen, (207, 241, 249), (x, y), max(4, round(remaining * 55)), 3)
            if self.wave is not None:
                self.Drawwave(camera, self.wave, (162, 229, 248))
            if self.encore > 0:
                x, y = camera.apply(self.x, self.y)
                radius = round(90 + (1.1 - self.encore) * 90)
                pg.draw.circle(self.screen, (147, 209, 243), (x, y), radius, 3)
                pg.draw.circle(self.screen, (74, 135, 187), (x, y), radius + 12, 2)
        super().render(camera)

    def Renderteleport(self, camera):

        Drawfrostfold(self.screen, camera, self.Teleportorigin, 1 - self.Teleporttime, False)
        Drawfrostfold(self.screen, camera, self.Teleporttarget, 1 - abs(2 * self.Teleporttime - 1), True)

    def Drawwave(self, camera, y, color):

        for left, right in [(ARENAX - 720, self.Wavegap - 95), (self.Wavegap + 95, ARENAX + 720)]:
            x, py = camera.apply(left, y)
            width = round(right - left)
            pg.draw.rect(self.screen, (57, 101, 153), (x, py - 10, width, 21))
            pg.draw.line(self.screen, color, (x, py - 6), (x + width, py - 6), 3)
            for offset in range(0, width - 14, 22):
                pg.draw.rect(self.screen, color, (x + offset, py - 5, 12, 10))

    def Keeperframe(self):

        index = 0
        if self.Teleporttime > 0:
            frame = self.Keeperposes[5 if self.Teleporttime > 0.5 else 7].copy()
            frame.set_alpha(round(255 * abs(self.Teleporttime - 0.5) * 2))
            return frame
        if self.encore > 0:
            index = 1
        elif self.windup > 0:
            index = (1, 3, 5, 5, 3)[self.pattern]
        elif self.Attackanimationtime > 0.10 or self.volley:
            index = (2, 4, 6, 6, 4)[self.pattern]
        if index == 0:
            return self.Bossrestframe()
        frame = self.Keeperposes[index]
        if self.aim.x < 0:
            return pg.transform.flip(frame, True, False)
        return frame

    def Drawwarning(self, x, y):

        if self.windup:
            color = (104, 200, 225)
        else:
            color = (204, 249, 250)
        Offsetx = x - self.x
        Offsety = y - self.y
        if self.pattern == 0:
            for point in self.chord:
                center = (round(point.x + Offsetx), round(point.y + Offsety))
                pg.draw.circle(self.screen, color, center, 110, 3 if self.windup else 8)
                pg.draw.circle(self.screen, color, center, 7, 2)
        elif self.pattern == 1:
            for lane in self.lanes:
                rect = lane.move(round(Offsetx), round(Offsety))
                for Yline in range(rect.top, rect.bottom, 34):
                    pg.draw.line(self.screen, color, (rect.left, Yline), (rect.left, Yline + 18), 3)
                    pg.draw.line(self.screen, color, (rect.right, Yline), (rect.right, Yline + 18), 3)
        elif self.pattern == 3:
            for point in self.chord:
                center = (round(point.x + Offsetx), round(point.y + Offsety))
                pg.draw.circle(self.screen, (114, 169, 226), center, 68, 2)
        elif self.pattern == 4:
            if self.windup:
                top = round(self.Wavey + Offsety)
                for gap in (self.Wavegap - 95, self.Wavegap + 95):
                    edge = round(gap + Offsetx)
                    for dy in range(0, 790, 48):
                        pg.draw.line(self.screen, (130, 223, 220), (edge, top + dy), (edge, top + dy + 16), 3)
        else:
            origin = pg.Vector2(x, y)
            for angle in (-30, -15, 0, 15, 30):
                for distance in (105, 155, 205, 255):
                    point = origin + self.aim.rotate(angle) * distance
                    pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 3)


class GuitarBoss(PianoBoss):

    Arenaroom = "Resonance Arena"
    Regionfolder = "GuitarCaverns"
    instrument = "Guitar"
    Homeposition = (GUITARARENAX, GUITARARENAY)

    def Setstats(self):

        self.Maxhp = 1250
        self.Currenthp = self.Maxhp
        self.attack = 48
        self.speed = 145
        self.size = 82

    def footprint(self):

        return 46, 22, 8

    def update(self, dt):

        self.moving = False
        super().update(dt)
        if not self.engaged and self.Currenthp > 0:
            self.x, self.y = self.Homeposition
            return
        if self.Currenthp > 0 and self.recovery > 0 and not self.windup and not self.encore and self.wave is None and self.Attackanimationtime <= 0:
            self.Movetowards(self.player.x, self.player.y, dt, 148)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Pick Rush", "Hammer-On", "Palm Mute", "Pickup Pull", "Fret Slide"][self.pattern]
        self.Winduplength = [0.69, 0.62, 0.92, 0.84, 0.94][self.pattern]
        if self.Secondphase:
            self.Winduplength *= 0.82
        self.windup = self.Winduplength
        self.Wavehit = False
        self.Aimatplayer()

    def Aimatplayer(self):

        aim = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if aim.length_squared():
            self.aim = aim.normalize()

    def Releaseattack(self):

        self.Attackanimationtime = 0.3
        self.strikes += 1
        if not self.Secondphase:
            self.recovery = 1.25
        else:
            self.recovery = 1.02
        if self.pattern == 0:
            self.wave = 0.40
        elif self.pattern == 1:
            self.Hitfront(155, 60, self.attack - 10)
            self.wave = 0.28
        elif self.pattern == 2:
            # Wait out the guard for a longer opening.
            self.recovery += 0.4
        elif self.pattern == 3:
            self.wave = 0.62
        else:
            self.wave = -60

    def Takedamage(self, damage):

        if self.Currenthp > 0 and self.pattern == 2 and self.windup > 0:
            self.windup = 0
            self.strikes += 1
            self.Aimatplayer()
            self.wave = 0.26
            self.recovery = 1.35
            self.Attackanimationtime = 0.3
            return False
        return super().Takedamage(damage)

    def Hitfront(self, reach, Halfwidth, damage):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if 0 <= offset.dot(self.aim) <= reach and abs(offset.cross(self.aim)) <= Halfwidth and self.Canreachplayer():
            self.player.Takedamage(damage)
            return True
        return False

    def Updatefloorattacks(self, dt):

        if self.wave is None:
            return
        if self.pattern == 4:
            self.Updatefretslide(dt)
            return

        Steptime = min(dt, self.wave)
        self.wave -= Steptime
        if self.pattern == 0:
            self.rush(Steptime)
        elif self.pattern == 3:
            self.Pullrogue(Steptime)

        if self.wave == 0:
            self.wave = None
            if self.pattern == 1:
                self.Hitfront(210, 82, self.attack)
                self.Attackanimationtime = 0.3
            elif self.pattern == 2:
                self.Hitfront(180, 65, self.attack + 9)
                self.Attackanimationtime = 0.3
            elif self.pattern == 3:
                self.Hitfront(155, 65, self.attack)
                self.Attackanimationtime = 0.3

    def rush(self, dt):

        move = self.aim * (795 if self.Secondphase else 680) * dt
        steps = max(1, math.ceil(move.length() / 8))
        for step in range(steps):
            if not self.Wavehit and self.Hitfront(105, 57, self.attack + 2):
                self.Wavehit = True
            x, y = self.x + move.x / steps, self.y + move.y / steps
            if not self.Canstep(x, y) or not self.Gamemap.Locationname(x, y).endswith(self.Arenaroom):
                self.wave = 0
                break
            self.x, self.y = x, y

    def Pullrogue(self, dt):

        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if offset.length() > 450 or offset.dot(self.aim) < 0 or abs(offset.cross(self.aim)) > 95:
            return
        if self.player.Dashtime > 0 or not self.Canreachplayer():
            return
        pull = self.aim * (-270 * dt)
        self.player._move(pull.x, pull.y, self.Gamemap)

    def Updatefretslide(self, dt):

        previous = self.wave
        self.wave = min(60, self.wave + (180 if self.Secondphase else 145) * dt)
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if not self.Wavehit and 0 < offset.length() <= 450 + self.player.size:
            angle = (self.aim.angle_to(offset) + 180) % 360 - 180
            margin = math.degrees(math.asin(min(1, (self.player.size + 7) / offset.length())))
            if previous - margin <= angle <= self.wave + margin:
                self.player.Takedamage(self.attack + 4)
                self.Wavehit = True
        if self.wave >= 60:
            self.wave = None

    def Drawwave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        origin = pg.Vector2(x, y)
        copper = (249, 170, 95)
        if self.pattern == 0:
            for angle in (-16, 0, 16):
                pg.draw.line(self.screen, copper, origin, origin - self.aim.rotate(angle) * 58, 4)
        elif self.pattern == 3:
            side = self.aim.rotate(90)
            for i in range(-2, 3):
                point = origin + self.aim * (105 + (i + 2) * 42) + side * i * 14
                pg.draw.line(self.screen, copper, point, point - self.aim * 26, 3)
        elif self.pattern == 4:
            tip = origin + self.aim.rotate(value) * 450
            pg.draw.line(self.screen, (113, 53, 49), origin, tip, 15)
            pg.draw.line(self.screen, (255, 164, 71), origin, tip, 8)
            pg.draw.line(self.screen, (255, 233, 174), origin, tip, 3)

    def Drawwarning(self, x, y):

        if self.windup:
            color = (227, 134, 67)
        else:
            color = (255, 213, 137)
        origin = pg.Vector2(x, y)
        side = self.aim.rotate(90)
        if self.pattern == 0 and self.windup:
            for distance in range(70, 330, 42):
                point = origin + self.aim * distance
                tail = point - self.aim * 18
                pg.draw.lines(self.screen, color, False, [tail + side * 18, point, tail - side * 18], 3)
        elif self.pattern in (1, 2) and (self.pattern == 1 or not self.windup):
            reach = 155 if self.windup else 210
            points = [origin + self.aim.rotate(angle) * reach for angle in range(-32, 33, 8)]
            pg.draw.lines(self.screen, color, False, points, 3)
        elif self.pattern == 2:
            pg.draw.lines(self.screen, (202, 215, 174), False, [(x - 49, y - 55), (x - 36, y - 75), (x + 36, y - 75), (x + 49, y - 55)], 4)
        elif self.pattern == 3:
            for i in (-1, 1):
                start = origin + side * (i * 16)
                end = origin + self.aim * 450 + side * (i * 95)
                pg.draw.line(self.screen, (194, 126, 104), start, end, 2)
        elif self.windup:
            for angle in (-60, 60):
                direction = self.aim.rotate(angle)
                for distance in range(75, 450, 30):
                    pg.draw.line(self.screen, color, origin + direction * distance, origin + direction * (distance + 14), 3)
            points = [origin + self.aim.rotate(angle) * 450 for angle in range(-60, 61, 10)]
            pg.draw.lines(self.screen, color, False, points, 2)


class WindOrb(Projectile):

    def __init__(self, screen, x, y, direction, damage, curve):

        super().__init__(screen, x, y, direction, damage)
        self.curve = curve
        self.speed = 320
        self.size = 13
        self.life = 2.5

    def update(self, dt):

        self.life -= dt
        self.direction = self.direction.rotate(self.curve * dt)
        super().update(dt)

    def Isonscreen(self):

        return self.life > 0 and super().Isonscreen()

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        pg.draw.circle(self.screen, (102, 162, 150), (x, y), 12, 2)
        pg.draw.arc(self.screen, (203, 240, 218), (x - 10, y - 10, 20, 20), 0.4, 4.9, 3)
        pg.draw.circle(self.screen, (223, 240, 229), (x, y), 3)


class FluteBoss(PianoBoss):

    Arenaroom = "Flute Hall"
    Regionfolder = "FluteCloister"
    instrument = "Flute"
    Homeposition = (FLUTEARENAX, FLUTEARENAY)

    def Setstats(self):

        self.Maxhp = 1350
        self.Currenthp = self.Maxhp
        self.attack = 48
        self.size = 82

    def footprint(self):

        return 37, 22, 8

    def Teleportanchor(self):

        for side in (1, -1):
            for offset in (-330, 310, 0):
                x = FLUTEARENAX + 490 * side
                y = FLUTEARENAY + offset
                if math.hypot(x - self.x, y - self.y) > 220 and math.hypot(x - self.player.x, y - self.player.y) > 145 and self.Canstep(x, y):
                    return x, y
        return None

    def Renderteleport(self, camera):

        for index, point in enumerate((self.Teleportorigin, self.Teleporttarget)):
            x, y = camera.apply(*point)
            spin = (1 - self.Teleporttime) * 350 + index * 90
            for i in range(16):
                shift = pg.Vector2(23 + i * 4, 0).rotate(spin + i * 26)
                px, py = round(x + shift.x), round(y + shift.y * 0.5 - i * 3)
                pg.draw.line(self.screen, (165, 215, 197), (px - 9, py + 2), (px + 8, py), 2)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Long Breath", "Spiral Current", "Breathing Space", "Crossdraft", "Reed Wisps"][self.pattern]
        self.Winduplength = [0.82, 0.76, 1.12, 0.85, 0.91][self.pattern]
        if self.Secondphase:
            self.Winduplength *= 0.85
        self.windup = self.Winduplength
        direction = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if direction.length_squared():
            self.aim = direction.normalize()
        if self.player.x > FLUTEARENAX:
            side = -1
        else:
            side = 1
        self.Wavegap = (FLUTEARENAX + side * 265, FLUTEARENAY + 170)
        self.Wavehit = False

    def Releaseattack(self):

        self.Attackanimationtime = 0.3
        self.strikes += 1
        if not self.Secondphase:
            self.recovery = 1.35
        else:
            self.recovery = 1.05
        if self.pattern == 0:
            self.wave = 0.48
        elif self.pattern == 1:
            for angle, curve in [(-35, 68), (0, -74), (35, 68)]:
                self.projectiles.append(WindOrb(self.screen, self.x, self.y, self.aim.rotate(angle), self.attack, curve))
        elif self.pattern == 2:
            if math.hypot(self.player.x - self.Wavegap[0], self.player.y - self.Wavegap[1]) > 170:
                self.player.Takedamage(self.attack + 4)
        elif self.pattern == 3:
            self.wave = 0.68
        else:
            for angle in (-90, 90, 180):
                direction = self.aim.rotate(angle)
                start = pg.Vector2(self.x, self.y) + direction * 95
                if self.Gamemap.Canmovecircle(start.x, start.y, 14):
                    orb = WindOrb(self.screen, start.x, start.y, direction.rotate(70), self.attack - 8, 112)
                    orb.speed = 210
                    self.projectiles.append(orb)

    def Updatefloorattacks(self, dt):

        if self.wave is None:
            return
        elapsed = min(dt, self.wave)
        self.wave -= elapsed
        if self.pattern == 0:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if 0 < offset.length() < 430 and self.aim.dot(offset.normalize()) > 0.78 and self.Canreachplayer():
                if not self.Wavehit:
                    self.player.Takedamage(self.attack)
                    self.Wavehit = True
                push = self.aim * 310 * elapsed
                self.player._move(push.x, push.y, self.Gamemap)
        elif self.pattern == 3 and self.player.Dashtime <= 0:
            side = self.aim.rotate(90)
            push = side * 310 * elapsed
            x, y = self.player.x, self.player.y
            self.player._move(push.x, push.y, self.Gamemap)
            if not self.Wavehit and math.hypot(x - self.player.x, y - self.player.y) < push.length() * 0.30:
                self.player.Takedamage(self.attack - 10)
                self.Wavehit = True
        if self.wave == 0:
            self.wave = None

    def Drawwave(self, camera, value, color):

        if self.pattern == 0:
            x, y = camera.apply(self.x, self.y)
            origin = pg.Vector2(x, y)
            for i in range(-3, 4):
                direction = self.aim.rotate(i * 10)
                for j in range(3):
                    point = origin + direction * (105 + j * 107 + (0.48 - value) * 95)
                    pg.draw.line(self.screen, (163, 220, 198), point, point + direction * 34, 2)
        elif self.pattern == 3:
            x, y = camera.apply(FLUTEARENAX, FLUTEARENAY)
            side = self.aim.rotate(90)
            for i in range(18):
                point = pg.Vector2(x + (i * 83) % 900 - 450, y + (i * 71) % 620 - 310) + side * ((0.68 - value) * 90)
                pg.draw.line(self.screen, (157, 214, 194), point, point + side * 39, 2)

    def Drawwarning(self, x, y):

        color = (133, 207, 181)
        origin = pg.Vector2(x, y)
        if self.pattern == 0:
            for angle in (-38, 38):
                direction = self.aim.rotate(angle)
                for distance in range(75, 430, 43):
                    point = origin + direction * distance
                    pg.draw.line(self.screen, color, point, point + direction * 19, 2)
        elif self.pattern == 1:
            for angle in (-35, 0, 35):
                point = origin + self.aim.rotate(angle) * 110
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 13, 3)
        elif self.pattern == 2:
            safe = (round(x + self.Wavegap[0] - self.x), round(y + self.Wavegap[1] - self.y))
            pg.draw.circle(self.screen, (211, 236, 189), safe, 170, 4)
            pg.draw.circle(self.screen, (107, 158, 144), safe, 162, 2)
        elif self.pattern == 3:
            side = self.aim.rotate(90)
            for i in (-2, -1, 0, 1, 2):
                point = origin + self.aim * (i * 75) + side * 100
                tail = point - side * 24
                pg.draw.lines(self.screen, color, False, [tail + self.aim * 11, point, tail - self.aim * 11], 3)
        else:
            for angle in (-90, 90, 180):
                point = origin + self.aim.rotate(angle) * 95
                pg.draw.circle(self.screen, color, (round(point.x), round(point.y)), 15, 2)


class CelloBoss(PianoBoss):

    Arenaroom = "Cello Amphitheatre"
    Regionfolder = "CelloCatacombs"
    instrument = "Cello"
    Homeposition = (CELLOARENAX, CELLOARENAY)

    def Setstats(self):

        self.Maxhp = 1500
        self.Currenthp = self.Maxhp
        self.attack = 52
        self.speed = 136
        self.size = 84

    def footprint(self):

        return 47, 25, 8

    def update(self, dt):

        self.moving = False
        super().update(dt)
        if not self.engaged and self.Currenthp > 0:
            self.x, self.y = self.Homeposition
            return
        if self.Currenthp > 0 and self.recovery > 0 and not self.windup and not self.encore and self.wave is None and self.Attackanimationtime <= 0:
            self.Movetowards(self.player.x, self.player.y, dt, 145)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Downbow", "Bridge Break", "Legato", "Bow Bind", "Bass Steps"][self.pattern]
        self.Winduplength = [0.78, 0.92, 1.0, 1.0, 0.76][self.pattern]
        if self.Secondphase:
            self.Winduplength *= 0.84
        self.windup = self.Winduplength
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        self.Wavehit = False
        self.chord = []

    def Releaseattack(self):

        self.Attackanimationtime = 0.3
        self.strikes += 1
        if not self.Secondphase:
            self.recovery = 1.4
        else:
            self.recovery = 1.1
        if self.pattern == 0:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if 0 <= offset.dot(self.aim) <= 245 and abs(offset.cross(self.aim)) <= 48 and self.Canreachplayer():
                self.player.Takedamage(self.attack + 7)
        elif self.pattern == 1:
            self.wave = 0.93
        elif self.pattern == 2:
            self.wave = 1.05
            self.Lastbreathposition = (self.player.x, self.player.y)
            self.Breathstill = 0
        elif self.pattern == 3:
            if math.hypot(self.player.x - self.x, self.player.y - self.y) < 265 and self.Canreachplayer():
                self.player.Takedamage(self.attack)
        else:
            self.wave = 0.76
            self.Basssteps = 0

    def Updatefloorattacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
        if self.pattern == 1 and not self.Wavehit:
            reach = (0.93 - self.wave) * 475 + 42
            for angle in (-29, 29):
                line = self.aim.rotate(angle)
                if abs(offset.dot(line) - reach) < 31 and abs(offset.cross(line)) < 42 and self.Canreachplayer():
                    self.player.Takedamage(self.attack)
                    self.Wavehit = True
        elif self.pattern == 2 and not self.Wavehit:
            moved = math.hypot(self.player.x - self.Lastbreathposition[0], self.player.y - self.Lastbreathposition[1])
            self.Lastbreathposition = (self.player.x, self.player.y)
            if moved < dt * 24:
                self.Breathstill = self.Breathstill + dt
            else:
                self.Breathstill = 0
            if self.Breathstill >= 0.38 and offset.length() < 500 and self.Canreachplayer():
                self.player.Takedamage(self.attack - 7)
                self.Wavehit = True
        elif self.pattern == 4:
            beat = 1 if self.wave > 0.37 else 2
            if self.Basssteps < beat:
                self.Basssteps = beat
                self.Movetowards(self.player.x, self.player.y, 0.24, 120)
                if math.hypot(self.player.x - self.x, self.player.y - self.y) < 155 and self.Canreachplayer():
                    self.player.Takedamage(self.attack - 13)
                self.Attackanimationtime = 0.3
        if self.wave == 0:
            self.wave = None

    def Drawwave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        origin = pg.Vector2(x, y)
        if self.pattern == 1:
            reach = (0.93 - value) * 475 + 42
            for angle in (-29, 29):
                direction = self.aim.rotate(angle)
                tip = origin + direction * reach
                pg.draw.line(self.screen, (117, 71, 117), origin, tip, 3)
                pg.draw.circle(self.screen, (219, 194, 237), (round(tip.x), round(tip.y)), 12, 3)
        elif self.pattern == 2:
            px, py = camera.apply(self.player.x, self.player.y)
            if not self.Wavehit:
                pg.draw.arc(self.screen, (217, 190, 234), (px - 29, py - 21, 58, 42), 0, math.tau * min(1, self.Breathstill / 0.38), 3)
        elif self.pattern == 4:
            radius = round(92 + (0.76 - value) % 0.38 * 135)
            pg.draw.ellipse(self.screen, (204, 174, 222), (x - radius, y - radius // 2, radius * 2, radius), 3)

    def Drawwarning(self, x, y):

        origin = pg.Vector2(x, y)
        color = (212, 184, 229)
        side = self.aim.rotate(90)
        if self.pattern == 0:
            end = origin + self.aim * 245
            if self.windup:
                pg.draw.lines(self.screen, color, False, [origin + side * 28, end + side * 48, end - side * 48, origin - side * 28], 3)
            else:
                pg.draw.polygon(self.screen, (109, 65, 111), [origin + side * 13, end, origin - side * 13])
                pg.draw.line(self.screen, (237, 215, 246), origin, end, 4)
        elif self.pattern == 1:
            for angle in (-29, 29):
                direction = self.aim.rotate(angle)
                for distance in range(58, 475, 38):
                    point = origin + direction * distance
                    pg.draw.line(self.screen, color, point, point + direction * 19, 2)
        elif self.pattern == 2:
            for index in range(3):
                length = 28 + index * 15
                pg.draw.arc(self.screen, (216, 187, 231), (x - length, y - 71 + index * 11, length * 2, 33), 0.15, 2.9, 2)
        elif self.pattern == 3:
            offset = pg.Vector2(self.player.x - self.x, self.player.y - self.y)
            if offset.length() < 265 and self.Canreachplayer():
                end = origin + offset
                bend = origin.lerp(end, 0.5) + offset.rotate(90) * 0.08
                pg.draw.lines(self.screen, (87, 52, 95), False, [origin, bend, end], 6)
                pg.draw.lines(self.screen, (222, 191, 236), False, [origin, bend, end], 2)
            pg.draw.circle(self.screen, (197, 168, 218), (x, y), 265, 2)
        else:
            pg.draw.ellipse(self.screen, color, (x - 155, y - 77, 310, 154), 2)


class HarpBoss(PianoBoss):

    Arenaroom = "Harp Chamber"
    Regionfolder = "HarpReservoir"
    instrument = "Harp"
    Homeposition = (HARPARENAX, HARPARENAY)

    def Setstats(self):

        self.Maxhp = 1650
        self.Currenthp = self.Maxhp
        self.attack = 55
        self.size = 87

    def footprint(self):

        return 45, 23, 10

    def Teleportanchor(self):

        for step in range(4):
            Sidex, Sidey = [(-1, -1), (1, 1), (1, -1), (-1, 1)][(step + self.Teleportindex) % 4]
            x = HARPARENAX + Sidex * 460
            y = HARPARENAY + Sidey * 375
            if math.hypot(x - self.player.x, y - self.player.y) > 180 and math.hypot(x - self.x, y - self.y) > 180 and self.Canstep(x, y):
                return x, y
        return None

    def Renderteleport(self, camera):

        for point in (self.Teleportorigin, self.Teleporttarget):
            x, y = camera.apply(*point)
            for offset in (0, 22, 44):
                radius = round(22 + (1 - self.Teleporttime) * 75 + offset)
                pg.draw.ellipse(self.screen, (103, 207, 187), (x - radius, y - radius // 2, radius * 2, radius), 2)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Tide Wells", "Crosscurrent", "Plucked Cascade", "Undertow", "Breaking String"][self.pattern]
        self.Winduplength = [1.02, 0.92, 0.82, 1.10, 0.98][self.pattern]
        if self.Secondphase:
            self.Winduplength *= 0.85
        self.windup = self.Winduplength
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target + side * shift for shift in (-230, 0, 230)]
        self.lanes = [pg.Rect(HARPARENAX - 600, round(target.y + shift - 44), 1200, 88) for shift in (-205, 0, 205)]
        self.Wavehit = False

    def Makenote(self, direction):

        bolt = Projectile(self.screen, self.x, self.y, direction, self.attack - 14)
        bolt.speed = 330
        bolt.size = 14
        bolt.colour = (126, 231, 207)
        return bolt

    def Releaseattack(self):

        self.strikes += 1
        self.Attackanimationtime = 0.3
        if self.Secondphase:
            self.recovery = 1.55
        else:
            self.recovery = 1.85
        if self.pattern == 2:
            self.volley = [-34, -17, 0, 17, 34]
            self.Beattimer = 0
        elif self.pattern == 3:
            self.wave = 1.0
        else:
            self.wave = 0.34

    def Updatefloorattacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if self.pattern == 0:
            hit = any(target.distance_to(point) <= 92 for point in self.chord)
        elif self.pattern == 1:
            hit = any(lane.collidepoint(target.x, target.y) for lane in self.lanes)
        elif self.pattern == 3:
            hit = abs(offset.length() - (570 * self.wave + 52)) <= 26
        else:
            hit = 0 <= offset.dot(self.aim) <= 620 and abs(offset.cross(self.aim)) <= 54
        if hit and not self.Wavehit:
            self.player.Takedamage(self.attack)
            self.Wavehit = True
        if self.wave == 0:
            self.wave = None

    def Drawwarning(self, x, y):

        if self.windup > 0:
            self.Drawpattern(x, y, (106, 187, 176), 1.0)

    def Drawwave(self, camera, value, color):

        self.Drawpattern(*camera.apply(self.x, self.y), (157, 246, 222), value)

    def Drawpattern(self, x, y, colour, value):

        shift = pg.Vector2(x - self.x, y - self.y)
        origin = pg.Vector2(x, y)
        if self.pattern == 0:
            for point in self.chord:
                center = point + shift
                pg.draw.circle(self.screen, colour, center, 92, 3)
                pg.draw.circle(self.screen, colour, center, 74, 1)
        elif self.pattern == 1:
            for lane in self.lanes:
                pg.draw.rect(self.screen, colour, lane.move(round(shift.x), round(shift.y)), 3)
        elif self.pattern == 2:
            for angle in (-34, -17, 0, 17, 34):
                direction = self.aim.rotate(angle)
                pg.draw.line(self.screen, colour, origin + direction * 85, origin + direction * 225, 2)
        elif self.pattern == 3:
            radius = round(570 * value + 52)
            for edge in (radius - 26, radius, radius + 26):
                pg.draw.circle(self.screen, colour, origin, edge, 4 if edge == radius else 1)
        else:
            side = self.aim.rotate(90) * 54
            end = origin + self.aim * 620
            pg.draw.lines(self.screen, colour, True, [origin + side, end + side, end - side, origin - side], 3)

    def Keeperframe(self):

        if self.Teleporttime > 0:
            frame = self.Keeperposes[0].copy()
            frame.set_alpha(round(255 * abs(self.Teleporttime - 0.5) * 2))
            return frame
        if self.windup > 0 and self.windup < self.Winduplength * 0.73:
            return self.Keeperposes[1]
        if self.Attackanimationtime > 0:
            return self.Keeperposes[2 if self.Attackanimationtime > 0.085 else 4]
        if self.volley:
            return self.Keeperposes[2 if self.Beattimer > 0.06 else 1]
        if self.encore:
            return self.Keeperposes[1]
        return self.Keeperposes[0]

    def render(self, camera):

        super().render(camera)
        if self.Currenthp <= 0 or self.Teleporttime > 0:
            return
        if self.Attackanimationtime <= 0 and not self.volley:
            return
        if self.Attackanimationtime:
            progress = 1 - self.Attackanimationtime / 0.3
        else:
            progress = 1 - min(1, self.Beattimer / 0.105)
        x, y = camera.apply(self.x, self.y)
        for index in range(5):
            spread = progress * (15 + index * 4)
            px = round(x + 46 + index * 4 + spread)
            py = round(y - 181 + index * 18 - spread * 0.36)
            if progress < 0.55:
                colour = (164, 242, 219)
            else:
                colour = (93, 171, 160)
            pg.draw.line(self.screen, colour, (px, py), (px + 4, py - 3), 2)


class ViolinBoss(PianoBoss):

    Arenaroom = "Performance Hall"
    Regionfolder = "ViolinHall"
    instrument = "Violin"
    Homeposition = (10880, 20320)

    def Setstats(self):

        self.Maxhp = 1750
        self.Currenthp = self.Maxhp
        self.attack = 56
        self.size = 65

    def footprint(self):

        return 29, 17, 7

    def Teleportanchor(self):

        for step in range(4):
            dx, dy = [(-470, -340), (470, 340), (470, -340), (-470, 340)][(self.Teleportindex + step) % 4]
            x, y = self.Homeposition[0] + dx, self.Homeposition[1] + dy
            if math.hypot(x - self.x, y - self.y) > 160 and math.hypot(x - self.player.x, y - self.player.y) > 165 and self.Canstep(x, y):
                return x, y
        return None

    def Renderteleport(self, camera):

        for point in (self.Teleportorigin, self.Teleporttarget):
            x, y = camera.apply(*point)
            progress = 1 - abs(2 * self.Teleporttime - 1)
            for offset in (-24, 0, 24):
                height = round(20 + 95 * progress)
                pg.draw.line(self.screen, (208, 151, 177), (x + offset, y), (x + offset, y - height), 2)

    def Startphrase(self):

        self.pattern = self.strikes % 5
        self.Movename = ["Bow Cut", "Crossed Strings", "Three Marks", "Pinch", "Final Rest"][self.pattern]
        self.Winduplength = [0.79, 0.98, 0.89, 1.04, 1.12][self.pattern]
        if self.Secondphase:
            self.Winduplength *= 0.85
        self.windup = self.Winduplength
        target = pg.Vector2(self.player.x, self.player.y)
        offset = target - (self.x, self.y)
        if offset.length_squared():
            self.aim = offset.normalize()
        side = self.aim.rotate(90)
        self.chord = [target - side * 168, target, target + side * 168]
        self.Wavehit = False

    def Releaseattack(self):

        self.strikes += 1
        self.Attackanimationtime = 0.3
        if self.Secondphase:
            self.recovery = 1.5
        else:
            self.recovery = 1.8
        if self.pattern in (2, 3):
            self.wave = 0.78
        else:
            self.wave = 0.32

    def Stringlines(self, value):

        if self.pattern == 0:
            return [(pg.Vector2(self.x, self.y), self.aim, 400, 32)]
        if self.pattern == 1:
            return [(self.chord[1], self.aim.rotate(angle), 470, 29) for angle in (-39, 39)]
        side = self.aim.rotate(90)
        gap = 54 + round(138 * value / 0.78)
        return [(self.chord[1] + side * offset, self.aim, 490, 28) for offset in (-gap, gap)]

    def Updatefloorattacks(self, dt):

        if self.wave is None:
            return
        self.wave = max(0, self.wave - dt)
        point = pg.Vector2(self.player.x, self.player.y)
        if self.pattern == 2:
            index = min(2, int((0.78 - self.wave) / 0.26))
            hit = point.distance_to(self.chord[index]) <= 76
        elif self.pattern == 4:
            hit = 145 <= point.distance_to((self.x, self.y)) <= 425
        else:
            hit = False
            for origin, direction, length, width in self.Stringlines(self.wave):
                offset = point - origin
                start = 0 if self.pattern == 0 else -length
                if start <= offset.dot(direction) <= length and abs(offset.cross(direction)) <= width:
                    hit = True
        if hit and not self.Wavehit:
            self.player.Takedamage(self.attack)
            self.Wavehit = True
        if self.wave == 0:
            self.wave = None

    def Drawwarning(self, x, y):

        if self.windup > 0:
            self.Drawstrings(x, y, (186, 145, 175), 0.78, True)

    def Drawwave(self, camera, value, color):

        x, y = camera.apply(self.x, self.y)
        self.Drawstrings(x, y, (236, 188, 207), value, False)

    def Drawstrings(self, x, y, colour, value, warning):

        shift = pg.Vector2(x - self.x, y - self.y)
        if self.pattern == 2:
            index = min(2, int((0.78 - value) / 0.26))
            if warning:
                marks = self.chord
            else:
                marks = [self.chord[index]]
            for point in marks:
                pg.draw.circle(self.screen, colour, point + shift, 76, 3)
                if not warning:
                    pg.draw.circle(self.screen, colour, point + shift, 61, 2)
        elif self.pattern == 4:
            for radius in (145, 425):
                pg.draw.circle(self.screen, colour, (x, y), radius, 3)
            if not warning:
                pg.draw.circle(self.screen, colour, (x, y), round(145 + 280 * value / 0.32), 2)
        else:
            for point, direction, length, width in self.Stringlines(value):
                point = point + shift
                if self.pattern == 0:
                    start = point
                else:
                    start = point - direction * length
                end = point + direction * length
                side = direction.rotate(90) * width
                pg.draw.lines(self.screen, colour, True, [start - side, end - side, end + side, start + side], 2)
                if not warning:
                    pg.draw.line(self.screen, colour, start, end, 4)
            if self.pattern == 3 and warning:
                for point, direction, length, width in self.Stringlines(0):
                    start = point + shift - direction * length
                    pg.draw.line(self.screen, colour, start, start + direction * length * 2, 1)

    def Keeperframe(self):

        if self.Teleporttime:
            frame = self.Keeperposes[0].copy()
            frame.set_alpha(round(510 * abs(self.Teleporttime - 0.5)))
            return frame
        index = 0
        if self.windup > 0:
            progress = 1 - self.windup / self.Winduplength
            if progress >= 0.22:
                index = 1
        elif self.Attackanimationtime > 0:
            if self.Attackanimationtime >= 0.10:
                index = 2
            else:
                index = 1
        elif self.encore > 0:
            index = 1
        frame = self.Keeperposes[index]
        return pg.transform.flip(frame, True, False) if self.aim.x < 0 else frame

    def render(self, camera):

        super().render(camera)
        if self.Currenthp <= 0 or self.Teleporttime > 0 or self.Attackanimationtime <= 0.10:
            return
        progress = 1 - self.Attackanimationtime / 0.3
        x, y = camera.apply(self.x, self.y)
        Offsetx, Offsety = Bossposeoffset(self)
        x += Offsetx
        y += Offsety
        side = -1 if self.aim.x < 0 else 1
        reach = round(20 * progress)
        if progress < 0.38:
            colour = (217, 170, 185)
        else:
            colour = (156, 111, 144)
        start = (x + side * (31 + reach), y - 105 + reach // 2)
        middle = (x + side * (47 + reach), y - 97 + reach)
        end = (x + side * (59 + reach), y - 86 + reach)
        pg.draw.lines(self.screen, colour, False, [start, middle, end], 2)
