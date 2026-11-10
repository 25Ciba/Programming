import math
from functools import lru_cache
import pygame as pg
from Hud import GOLD, TEXT
from Menus import KEYS, Keyname
from Store import PRICES
from Items import ITEMS, LOOTSETS, Bestheal, Itemicon


CATEGORIES = ("Armour", "Weapons", "Shields", "Potions", "Talismans", "Misc", "Fragment")
ITEMCATEGORIES = {
    "Primordial Instrument Blueprint": "Fragment",
    "Piano Fragment": "Fragment",
    "Guitar Fragment": "Fragment",
    "Flute Fragment": "Fragment",
    "Cello Fragment": "Fragment",
    "Harp Fragment": "Fragment",
    "Violin Fragment": "Fragment"
}


ITEMCATEGORIES.update({name: info[0] for name, info in ITEMS.items()})
VISIBLEITEMS = 6


def Inventoryitems(inventory, category):

    return [(item, count) for item, count in inventory.items() if ITEMCATEGORIES.get(item, "Misc") == CATEGORIES[category]]


def Itemrow(box, index):

    return pg.Rect(box.x + 18, box.y + 128 + index * 48, 358, 42)


def Makechests(screen, Gamemap, player):

    chests = [Chest(screen, 11060, 8650, [("Crimson Flask", 3)])]
    for index, loot in enumerate(LOOTSETS):
        region = index // 5 + 1
        rooms = [(name, rect) for name, number, rect in Gamemap.rooms if number == region]
        name, room = rooms[index % 5]
        offsets = [(180, 120), (-180, 120), (180, -120), (-180, -120), (0, 210), (0, -210), (0, 0)]
        offsets.extend((x, y) for x in range(-room.width // 2 + 100, room.width // 2 - 80, 120) for y in range(-room.height // 2 + 100, room.height // 2 - 80, 120))
        for dx, dy in offsets:
            x, y = room.centerx + dx, room.centery + dy
            if Gamemap.Locationname(x, y).endswith(name) and Gamemap.Canmovecircle(x, y, player.size):
                chests.append(Chest(screen, x, y, loot))
                break
    return chests


class BossDrop:

    def __init__(self, screen, x, y, item):

        self.screen = screen
        self.x, self.y = x, y
        self.item = item
        self.Isopen = False

    def open(self, inventory):

        inventory[self.item] = inventory.get(self.item, 0) + 1
        self.Isopen = True
        return f"Picked up {self.item}."

    def render(self, camera):

        if self.Isopen:
            return
        x, y = camera.apply(self.x, self.y)
        pg.draw.ellipse(self.screen, (40, 28, 48), (x - 12, y - 2, 24, 9))
        points = [(x, y - 16), (x + 8, y - 7), (x, y + 2), (x - 8, y - 7)]
        pg.draw.polygon(self.screen, (228, 178, 114), points)
        pg.draw.lines(self.screen, (105, 61, 77), True, points, 2)


class Chest:

    def __init__(self, screen, x, y, loot):

        self.screen = screen
        self.x, self.y = x, y
        self.loot = loot
        self.Isopen = False

    def open(self, inventory):

        if self.Isopen:
            return "The chest is empty."
        for item, count in self.loot:
            inventory[item] = inventory.get(item, 0) + count
        self.Isopen = True
        return f"Collected {sum(count for _, count in self.loot)} items. Press I to inspect."

    def render(self, camera):

        x, y = camera.apply(self.x, self.y)
        base = pg.Rect(x - 23, y - 16, 46, 25)
        if not self.screen.get_rect().colliderect(base.inflate(0, 40)):
            return
        pg.draw.ellipse(self.screen, (24, 21, 34), (x - 27, y, 54, 14))
        pg.draw.rect(self.screen, (34, 23, 35), base)
        pg.draw.rect(self.screen, (110, 58, 53), base.inflate(-6, -6))
        for side in (-1, 1):
            pg.draw.rect(self.screen, (165, 113, 69), (x + side * 17 - 2, y - 12, 4, 17))
        Lidy = y - 31 if self.Isopen else y - 22
        pg.draw.rect(self.screen, (34, 23, 35), (x - 23, Lidy, 46, 14))
        pg.draw.rect(self.screen, (150, 85, 65), (x - 20, Lidy + 3, 40, 7))
        pg.draw.line(self.screen, (208, 150, 94), (x - 19, Lidy + 3), (x + 19, Lidy + 3), 2)
        if self.Isopen:
            pg.draw.rect(self.screen, (49, 29, 44), (x - 16, y - 17, 32, 8))
        else:
            pg.draw.rect(self.screen, (222, 170, 92), (x - 5, y - 12, 10, 10))
            pg.draw.rect(self.screen, (66, 41, 47), (x - 1, y - 9, 2, 4))


def Nearbychest(chests, player):

    close = [chest for chest in chests if math.hypot(chest.x - player.x, chest.y - player.y) <= 82]
    return min(close, key=lambda chest: math.hypot(chest.x - player.x, chest.y - player.y), default=None)


def Categorytab(box, index):

    return pg.Rect(box.x + 18 + index * 92, box.y + 66, 88, 52)


def Inventorybox(screen):

    box = pg.Rect(0, 0, 676, 478)
    box.center = screen.get_rect().center
    return box


ICONS = [
    ["0110110", "1111111", "1101011", "0101010", "0111110", "0111110", "0111110"],
    ["0000011", "0000111", "0001110", "1011100", "0111000", "1110000", "1000000"],
    ["1111111", "1101011", "1001001", "1001001", "0101010", "0011100", "0001000"],
    ["0011100", "0011100", "0001000", "0011100", "0110110", "0111110", "0011100"],
    ["0011100", "0100010", "0011100", "0110110", "1101011", "0110110", "0011100"],
    ["0111110", "0101011", "0100011", "0111011", "0100011", "0101011", "0111110"],
    ["0001100", "0011100", "0111110", "1101111", "0111110", "0011100", "0010000"]
]
ICONCOLOURS = [(181, 165, 193), (208, 190, 160), (143, 178, 198), (202, 124, 147), (171, 145, 217), (203, 168, 121), (224, 181, 113)]


def Pixelicon(screen, index, center):

    x, y = center
    for row, line in enumerate(ICONS[index]):
        for col, pixel in enumerate(line):
            if pixel == "1":
                pg.draw.rect(screen, ICONCOLOURS[index], (x - 7 + col * 2, y - 7 + row * 2, 2, 2))


@lru_cache(maxsize=4)
def Equipmenttile(size):

    tile = pg.Surface((size, size), pg.SRCALPHA)
    tile.fill((17, 15, 23, 205))
    for y in range(3, size - 3, 2):
        for x in range(3, size - 3, 2):
            value = (x * 13 + y * 19 + x * y * 3) % 11
            tile.fill((23 + value, 20 + value, 27 + value, 205), (x, y, 2, 2))
    pg.draw.rect(tile, (72, 60, 54, 238), tile.get_rect(), 1)
    pg.draw.line(tile, (164, 136, 98, 235), (5, 1), (size - 6, 1))
    pg.draw.line(tile, (109, 86, 69, 230), (5, size - 2), (size - 6, size - 2))
    for x, y, dx, dy in [(2, 2, 1, 1), (size - 3, 2, -1, 1), (2, size - 3, 1, -1), (size - 3, size - 3, -1, -1)]:
        pg.draw.lines(tile, (169, 137, 91, 235), False, [(x + dx * 5, y), (x, y), (x, y + dy * 5)])
    center = size // 2
    for y in (2, size - 3):
        pg.draw.polygon(tile, (179, 148, 103, 235), [(center - 3, y), (center, y - 2), (center + 3, y), (center, y + 2)])
    return tile


def Drawinventory(screen, inventory, category, Selecteditem, player):

    shade = pg.Surface(screen.get_size(), pg.SRCALPHA)
    shade.fill((12, 10, 17, 155))
    screen.blit(shade, (0, 0))
    box = Inventorybox(screen)
    title = pg.font.Font(None, 38)
    Labelfont = pg.font.Font(None, 21)
    body = pg.font.Font(None, 22)
    small = pg.font.Font(None, 18)
    pg.draw.rect(screen, (20, 17, 27), box)
    pg.draw.rect(screen, (100, 77, 67), box, 1)
    pg.draw.rect(screen, (51, 40, 49), box.inflate(-8, -8), 1)
    for x in (box.left + 4, box.right - 11):
        for y in (box.top + 4, box.bottom - 11):
            pg.draw.rect(screen, (166, 130, 87), (x, y, 7, 7), 1)
    screen.blit(title.render("Inventory", True, (223, 199, 155)), (box.x + 20, box.y + 16))
    close = small.render(f"{Keyname(KEYS['Inventory'])} / Esc to close", True, (178, 157, 165))
    screen.blit(close, close.get_rect(topright=(box.right - 23, box.y + 27)))
    pg.draw.line(screen, (86, 67, 65), (box.x + 18, box.y + 55), (box.right - 18, box.y + 55))
    for index, name in enumerate(CATEGORIES):
        tab = Categorytab(box, index)
        selected = index == category
        pg.draw.rect(screen, (54, 41, 51) if selected else (31, 26, 38), tab)
        pg.draw.rect(screen, (133, 103, 78) if selected else (56, 45, 53), tab, 1)
        Pixelicon(screen, index, (tab.centerx, tab.y + 15))
        label = Labelfont.render(name, True, GOLD if selected else TEXT)
        screen.blit(label, label.get_rect(center=(tab.centerx, tab.y + 37)))
        if selected:
            pg.draw.line(screen, (196, 151, 93), (tab.x + 10, tab.bottom - 4), (tab.right - 11, tab.bottom - 4))
    items = Inventoryitems(inventory, category)
    details = pg.Rect(box.x + 391, box.y + 128, 267, 282)
    pg.draw.rect(screen, (28, 23, 34), details)
    pg.draw.rect(screen, (73, 55, 59), details, 1)
    if not items:
        screen.blit(body.render("This category is empty.", True, (181, 156, 174)), (box.x + 24, box.y + 144))
        return
    start = max(0, Selecteditem - VISIBLEITEMS + 1)
    for index, (item, count) in enumerate(items[start:start + VISIBLEITEMS]):
        row = Itemrow(box, index)
        selected = start + index == Selecteditem
        pg.draw.rect(screen, (55, 41, 51) if selected else (30, 25, 36), row)
        pg.draw.rect(screen, (139, 104, 79) if selected else (54, 43, 52), row, 1)
        icon = Itemicon(item)
        icon = pg.transform.smoothscale(icon, (36, 36))
        screen.blit(icon, icon.get_rect(center=(row.x + 22, row.centery)))
        label = Labelfont.render(item, True, TEXT)
        screen.blit(label, label.get_rect(midleft=(row.x + 45, row.centery)))
        equipped = item in (player.Mainhand, player.Offhand, player.armour, player.charm)
        amount = small.render("EQUIPPED" if equipped else f"x{count}", True, (209, 172, 119))
        screen.blit(amount, amount.get_rect(midright=(row.right - 9, row.centery)))
    item = items[Selecteditem][0]
    icon = pg.transform.smoothscale(Itemicon(item), (62, 62))
    tile = Equipmenttile(76)
    slot = tile.get_rect(midtop=(details.centerx, details.top + 12))
    screen.blit(tile, slot)
    screen.blit(icon, icon.get_rect(center=slot.center))
    heading = body.render(item, True, (231, 211, 172))
    screen.blit(heading, heading.get_rect(midtop=(details.centerx, details.y + 98)))
    pg.draw.line(screen, (81, 62, 64), (details.x + 13, details.y + 121), (details.right - 13, details.y + 121))
    info = ITEMS.get(item)
    if info:
        group, form, colour, power, affinity, lore = info
        stat = {"Weapons": f"{power} attack", "Armour": f"+{power} defence", "Shields": f"{power} guard rating", "Talismans": f"+{power} attack", "Potions": f"Up to {power} HP"}.get(group, "Lore")
        if affinity:
            stat += "  /  " + affinity
    else:
        stat = "Primordial collection"
        if item.endswith(" Fragment"):
            lore = "A piece of the instrument described by the Overture Keeper's blueprint."
        else:
            lore = "Plans for a single instrument made from the six Ultra Boss fragments."
    screen.blit(small.render(stat, True, GOLD), (details.x + 13, details.y + 134))
    line = ""
    lines = []
    for word in lore.split():
        joined = f"{line} {word}".strip()
        if small.size(joined)[0] > details.width - 26:
            lines.append(line)
            line = word
        else:
            line = joined
    lines.append(line)
    for index, line in enumerate(lines):
        screen.blit(small.render(line, True, TEXT), (details.x + 13, details.y + 162 + index * 18))
    if item in PRICES:
        _, Buyprice, Sellprice, level = PRICES[item]
        if item in ITEMS:
            label = f"Buy {Buyprice}  /  Sell {Sellprice}  /  Lv {level}"
        else:
            label = "Story reward"
        screen.blit(small.render(label, True, (184, 156, 143)), (details.x+13, details.bottom-26))
    status = small.render(f"{Selecteditem + 1} / {len(items)}", True, (176, 155, 163))
    screen.blit(status, status.get_rect(bottomright=(box.right - 20, box.bottom - 15)))
    Helptext = "Enter  Equip / drink     Up / Down  Select"
    screen.blit(small.render(Helptext, True, (181, 156, 174)), (box.x + 20, box.bottom - 29))


def Drawhandhud(screen, font, player, inventory):

    potion = Bestheal(inventory, max(1, player.Maxhp - player.Currenthp))
    size = 62
    x, y = 19, screen.get_height() - 197
    slots = [(None, 1, 0), (player.Offhand, 0, 1), (player.Mainhand, 2, 1), (potion, 1, 2)]
    for item, column, row in slots:
        rect = pg.Rect(x + column * 64, y + row * 61, size, size)
        tile = pg.Surface(rect.size, pg.SRCALPHA)
        tile.fill((18, 17, 24, 185))
        screen.blit(tile, rect)
        pg.draw.rect(screen, (84, 80, 92), rect, 1)
        if item:
            icon = pg.transform.smoothscale(Itemicon(item), (51, 51))
            screen.blit(icon, icon.get_rect(center=rect.center))
        if row == 2:
            hint = font.render(Keyname(KEYS["Heal"]), True, (226, 197, 149))
            screen.blit(hint, hint.get_rect(bottomleft=(rect.x + 6, rect.bottom - 4)))
            if potion:
                count = font.render(str(inventory[potion]), True, (247, 227, 184))
                screen.blit(count, count.get_rect(bottomright=(rect.right - 6, rect.bottom - 4)))
