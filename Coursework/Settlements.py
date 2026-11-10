import math
from TownArt import Townhouse, Streetprop
import pygame as pg
from Items import LOOTSETS, POTIONS

VILLAGENAMES = ("Lanternwick", "Ivory Hearth", "Copper Rest", "Reed Crossing", "Rosinstead", "Tidewatch", "Rosewood End")
HOUSES = ("Keeper's Cottage", "Workshop", "Reading Room", "Market Hall", "Inn", "Storehouse", "Gardener's House", "Watch House", "Loom House")
RESIDENTS = ("Mara", "Iven", "Tessa", "Neris", "Orrin", "Sela", "Vera")
STONEORDERS = ((2, 1, 3), (3, 1, 2), (1, 3, 2), (2, 3, 1), (3, 2, 1), (1, 2, 3), (3, 1, 2))
TOWNLOTS = ((-390, -210), (0, -210), (390, -210), (-780, 135), (780, 135), (-780, 485), (780, 485), (-390, 700), (390, 700))
GATEROOMS = ("Lantern Shelter", "Snow Court", "String Hollow", "Open Cloister", "Silt Court", "Dark Reservoir", "Lantern Court")
GROUND = ((73, 80, 77), (84, 105, 115), (108, 77, 61), (89, 94, 82), (113, 88, 64), (64, 99, 93), (91, 69, 86))
WORLDWIDTH = 72000
WORLDHEIGHT = 56000


def Villagersprite(region):

    sprite = pg.Surface((22, 25), pg.SRCALPHA)
    hair, skin, coat = [
        ((104, 62, 38), (214, 158, 109), (80, 107, 133)),
        ((159, 128, 89), (225, 173, 128), (91, 119, 146)),
        ((62, 42, 41), (166, 109, 79), (143, 81, 63)),
        ((118, 78, 52), (212, 150, 106), (93, 119, 80)),
        ((72, 48, 44), (187, 124, 87), (143, 103, 65)),
        ((54, 45, 59), (212, 151, 116), (68, 127, 119)),
        ((112, 55, 46), (224, 164, 115), (131, 72, 103))
    ][region]
    ink = (45, 30, 39)
    shade = tuple(max(0, channel - 25) for channel in skin)
    Hairlight = tuple(min(255, channel + 22) for channel in hair)
    Clothlight = tuple(min(255, channel + 25) for channel in coat)
    pg.draw.polygon(sprite, ink, [(5, 4), (7, 2), (15, 2), (18, 4), (20, 7), (20, 13), (18, 15), (17, 17), (20, 18), (21, 21), (18, 22), (16, 21), (16, 24), (12, 24), (11, 23), (10, 24), (6, 24), (6, 21), (4, 22), (1, 21), (2, 18), (5, 17), (4, 15), (2, 13), (2, 7)])
    pg.draw.polygon(sprite, hair, [(6, 4), (8, 3), (15, 3), (18, 5), (19, 8), (19, 13), (16, 14), (5, 14), (3, 13), (3, 8)])
    pg.draw.polygon(sprite, Hairlight, [(6, 6), (9, 4), (14, 4), (17, 6), (17, 8), (13, 7), (10, 8), (6, 9)])
    pg.draw.polygon(sprite, skin, [(5, 12), (8, 12), (8, 10), (12, 10), (12, 11), (16, 11), (17, 13), (18, 13), (18, 15), (16, 16), (15, 18), (7, 18), (6, 16), (4, 15), (4, 13)])
    pg.draw.line(sprite, shade, (7, 16), (15, 16), 1)
    for x in (7, 13):
        pg.draw.rect(sprite, (246, 222, 185), (x, 13, 3, 2))
        pg.draw.rect(sprite, ink, (x+1, 13, 1, 2))
    pg.draw.rect(sprite, shade, (10, 15, 2, 2))
    pg.draw.polygon(sprite, coat, [(7, 17), (9, 18), (13, 18), (15, 17), (17, 20), (15, 22), (7, 22), (5, 20)])
    pg.draw.line(sprite, Clothlight, (8, 19), (14, 19), 1)
    pg.draw.line(sprite, (78, 52, 56), (7, 21), (15, 21), 1)
    pg.draw.rect(sprite, (189, 145, 92), (10, 20, 2, 2))
    for x in (3, 17):
        pg.draw.rect(sprite, skin, (x, 18, 3, 3))
        pg.draw.rect(sprite, shade, (x, 20, 3, 1))
    for x in (7, 12):
        pg.draw.rect(sprite, hair, (x, 22, 3, 1))
    return pg.transform.scale(sprite, (44, 50))


def Floorarea(rects):

    xs = sorted({x for rect in rects for x in (rect.left, rect.right)})
    area = 0
    for left, right in zip(xs, xs[1:]):
        spans = sorted((rect.top, rect.bottom) for rect in rects if rect.left <= left and rect.right >= right)
        end = -1
        for top, bottom in spans:
            area += (right - left) * max(0, bottom - max(top, end))
            end = max(end, bottom)
    return area


class Settlements:

    def __init__(self, Gamemap):

        self.map = Gamemap
        self.houses = [[Townhouse(region, style) for style in range(len(HOUSES))] for region in range(len(VILLAGENAMES))]
        self.buildings = []
        self.Streetprops = []
        self.residents = [Villagersprite(region) for region in range(len(VILLAGENAMES))]
        Basearea = Floorarea([rect for _, _, rect in Gamemap.Roomfloors] + [rect for _, rect in Gamemap.corridors])
        self.side = math.ceil(math.sqrt(Basearea * 9 / 7) / 64) * 64
        self.sites = []
        self.features = []
        self.solids = [[] for _ in VILLAGENAMES]
        self.interiors = []
        self.tiles = []
        for region, base in enumerate(GROUND):
            tile = pg.Surface((160, 160))
            tile.fill(base)
            for i in range(72):
                tx, ty = (i*41)%159, (i*67)%159
                change = (i%5-2)*3
                tone = tuple(max(0, min(255, c+change)) for c in base)
                pg.draw.rect(tile, tone, (tx, ty, 3+i%7, 2+i%3))
            self.tiles.append(tile)
        self.Loottaken = set()
        self.levers = set()
        self.sequence = [0] * 7
        self.solved = set()
        self.Deskseals = set()
        self.Orchardseals = set()
        self.scenery = []
        for region, name in enumerate(VILLAGENAMES):
            x = 25000 + region % 3 * 15000
            y = 1800 + region // 3 * 15500
            grounds = pg.Rect(x, y, self.side, self.side)
            cx, cy = grounds.center
            gate = self.Findgate(GATEROOMS[region])
            self.sites.append((region, name, grounds, gate))
            self.Addroom(name, region, grounds)
            self.features.append((region, "Travel to " + name, gate, "travel", (cx, cy + 570)))
            self.features.append((region, "Return to " + GATEROOMS[region], (cx, cy + 680), "travel", gate))
            self.features.append((region, "Speak to " + RESIDENTS[region], (cx + 125, cy + 170), "npc", None))
            self.features.append((region, "Read the village trail marker", (cx - 124, cy + 170), "sign", None))
            for number, house in enumerate(HOUSES):
                dx, dy = TOWNLOTS[number]
                hx, hy = cx+dx, cy+dy
                Doorx = hx
                self.buildings.append((region, number, hx, hy))
                self.solids[region].append(pg.Rect(hx - 125, hy - 130, 250, 153))
                inside = pg.Rect(x + 180 + 640 * (number % 3), y + self.side + 500 + 550 * (number // 3), 540, 430)
                self.Addroom(name + " " + house, region, inside)
                self.interiors.append((inside, number))
                self.features.append((region, "Enter " + house, (Doorx, hy + 53), "travel", (inside.centerx, inside.bottom - 105)))
                self.features.append((region, "Leave " + house, (inside.centerx, inside.bottom - 35), "travel", (Doorx, hy + 105)))
                if number == 0:
                    self.features.append((region, "Read the keeper's journal", (inside.centerx, inside.top + 110), "journal", None))
                if number == 1:
                    self.features.append((region, "Pull the workshop lever", (inside.centerx, inside.top + 110), "lever", None))
                if number == 2:
                    self.features.append((region, "Search the reading desk", (inside.centerx, inside.top + 110), "desk", None))
                if number >= 3:
                    self.features.append((region, "Search " + house.lower() + " supplies", (inside.centerx, inside.top+110), "landmark", house))
            for title, dx, dy, clue in [
                ("Market trader", -310, 135, "The market hall keeps spare flasks for travellers."),
                ("Innkeeper", 315, 152, "There are beds in the inn, and supplies by the back wall."),
                ("Gardener", -480, 435, "The path markers lead out to an orchard, a cairn, a shelter and a watch post."),
                ("Village guard", 515, 425, "The stone buttons are north of the village. The workshop lever wakes them."),
                ("Weaver", 210, 520, "The loom house keeps supplies for anyone heading back into the dungeon.")
            ]:
                self.features.append((region, "Speak to " + title, (cx+dx, cy+dy), "npc", clue))
            for kind, dx, dy in [
                ("stall", -445, 124), ("stall", -465, 230), ("stall", 433, 130), ("well", 215, 220),
                ("bench", -170, 230), ("bench", 345, 290), ("bench", -343, 320),
                ("garden", -550, 365), ("garden", 565, 360), ("garden", -580, 610), ("garden", 570, 625),
                ("crate", -635, 260), ("crate", 645, 265), ("crate", -910, 555), ("crate", 915, 553),
                ("crate", -540, -175), ("crate", 542, -175),
                ("crate", -625, -168), ("crate", 628, -166), ("bench", -210, -105), ("bench", 209, -105),
                ("garden", -610, -23), ("garden", 607, -21), ("garden", -328, 342), ("garden", 328, 404),
                ("bench", -920, 205), ("bench", 919, 207), ("crate", -900, 310), ("crate", 909, 323),
                ("stall", -440, 511), ("stall", 425, 560), ("crate", -255, 589), ("crate", 273, 653)
            ]:
                px, py=cx+dx, cy+dy
                self.Streetprops.append((region, px, py, kind))
                half = {"stall":40, "well":29, "garden":37, "bench":25, "crate":11}[kind]
                self.solids[region].append(pg.Rect(px-half, py-10, half*2, 23))
            for number, offset in enumerate((-124, 0, 124), 1):
                self.features.append((region, f"Press stone {number}", (cx + offset, cy - 720), "plate", number))
            vault = pg.Rect(x + 2140, y + self.side + 500, 620, 470)
            self.Addroom(name + " Hidden Vault", region, vault)
            self.interiors.append((vault, 3))
            self.features.append((region, "Open the hidden door", (cx, cy - 970), "secret", (vault.centerx, vault.bottom - 105)))
            self.features.append((region, "Leave the vault", (vault.centerx, vault.bottom - 35), "travel", (cx, cy - 905)))
            self.features.append((region, "Open the village cache", (vault.centerx, vault.top + 125), "cache", None))
            for index in range(54):
                row, col = divmod(index, 9)
                tx = cx + (col - 4) * (self.side // 10) + (index * 113) % 140 - 70
                ty = cy + (row - 3) * (self.side // 8) + (index * 157) % 160 - 80
                if abs(tx - cx) > 240 and abs(ty - cy) > 340 and math.hypot(tx - cx, ty - cy) > 750:
                    self.scenery.append((region, tx, ty, index))
                    self.solids[region].append(pg.Rect(tx - 18, ty - 13, 36, 26))
            for label, dx, dy in [("Old orchard", -1, -1), ("Outer cairn", 1, -1), ("Pilgrim shelter", -1, 1), ("Watch post", 1, 1)]:
                point = (cx + dx * self.side // 3, cy + dy * self.side // 3)
                self.features.append((region, "Search " + label.lower(), point, "landmark", label))

    def Addroom(self, name, region, rect):

        self.map.rooms.append((name, region, rect))
        self.map.Roomfloors.append((name, region, rect))

    def Findgate(self, room):

        rect = next(rect for name, _, rect in self.map.rooms if name == room)
        for dx in (0, -220, 220, -420, 420):
            for dy in (280, -280, 420, -420, 0):
                x, y = rect.centerx + dx, rect.centery + dy
                if self.map.Locationname(x, y).endswith(room) and self.map.Canmovecircle(x, y, 42):
                    return x, y
        return rect.center

    def blocks(self, x, y, radius):

        for region, _, grounds, _ in self.sites:
            if grounds.collidepoint(x, y):
                return any(rect.inflate(radius * 2, radius * 2).collidepoint(x, y) for rect in self.solids[region])
        return False

    def nearby(self, player):

        for feature in self.features:
            region, label, point, kind, data = feature
            if kind == "secret" and region not in self.solved:
                continue
            if math.hypot(player.x - point[0], player.y - point[1]) < 72:
                return feature
        return None

    def interact(self, player, inventory):

        feature = self.nearby(player)
        if not feature:
            return None
        region, label, point, kind, data = feature
        order = STONEORDERS[region]
        if kind in ("travel", "secret"):
            if kind == "secret" and region in (1, 4, 6) and region not in self.Deskseals:
                return "A seal-shaped recess blocks the door. Search the reading desk."
            player.x, player.y = data
            player.Dashtime = player.Blocktime = player.Attackanimationtime = 0
            player.Attackstage = 0
            player.Attackqueued = False
            player.Attacktargets.clear()
            player.shots.clear()
            if player.powers:
                player.powers.Leavearea()
            player.Dashtrail.clear()
            return label
        if kind == "npc":
            if data:
                return label[9:] + ": " + data
            clue = (
                "The workshop lever wakes the stones. The cottage journal gives their order.",
                "The stones need the workshop lever and the seal from the reading desk.",
                "Search the old orchard for a gear before trying the workshop lever.",
                "The keeper wrote the stone order in the cottage. The lever is in the workshop.",
                "The vault needs the reading desk seal. Look for the workshop lever too.",
                "The orchard hides a counterweight. Bring it to the workshop lever.",
                "Read the journal, wake the stones, and bring the reading desk seal to the hidden door."
            )[region]
            return RESIDENTS[region] + ": " + clue
        if kind == "sign":
            return "The village road leads north to the stones. Four marked paths lead to old supply caches."
        if kind == "journal":
            return "Keeper's journal. After the lever, press stones " + ", ".join(map(str, order)) + "."
        if kind == "lever":
            if region in (2, 5) and region not in self.Orchardseals:
                return "A piece of the mechanism is missing. Search the old orchard."
            self.levers.add(region)
            return "The stones north of the village stir."
        if kind == "plate":
            if region in self.solved:
                return "The stones are quiet. The hidden door is open."
            if region not in self.levers:
                return "The stone stays dark. A mechanism is missing."
            if data != order[self.sequence[region]]:
                self.sequence[region] = 0
                return "The stones dim. Start the sequence again."
            self.sequence[region] += 1
            if self.sequence[region] == 3:
                self.solved.add(region)
                return "A hidden door opens just north of the stones."
            return "The stone lights up."
        key = (region, kind, data)
        if key in self.Loottaken:
            return "You already searched here."
        self.Loottaken.add(key)
        if kind == "cache":
            loot = LOOTSETS[max(0, region - 1) * 5 + 4]
        elif kind == "desk":
            self.Deskseals.add(region)
            loot = [LOOTSETS[max(0, region - 1) * 5][-1]]
        else:
            if data == "Old orchard":
                self.Orchardseals.add(region)
            if data == "Old orchard":
                loot = [("Crimson Flask", 1)]
            elif data == "Outer cairn":
                loot = [LOOTSETS[max(0, region - 1) * 5 + 1][3]]
            elif data == "Watch post":
                loot = [LOOTSETS[max(0, region - 1) * 5 + 2][2]]
            else:
                loot = [(POTIONS[region][0], 1)]
        for item, count in loot:
            inventory[item] = inventory.get(item, 0) + count
        if kind == "landmark" and data == "Old orchard" and region in (2, 5):
            return "Found the workshop mechanism and a Crimson Flask."
        if kind == "desk" and region in (1, 4, 6):
            return "Found a vault seal and " + loot[0][0] + "."
        return "Collected " + ", ".join(item for item, _ in loot) + "."

    def render(self, screen, camera):

        view = screen.get_rect()
        for region, name, grounds, _ in self.sites:
            x, y = camera.apply(grounds.x, grounds.y)
            bounds = pg.Rect(x, y, grounds.width, grounds.height)
            if not view.colliderect(bounds):
                continue
            visible = bounds.clip(view)
            tile = self.tiles[region]
            clip = screen.get_clip()
            screen.set_clip(visible)
            Firstx = visible.left - (visible.left - bounds.left) % 160
            Firsty = visible.top - (visible.top - bounds.top) % 160
            for tx in range(Firstx, visible.right, 160):
                for ty in range(Firsty, visible.bottom, 160):
                    screen.blit(tile, (tx, ty))
            screen.set_clip(clip)
            cx, cy = camera.apply(*grounds.center)
            road = tuple(max(0, channel - 16) for channel in GROUND[region])
            pg.draw.rect(screen, road, (cx - 60, bounds.y, 120, bounds.height))
            pg.draw.rect(screen, road, (bounds.x, cy - 58, bounds.width, 116))
            paving = tuple(min(255, channel + 11) for channel in road)
            for offset in (-780, -390, 390, 780):
                pg.draw.rect(screen, road, (cx + offset - 29, cy - 110, 58, 920))
                for step in range(20):
                    py = cy - 106 + 44 * step
                    if view.colliderect((cx + offset - 23, py, 46, 30)):
                        pg.draw.rect(screen, paving, (cx + offset - 22 + step%2*4, py, 41, 29), 1)
            for offset in (190, 545):
                pg.draw.rect(screen, road, (cx-880, cy+offset-31, 1760, 62))
            for i in range(160):
                wx = grounds.x + 80 + (i * 431) % (grounds.width - 160)
                wy = grounds.y + 80 + (i * 617) % (grounds.height - 160)
                px, py = camera.apply(wx, wy)
                if view.collidepoint(px, py):
                    pg.draw.rect(screen, road, (px, py, 7, 3))
            for i in range(20):
                px = cx - 550 + i * 55
                py = cy + 22 + (i * 17) % 38
                pg.draw.lines(screen, (109, 100, 88), False, [(px - 9, py), (px - 7, py - 5), (px + 5, py - 6), (px + 9, py)], 2)
            for i in range(12):
                px = cx + (-1 if i % 2 else 1) * (165 + i * 39)
                py = cy + 129 + i % 4 * 27
                pg.draw.lines(screen, (103, 116, 88), False, [(px - 6, py - 6), (px, py), (px + 4, py - 10)], 2)
        for region, wx, wy, kind in self.Streetprops:
            px, py = camera.apply(wx, wy)
            if view.inflate(110, 110).collidepoint(px, py):
                Streetprop(screen, px, py, kind, region)
        for region, style, wx, wy in self.buildings:
            px, py = camera.apply(wx, wy)
            house = self.houses[region][style]
            box = house.get_rect(midbottom=(px, py+26))
            if view.colliderect(box):
                screen.blit(house, box)
                pg.draw.rect(screen, (53, 42, 46), (px-39, py+14, 13, 18))
                pg.draw.rect(screen, (207, 155, 90), (px-36, py+16, 7, 9))
        for interior, kind in self.interiors:
            left, top = camera.apply(interior.x, interior.y)
            room = pg.Rect(left, top, interior.width, interior.height)
            if not view.colliderect(room):
                continue
            pg.draw.rect(screen, (42, 31, 44), room, 18)
            rug = pg.Rect(room.centerx-68, room.centery-36, 136, 165)
            pg.draw.rect(screen, (88, 51, 66), rug)
            pg.draw.rect(screen, (134, 89, 83), rug.inflate(-12, -12), 2)
            for x in (room.left+73, room.right-133):
                pg.draw.rect(screen, (46, 30, 42), (x, room.top+48, 60, 93))
                pg.draw.rect(screen, (109, 67, 61), (x+4, room.top+51, 52, 75))
                for y in range(room.top+62, room.top+123, 18):
                    pg.draw.line(screen, (157, 106, 76), (x+7, y), (x+53, y), 3)
            if kind in (0, 4, 8):
                for x in (room.left + 65, room.right - 125):
                    pg.draw.rect(screen, (63, 40, 50), (x, room.centery+27, 62, 94))
                    pg.draw.rect(screen, (136, 85, 93), (x+4, room.centery+31, 54, 84))
                    pg.draw.rect(screen, (192, 171, 139), (x+8, room.centery+36, 46, 20))
            elif kind in (1, 3, 5, 7):
                for x in (room.left + 75, room.right - 75):
                    Streetprop(screen, x, room.centery+66, "crate", 0)
                    Streetprop(screen, x, room.centery+92, "crate", 0)
            elif kind == 6:
                for x in (room.left+91, room.right-91):
                    Streetprop(screen, x, room.centery+72, "garden", 3)
            for x in (room.left+48, room.right-48):
                pg.draw.circle(screen, (128, 88, 61), (x, room.centery), 11)
                pg.draw.circle(screen, (218, 171, 96), (x, room.centery-3), 5)
        for region, wx, wy, index in self.scenery:
            x, y = camera.apply(wx, wy)
            if not view.inflate(150, 150).collidepoint(x, y):
                continue
            tone = tuple(max(25, c - 22) for c in GROUND[region])
            light = tuple(min(255, c + 19) for c in GROUND[region])
            pg.draw.ellipse(screen, (45, 38, 44), (x - 27, y - 9, 55, 18))
            pg.draw.rect(screen, (83, 61, 52), (x - 6, y - 32, 12, 33))
            for i in range(3):
                px, py = x + (i - 1) * 13, y - 37 - (i % 2) * 17
                pg.draw.polygon(screen, tone, [(px - 19, py + 14), (px - 16, py - 13), (px, py - 25), (px + 18, py - 12), (px + 21, py + 13), (px + 5, py + 22)])
                pg.draw.lines(screen, light, False, [(px - 16, py - 10), (px, py - 22), (px + 13, py - 12)], 3)
        for region, label, point, kind, data in self.features:
            x, y = camera.apply(*point)
            if not view.inflate(44, 44).collidepoint(x, y):
                continue
            if kind == "secret" and region not in self.solved:
                continue
            if kind == "npc":
                pg.draw.ellipse(screen, (42, 33, 42), (x - 15, y - 4, 30, 11))
                if data:
                    sprite = self.residents[(region + sum(map(ord, label))) % len(self.residents)]
                else:
                    sprite = self.residents[region]
                screen.blit(sprite, sprite.get_rect(midbottom=(x, y + 4)))
            elif kind == "plate":
                light = (225, 188, 113) if region in self.solved else (167, 135, 102) if region in self.levers else (91, 75, 78)
                pg.draw.rect(screen, (48, 40, 49), (x - 21, y - 16, 42, 32))
                pg.draw.rect(screen, light, (x - 15, y - 10, 30, 20), 2)
                for mark in range(data):
                    pg.draw.rect(screen, light, (x - 7 + mark * 6, y - 5, 3, 10))
            else:
                if kind in ("travel", "secret"):
                    colour = (185, 143, 94)
                else:
                    colour = (143, 109, 100)
                pg.draw.rect(screen, (47, 37, 49), (x - 14, y - 13, 28, 23))
                pg.draw.rect(screen, colour, (x - 11, y - 10, 22, 14), 2)
