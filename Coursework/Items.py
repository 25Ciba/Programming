import pygame as pg
from functools import lru_cache
from pathlib import Path

CLASSES = ("Mage", "Tank", "Fighter", "Assassin", "Summoner", "Marksman")
REGIONGEAR = [
    ("Ivory", (151, 190, 218), ("Key Rubbing", "Thaw Ledger", "Snow Court Map", "Metronome Spring", "Pianist's Program")),
    ("Copper", (209, 130, 83), ("Workshop Receipt", "Ember Seal", "Tunnel Sketch", "Luthier's Letter", "Broken Fret")),
    ("Reed", (162, 203, 170), ("Vestry Key Tag", "Chime Diagram", "Breath Exercise", "Chapel Ribbon", "Flutist's Margin")),
    ("Rosin", (209, 152, 104), ("Crypt Token", "Bowmaker's Log", "Buried Program", "Gallery Receipt", "Cellist's Letter")),
    ("Tideglass", (114, 198, 186), ("Pump Register", "Tide Rubbing", "Causeway Marker", "Sunken Inventory", "Harpist's Journal")),
    ("Rosewood", (210, 145, 174), ("Tuning Ledger", "Seat Ticket", "Backstage Cue", "Bow Rack Tag", "Final Program"))
]
LORE = [
    ("Snow Court. The first footprints turn at the lake.", "Thaw Passage. Follow the meltwater north to the court.", "Side Chapel. The court has a side passage west of the ice.", "Key Gallery. The tuning crew left their tools east of the court.", "Piano Chamber. The last performer waits behind the ivory door."),
    ("Luthier's Workshop. Follow the carts east out of String Hollow.", "Ember Vault. The warm draft comes from the south passage.", "Low Tunnel. The oldest shafts meet north of String Hollow.", "String Hollow. The luthier left a test guitar by the main route.", "Resonance Arena. A fretblade marks the door west of the hollow."),
    ("Wind Vestry. The ribbons point west when the hall draws breath.", "Open Cloister. Ring the chimes where the paths meet.", "High Chapel. The breath exercise was carved on the northern route.", "Lower Chapel. Spare reeds were kept below the cloister.", "Flute Hall. The eastern curtains move before the first note."),
    ("Side Crypt. The west passage leads to the oldest seats.", "Bow Landing. The spare bow case was left by the northern steps.", "Silt Court. The audience left when sand reached the stage.", "Rosin Gallery. Follow the eastern passage to the old supply ledger.", "Cello Amphitheatre. The broken bowblade lies before the southern door."),
    ("Pump Room. The western keeper wrote the tide down by ear.", "Dark Reservoir. Stay on the dry stones between the pools.", "Raised Causeway. Follow the green lights north of the reservoir.", "Sunken Hall. The eastern shelves held the missing harp strings.", "Harp Chamber. The Tidehook marks the door beyond the pools."),
    ("Tuning Room. A string snapped here every night.", "Lantern Court. The brass inlay leads back to the main aisle.", "East Backstage. Read the stage cue before following the footlights.", "West Backstage. Spare bows still hang off the main passage.", "Performance Hall. The final bow waits past the southern doors.")
]
GEARFORMS = {
    "Armour": ("Vestment", "Cuirass", "Mail", "Mantle", "Coat"),
    "Weapons": ("Focus", "Maul", "Blade", "Knife", "Bow"),
    "Shields": ("Ward", "Tower", "Kite", "Buckler", "Heater"),
    "Talismans": ("Lens", "Seal", "Knot", "Charm", "Pendant")
}
ITEMS = {}
LOOTSETS = []
for region, (prefix, colour, notes) in enumerate(REGIONGEAR):
    for tier, note in enumerate(notes):
        loot = []
        for category, forms in GEARFORMS.items():
            form = forms[tier]
            name = f"{prefix} {form}"
            affinity = CLASSES[tier if tier < 4 else 5]
            if category == "Weapons" and tier == 0 and region % 2:
                affinity = "Summoner"
            if category == "Talismans" and tier == 4:
                affinity = "Summoner"
            power = {"Armour": 2 + region * 2 + tier, "Weapons": (17, 28, 23, 18, 17)[tier] + region * 2, "Shields": 2 + region + tier, "Talismans": 2 + region + tier}[category]
            if name == "Ivory Blade":
                power = 20
            ITEMS[name] = (category, form, colour, power, affinity, LORE[region][tier])
            loot.append((name, 1))
        ITEMS[note] = ("Misc", "Note", colour, 0, "", LORE[region][tier])
        loot.append((note, 1))
        LOOTSETS.append(loot)

POTIONS = [
    ("Crimson Flask", 25, (200, 70, 92)),
    ("Thaw Draught", 18, (131, 186, 223)),
    ("Ember Tonic", 32, (223, 124, 76)),
    ("Reed Elixir", 38, (134, 190, 141)),
    ("Rosin Cordial", 45, (219, 158, 90)),
    ("Tideglass Phial", 55, (100, 188, 184)),
    ("Rosewood Restorative", 70, (201, 112, 163))
]
for name, healing, colour in POTIONS:
    ITEMS[name] = ("Potions", "Flask", colour, healing, "", f"Restores up to {healing} HP.")
for index, loot in enumerate(LOOTSETS):
    if index % 3 == 0:
        loot.append((POTIONS[(index // 3) % len(POTIONS)][0], 2))

STARTWEAPON = "Ivory Blade"
STARTSHIELD = "Ivory Buckler"


def Bestheal(inventory, missing):
    available = [(name, value) for name, value, _ in POTIONS if inventory.get(name, 0) > 0]
    if not available:
        return None
    return min(available, key=lambda item: (item[1] < missing, abs(item[1] - missing)))[0]


def drink(player, inventory, name=None):
    missing = player.Maxhp - player.Currenthp
    if missing <= 0:
        return "HP is already full."
    if player.Currenthp <= 0 or player.Attackstage or player.Dashtime or player.Blocktime:
        return "Wait for your current action to finish."
    name = name or Bestheal(inventory, missing)
    if not name or not inventory.get(name, 0):
        return "No healing potions left."
    gain = min(missing, ITEMS[name][3])
    player.Currenthp += gain
    inventory[name] -= 1
    if inventory[name] == 0:
        del inventory[name]
    return f"{name} restored {gain} HP."


def equip(player, name):
    category, form, colour, power, affinity, lore = ITEMS[name]
    if player.Attackstage or player.Dashtime or player.Blocktime:
        return "Wait for your current action to finish."
    if category == "Weapons":
        player.Mainhand = name
        player.attack = power + (4 if player.clan == "Fighter" else 0)
        player.Attackrange = {"Knife": 78, "Blade": 100, "Maul": 90, "Bow": 370, "Focus": 300}[form]
        if player.clan == "Marksman" and form in ("Bow", "Focus"):
            player.Attackrange += 70
        player.art.Equipweapon(name)
    elif category == "Shields":
        player.Offhand = name
        player.Guardmultiplier = max(.12, .24 - power * .008)
        if player.clan == "Tank":
            player.Guardmultiplier *= .75
    elif category == "Armour":
        player.armour = name
        player.defence = getattr(player, 'Basedefence', 50) + power
    elif category == "Talismans":
        player.charm = name
    else:
        return ""
    return f"Equipped {name}."


ART = Path(__file__).resolve().parent / "Images" / "Items"


@lru_cache(maxsize=200)
def Equipmentart(name):

    category, form, colour, _, _, _ = ITEMS[name]
    if form in ("Blade", "Knife"):
        region = next(index for index, (prefix, _, _) in enumerate(REGIONGEAR) if name.startswith(prefix + " "))
        sprite = pg.image.load(ART / f"{form}{region}.png").convert_alpha()
    else:
        sprite = pg.image.load(ART / f"{form}.png").convert_alpha()
        sprite.fill(tuple(round(115 + channel * .55) for channel in colour), special_flags=pg.BLEND_RGB_MULT)
    return sprite


def Drawhand(surface, hand, direction, name, scale=1):

    if not name:
        return
    category, form, _, _, _, _ = ITEMS[name]
    sprite = Equipmentart(name)
    direction = pg.Vector2(direction).normalize()
    length = {"Knife": 18, "Blade": 28, "Maul": 27, "Bow": 24, "Focus": 27}.get(form, 21 if form == "Buckler" else 28)
    size = max(3, round(length * scale))
    sprite = pg.transform.scale_by(sprite, size / max(sprite.get_size()))
    angle = direction.as_polar()[1]
    if category == "Shields":
        source = 90
    else:
        source = -48
    sprite = pg.transform.rotate(sprite, source - angle)
    grip = pg.Vector2(hand)
    if category == "Weapons" and form != "Bow":
        grip += direction * (size * .42)
    surface.blit(sprite, sprite.get_rect(center=grip))


@lru_cache(maxsize=200)
def Itemicon(name):

    if name not in ITEMS:
        return Fragmenticon(name)
    category, _, colour, _, _, _ = ITEMS[name]
    sprite = Equipmentart(name)
    icon = pg.Surface((44, 44), pg.SRCALPHA)
    sprite = pg.transform.smoothscale_by(sprite, 38 / max(sprite.get_size()))
    icon.blit(sprite, sprite.get_rect(center=(22, 22)))
    if category == "Misc":
        notes = next(names for _, _, names in REGIONGEAR if name in names)
        mark = notes.index(name)
        pg.draw.rect(icon, (74, 43, 53), (29, 29, 8, 7))
        for index in range(mark+1):
            x = 29 + index % 3 * 2
            y = 30 + index // 3 * 2
            pg.draw.rect(icon, colour, (x, y, 2, 2))
    return icon


def Fragmenticon(name):

    icon = pg.Surface((34, 34), pg.SRCALPHA)
    outline = (55, 35, 55)
    gold = (210, 164, 104)
    bright = (241, 214, 162)
    if name == "Primordial Instrument Blueprint":
        pg.draw.rect(icon, outline, (5, 5, 24, 25))
        pg.draw.rect(icon, (86, 115, 151), (7, 7, 20, 21))
        pg.draw.lines(icon, (165, 194, 213), False, [(11, 23), (11, 12), (22, 12), (22, 23), (16, 17), (11, 23)], 1)
        pg.draw.rect(icon, gold, (22, 23, 5, 5))
        return icon
    colours = {"Piano": (151, 190, 218), "Guitar": (209, 130, 83), "Flute": (162, 203, 170), "Cello": (209, 152, 104), "Harp": (114, 198, 186), "Violin": (210, 145, 174)}
    instrument = name.split()[0]
    colour = colours.get(instrument, gold)
    shard = [(8, 24), (12, 10), (21, 4), (27, 11), (23, 22), (16, 29)]
    pg.draw.polygon(icon, outline, shard)
    pg.draw.polygon(icon, colour, [(10, 23), (14, 11), (21, 7), (25, 12), (21, 21), (16, 26)])
    pg.draw.lines(icon, bright, False, [(11, 22), (14, 12), (21, 8)], 2)
    if instrument in ("Piano", "Flute"):
        for x in (14, 17, 20):
            pg.draw.rect(icon, outline, (x, 15, 2, 5))
    else:
        for offset in (-2, 0, 2):
            pg.draw.line(icon, gold, (13 + offset, 23), (21 + offset, 11))
    return icon
