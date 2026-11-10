import math
from pathlib import Path
import pygame as pg
from Items import CLASSES, equip
from RogueArt import DIRECTIONS, Colourrobe
from FamiliarArt import FamiliarArt

# HP, mana, speed, defence, starter weapon, starter shield, robe, three passives.
CLAN = {
    "Mage": (85, 150, 490, 32, "Ivory Focus", "Ivory Ward", (101, 156, 225), ("Deep mana pool", "Quick mana recovery", "Elemental skill damage")),
    "Tank": (155, 80, 420, 83, "Ivory Maul", "Ivory Tower", (172, 133, 82), ("Heavy defence", "Extra health", "Stronger guard")),
    "Fighter": (120, 95, 510, 56, "Ivory Blade", "Ivory Kite", (189, 93, 104), ("Heavy weapon damage", "Sturdy defence", "Faster swings")),
    "Assassin": (90, 95, 610, 35, "Ivory Knife", "Ivory Buckler", (127, 103, 184), ("Fast movement", "Lower enemy detection", "Passive lifesteal")),
    "Summoner": (100, 135, 470, 45, "Copper Focus", "Ivory Ward", (113, 176, 133), ("Deep mana pool", "Long-lived familiar", "Damage reduction with familiar")),
    "Marksman": (95, 105, 545, 37, "Ivory Bow", "Ivory Heater", (205, 158, 105), ("Longer shot range", "Faster projectiles", "Quick movement"))
}
SKILLS = {
    "Mage": [("Fireball", 24, 5), ("Lightning Bolt", 25, 6), ("Ice Rain", 29, 8), ("Waterfall", 16, 4)],
    "Tank": [("Charge", 18, 5), ("Shockwave", 23, 7), ("Juggernaut", 25, 10), ("Shield", 34, 14)],
    "Fighter": [("Slash", 17, 4), ("Stab", 21, 6), ("Sweep", 25, 7), ("Pierce", 20, 8)],
    "Assassin": [("Teleport", 27, 12), ("Sneak", 17, 6), ("Blind", 28, 7), ("Lifesteal", 33, 8)],
    "Summoner": [("Summon", 0, 12), ("Buff", 22, 7), ("Sacrifice", 18, 10), ("Stun", 13, 7)],
    "Marksman": [("Missile", 22, 5), ("True Strike", 18, 6), ("Piercing", 24, 7), ("Arrow Rain", 31, 11)]
}


def Chooseclass(display, screen, frame):

    selected = 3
    title = pg.font.Font(None, 49)
    body = pg.font.Font(None, 27)
    small = pg.font.Font(None, 22)
    clock = pg.time.Clock()
    cards = [pg.Rect(140 + index % 2 * 220, 255 + index // 2 * 115, 190, 62) for index in range(6)]
    base = Path(__file__).resolve().parent / "Images" / "Characters" / "Rogue" / "Directional" / "Rogue_0.png"
    rogue = pg.image.load(base).convert_alpha()
    portraits = [pg.transform.scale_by(Colourrobe(rogue.copy(), CLAN[name][6]), 1.55) for name in CLASSES]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return None
            if event.type == pg.VIDEORESIZE:
                scale = min(event.w / screen.get_width(), event.h / screen.get_height())
                frame.size = (round(screen.get_width() * scale), round(screen.get_height() * scale))
                frame.center = display.get_rect().center
            if event.type == pg.KEYDOWN:
                if pg.K_1 <= event.key <= pg.K_6:
                    selected = event.key - pg.K_1
                elif event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                    selected = (selected + {pg.K_LEFT:-1, pg.K_RIGHT:1, pg.K_UP:-2, pg.K_DOWN:2}[event.key]) % 6
                elif event.key == pg.K_RETURN:
                    return CLASSES[selected]
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and frame.collidepoint(event.pos):
                x = (event.pos[0] - frame.x) * screen.get_width() / frame.width
                y = (event.pos[1] - frame.y) * screen.get_height() / frame.height
                for index, card in enumerate(cards):
                    if card.collidepoint(x, y):
                        if selected == index:
                            return CLASSES[index]
                        selected = index
                        break
        screen.fill((19, 18, 22))
        pg.draw.rect(screen, (145, 145, 150), (34, 30, 1132, 740), 1)
        pg.draw.lines(screen, (132, 132, 138), True, [(198, 83), (1002, 83), (1027, 125), (1002, 167), (198, 167), (173, 125)], 1)
        heading = title.render("Clan Selection", True, (231, 216, 199))
        screen.blit(heading, heading.get_rect(center=(600, 125)))
        for index, name in enumerate(CLASSES):
            card = cards[index]
            colour = CLAN[name][6]
            pg.draw.rect(screen, (25, 39, 64) if index == selected else (24, 22, 28), card, border_radius=7)
            pg.draw.rect(screen, (163, 168, 179) if index == selected else (110, 110, 115), card, 1, border_radius=7)
            label = body.render(name, True, colour if index == selected else (215, 202, 198))
            screen.blit(label, label.get_rect(center=card.center))
        detail = pg.Rect(632, 240, 422, 335)
        pg.draw.rect(screen, (27, 24, 31), detail)
        pg.draw.rect(screen, (110, 110, 115), detail, 1)
        name = CLASSES[selected]
        hp, mana, speed, defence, weapon, shield, robe, passives = CLAN[name]
        screen.blit(body.render(name, True, robe), (653, 258))
        screen.blit(portraits[selected], portraits[selected].get_rect(topright=(1035, 255)))
        screen.blit(small.render(f"{hp} HP   {mana} mana   {defence} defence", True, (220, 206, 200)), (653, 299))
        for i, passive in enumerate(passives):
            screen.blit(small.render(passive, True, (196, 181, 191)), (653, 337+i*22))
        for i, (skill, cost, _) in enumerate(SKILLS[name]):
            screen.blit(small.render(f"{i+1}   {skill}", True, robe), (653, 430+i*27))
        hint = small.render("Arrows or 1-6 to select   |   Enter to begin", True, (189, 168, 155))
        screen.blit(hint, hint.get_rect(center=(600, 685)))
        display.fill((0, 0, 0))
        display.blit(pg.transform.scale(screen, frame.size), frame)
        pg.display.flip()
        clock.tick(30)


class FamiliarTarget:

    size = 18
    Dashtime = 0
    powers = None
    clan = "Familiar"

    def __init__(self, powers):

        self.owner = powers
        self.Maxhp = max(1, powers.player.Maxhp // 2)
        self.Currenthp = self.Maxhp

    @property
    def x(self):
        return self.owner.familiar.x if self.owner.familiar is not None else self.owner.Familiarlast.x

    @property
    def y(self):
        return self.owner.familiar.y if self.owner.familiar is not None else self.owner.Familiarlast.y

    def Takedamage(self, damage):

        if self.owner.familiar is None:
            return 0
        damage = min(self.Currenthp, max(1, round(damage)))
        self.Currenthp -= damage
        if self.Currenthp <= 0:
            self.owner.Endfamiliar()
        return damage

    def _move(self, dx, dy, Gamemap):

        if self.owner.familiar is not None and Gamemap.Canmovecircle(self.x+dx, self.y+dy, self.size):
            self.owner.familiar += pg.Vector2(dx, dy)


class ClanPowers:

    def __init__(self, player, name):

        self.player = player
        self.name = name
        self.cooldowns = [0.0] * 4
        self.effects = {}
        self.stunned = {}
        self.visuals = []
        self.Casttrails = []
        self.pending = []
        self.marked = None
        self.familiar = None
        self.Familiarlast = pg.Vector2()
        self.Familiaractor = None
        self.Familiartime = 0
        self.Familiarhit = 0
        self.Familiarattack = 0
        self.Familiartarget = None
        self.Familiardirection = 1
        self.Familiardeparture = None
        if name == "Summoner":
            self.Familiarart = FamiliarArt()
        else:
            self.Familiarart = None
        self.map = None

    def Leavearea(self):

        self.familiar = None
        self.Familiardeparture = None
        self.Familiartarget = None
        self.pending.clear()
        self.Casttrails.clear()
        self.visuals.clear()
        self.marked = None
        self.effects.pop("True Strike", None)

    def Endfamiliar(self, sacrifice=False):

        if self.familiar is not None:
            self.Familiarlast = self.familiar.copy()
            self.Familiardeparture = (self.Familiarlast, 0.0, sacrifice)
        self.familiar = None
        self.Familiarattack = 0
        self.Familiartarget = None

    def active(self, name):

        return self.effects.get(name, 0) > 0

    def Speedfactor(self):

        if self.active("Sacrifice"):
            return 1.7
        if self.active("Sneak"):
            return .63
        return 1

    def hit(self, enemy, damage):

        if self.active("Juggernaut") or self.active("Sacrifice"):
            damage = round(damage * (1.7 if self.active("Sacrifice") else 1.4))
        if self.active("Pierce"):
            damage = round(damage * 1.5)
            self.effects.pop("Pierce")
        old = enemy.Currenthp
        enemy.Takedamage(damage)
        dealt = max(0, old - max(0, enemy.Currenthp))
        ratio = .32 if self.active("Lifesteal") else .09 if self.name == "Assassin" else 0
        self.player.Currenthp = min(self.player.Maxhp, self.player.Currenthp + round(dealt * ratio))

    def nearby(self, point, radius):

        return [enemy for enemy in self.player.enemies if enemy.Currenthp > 0 and point.distance_to((enemy.x, enemy.y)) <= radius]

    def visible(self, start, enemy):

        return self.map.Clearenemypath(start.x, start.y, enemy.x, enemy.y, 3)

    def pulse(self, point, radius, damage, colour):

        for enemy in self.nearby(point, radius):
            if self.visible(point, enemy):
                self.hit(enemy, damage)
        self.visuals.append((point, radius, colour, .48))

    def line(self, start, direction, distance, width, damage, piercing=False):

        targets = []
        for enemy in self.nearby(start, distance + 70):
            delta = pg.Vector2(enemy.x, enemy.y) - start
            along = delta.dot(direction)
            if 0 < along <= distance and abs(delta.cross(direction)) <= width + enemy.Bodyradius() and self.visible(start, enemy):
                targets.append((along, enemy))
        targets.sort(key=lambda entry: entry[0])
        for _, enemy in (targets if piercing else targets[:1]):
            self.hit(enemy, damage)
        end = start + direction * (distance if piercing or not targets else targets[0][0])
        self.Casttrails.append((start, end, CLAN[self.name][6], .30, .30))

    def cast(self, index, cursor, Gamemap):

        self.map = Gamemap
        p = self.player
        name, cost, cooldown = SKILLS[self.name][index]
        if name == "Summon":
            if self.familiar is not None:
                self.Endfamiliar()
                return "Familiar dismissed."
            cost = p.Maxmana / 2
        if self.familiar is not None and name not in ("Buff", "Sacrifice"):
            return "Dismiss the familiar before casting another skill."
        if p.Currenthp <= 0 or p.Attackstage or p.Dashtime or p.Blocktime:
            return "Finish your current action first."
        if self.cooldowns[index] > 0:
            return f"{name} is recovering."
        if p.Currentmana < cost:
            return "Not enough mana."
        if name in ("Buff", "Sacrifice") and self.familiar is None:
            return "Summon a familiar first."
        start = pg.Vector2(p.x, p.y)
        target = pg.Vector2(cursor)
        delta = target - start
        if delta.length_squared():
            direction = delta.normalize()
        else:
            direction = pg.Vector2(0, 1)
        target = start + direction * min(delta.length(), 510)
        colour = CLAN[self.name][6]
        if name in ("Fireball", "Lightning Bolt", "Ice Rain", "Waterfall", "Arrow Rain"):
            if not self.map.Clearenemypath(start.x, start.y, target.x, target.y, 3):
                return "Aim at a clear spot."
            radius, damage, colour = {"Fireball":(115, 37, (240, 112, 79)), "Lightning Bolt":(92, 39, (242, 213, 137)), "Ice Rain":(155, 31, (135, 209, 239)), "Waterfall":(115, 27, (113, 180, 225)), "Arrow Rain":(153, 42, colour)}[name]
            if name == "Fireball":
                duration = max(.15, start.distance_to(target)/1000)
                self.Casttrails.append((start, target, colour, duration, duration))
                self.pending.append((target, radius, damage, colour, duration))
            elif name in ("Ice Rain", "Arrow Rain"):
                for delay in (.15, .32, .49):
                    self.pending.append((target, radius, round(damage/3), colour, delay))
                self.visuals.append((target, radius, colour, .52))
            else:
                if name == "Lightning Bolt":
                    self.Casttrails.append((target + pg.Vector2(0, -185), target, colour, .25, .25))
                self.pulse(target, radius, damage, colour)
        elif name in ("Missile", "Piercing"):
            self.line(start, direction, 560, 26, round(p.attack*1.65) if name=="Missile" else p.attack, name=="Piercing")
        elif name == "True Strike":
            targets = [enemy for enemy in self.nearby(target, 100) if start.distance_to((enemy.x, enemy.y)) <= 560]
            if not targets:
                return "Aim closer to an enemy."
            enemy = min(targets, key=lambda enemy: target.distance_to((enemy.x, enemy.y)))
            self.marked = enemy
            self.effects["True Strike"] = 8
            self.visuals.append((pg.Vector2(enemy.x, enemy.y), 24, colour, .4))
        elif name == "Teleport":
            target = start + direction * min(delta.length(), 620)
            if not p.Canmoveto(target.x, target.y, Gamemap) or not Gamemap.Clearenemypath(start.x, start.y, target.x, target.y, 3):
                return "Choose a clear destination."
            p.x, p.y = target
            self.visuals.append((start, 34, colour, .36))
            self.visuals.append((target, 34, colour, .36))
        elif name == "Charge":
            forward = pg.Vector2(DIRECTIONS[p.facing]).normalize()
            for _ in range(20):
                p._move(forward.x * 7, forward.y * 7, Gamemap)
            end = pg.Vector2(p.x, p.y)
            for enemy in p.Meleetargets(p.enemies, end, forward, 85, Gamemap):
                self.hit(enemy, p.attack)
            self.Casttrails.append((start, end, colour, .28, .28))
        elif name == "Shockwave":
            self.pulse(start, 170, p.attack + 10, colour)
        elif name in ("Slash", "Stab"):
            forward = pg.Vector2(DIRECTIONS[p.facing]).normalize()
            reach = 135 if name == "Slash" else 168
            targets = list(p.Meleetargets(p.enemies, start, forward, reach, Gamemap))
            if name == "Stab":
                targets.sort(key=lambda enemy: start.distance_to((enemy.x, enemy.y)))
                targets = targets[:1]
                self.effects["Stab"] = .45
            for enemy in targets:
                self.hit(enemy, p.attack * 2 if name == "Slash" else round(p.attack * 2.5))
            self.Casttrails.append((start, start + forward * reach, colour, .28, .28))
        elif name == "Sweep":
            for _ in range(3):
                self.pulse(start, 120, max(1, p.attack//2), colour)
        elif name in ("Blind", "Stun"):
            affected = self.nearby(start if name=="Blind" else target, 190 if name=="Blind" else 94)
            for enemy in affected:
                if enemy.Directionalmob:
                    self.stunned[enemy] = 2.2
            self.visuals.append((start if name=="Blind" else target, 120, colour, .44))
        elif name == "Summon":
            self.familiar = start + direction * 35
            if not Gamemap.Canmovecircle(self.familiar.x, self.familiar.y, 12):
                self.familiar = start
            self.Familiaractor = FamiliarTarget(self)
            self.Familiartime = 12
            self.Familiarhit = self.Familiarattack = 0
        elif name == "Sacrifice":
            self.Endfamiliar(sacrifice=True)
            self.effects[name] = 10
        else:
            self.effects[name] = {"Buff":6, "Juggernaut":6, "Shield":2.2, "Sneak":5, "Lifesteal":6, "Pierce":8}[name]
            self.visuals.append((start, 48, colour, .45))
        p.Currentmana -= cost
        self.cooldowns[index] = cooldown
        return "Buff: your guard is strengthened." if name == "Buff" else name

    def update(self, dt):

        p = self.player
        p.Currentmana = min(p.Maxmana, p.Currentmana + dt * (9 if self.name=="Mage" else 6))
        self.cooldowns = [max(0, timer - dt) for timer in self.cooldowns]
        for name in list(self.effects):
            self.effects[name] -= dt
            if self.effects[name] <= 0:
                del self.effects[name]

        for enemy in list(self.stunned):
            self.stunned[enemy] -= dt
            if self.stunned[enemy] <= 0 or enemy.Currenthp <= 0:
                del self.stunned[enemy]
        self.visuals = [(point, radius, colour, time-dt) for point, radius, colour, time in self.visuals if time>dt]
        self.Casttrails = [(a, b, c, time-dt, total) for a, b, c, time, total in self.Casttrails if time>dt]
        waiting = []
        for point, radius, damage, colour, time in self.pending:
            if time <= dt:
                self.pulse(point, radius, damage, colour)
            else:
                waiting.append((point, radius, damage, colour, time-dt))
        self.pending = waiting
        if self.Familiardeparture:
            point, elapsed, sacrifice = self.Familiardeparture
            elapsed += dt
            if elapsed < (.65 if sacrifice else .38):
                self.Familiardeparture = (point, elapsed, sacrifice)
            else:
                self.Familiardeparture = None
        if self.familiar is None:
            return
        self.Familiartime -= dt
        if self.Familiartime <= 0:
            self.Endfamiliar()
            return
        self.Familiarhit = max(0, self.Familiarhit-dt)
        if self.Familiarattack > 0:
            previous = self.Familiarattack
            self.Familiarattack = max(0, previous-dt)
            enemy = self.Familiartarget
            if previous > .16 >= self.Familiarattack and enemy.Currenthp > 0 and self.familiar.distance_to((enemy.x, enemy.y)) <= 70 and self.visible(self.familiar, enemy):
                enemy.Takedamage(max(1, round(p.attack*.5)))
            return
        targets = [enemy for enemy in self.nearby(self.familiar, 1050) if self.visible(self.familiar, enemy)]
        if not targets:
            return
        enemy = min(targets, key=lambda enemy: self.familiar.distance_to((enemy.x, enemy.y)))
        delta = pg.Vector2(enemy.x, enemy.y) - self.familiar
        if delta.x:
            if delta.x > 0:
                self.Familiardirection = 1
            else:
                self.Familiardirection = -1
        if delta.length() > 55:
            step = self.familiar + delta.normalize() * 170 * dt
            if self.map.Canmovecircle(step.x, step.y, 12):
                self.familiar = step
        elif self.Familiarhit == 0 and self.visible(self.familiar, enemy):
            self.Familiartarget = enemy
            self.Familiarattack = .30
            self.Familiarhit = .65

    def render(self, screen, camera):

        for start, end, colour, time, total in self.Casttrails:
            progress = 1-time/total
            front = start.lerp(end, min(1, progress+.15))
            tail = start.lerp(end, max(0, progress-.18))
            pg.draw.line(screen, colour, camera.apply(tail.x, tail.y), camera.apply(front.x, front.y), 3)
        for point, radius, colour, time in self.visuals:
            x, y = camera.apply(point.x, point.y)
            size = max(4, round(radius*(1-time*.75)))
            pg.draw.circle(screen, colour, (x, y), size, 2)
        if self.active("Buff"):
            x, y = camera.apply(self.player.x, self.player.y)
            pg.draw.ellipse(screen, (128, 176, 145), (x-27, y-8, 54, 17), 2)
        if self.familiar is not None:
            point = camera.apply(self.familiar.x, self.familiar.y)
            self.Familiarart.render(screen, point, self.player.Animationtime, self.Familiarattack, self.Familiardirection)
            health = self.Familiaractor.Currenthp / self.Familiaractor.Maxhp
            pg.draw.rect(screen, (29, 24, 39), (point[0]-18, point[1]-67, 36, 5))
            pg.draw.rect(screen, (145, 204, 157), (point[0]-18, point[1]-67, round(36*health), 5))
        if self.Familiardeparture:
            point, elapsed, sacrifice = self.Familiardeparture
            self.Familiarart.vanish(screen, camera.apply(point.x, point.y), elapsed/(.65 if sacrifice else .38), sacrifice)


def Configureclass(player, name):

    hp, mana, speed, defence, weapon, shield, robe, passives = CLAN[name]
    player.clan = name
    player.Maxhp = player.Currenthp = hp
    player.Maxmana = player.Currentmana = mana
    player.speed = speed
    player.Basedefence = player.defence = defence
    player.powers = ClanPowers(player, name)
    player.art = type(player.art)(robe, getattr(player, 'character', 'Male'))
    equip(player, weapon)
    equip(player, shield)
    if name == "Fighter":
        player.Attackdelay *= .86
    return {weapon:1, shield:1}
