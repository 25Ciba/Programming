import pygame as pg
from DungeonLayout import REGIONS, BOSSROOMS, GATES
from Frost import LAKEX, LAKEY, LAKEWIDTH, LAKEHEIGHT
from RogueArt import DIRECTIONS
from Menus import KEYS, Keyname

INK = (17, 21, 34)
EDGE = (86, 87, 113)
GOLD = (192, 157, 99)
TEXT = (231, 228, 237)
FLOORCOLOURS = [
    (100, 112, 143), (105, 155, 182), (151, 109, 83), (151, 132, 164),
    (161, 131, 90), (86, 143, 148), (169, 149, 99)
]


def panel(screen, rect):

    pg.draw.rect(screen, (9, 12, 21), rect.move(3, 4))
    pg.draw.rect(screen, INK, rect)
    pg.draw.rect(screen, EDGE, rect, 2)
    pg.draw.rect(screen, (40, 43, 63), rect.inflate(-8, -8), 1)
    for x in (rect.left, rect.right - 7):
        for y in (rect.top, rect.bottom - 7):
            pg.draw.rect(screen, GOLD, (x, y, 7, 7))
            pg.draw.rect(screen, INK, (x + 2, y + 2, 3, 3))


def meter(screen, font, rect, name, value, maximum, dark, light):

    label = font.render(name, True, TEXT)
    count = font.render(f"{int(value)}/{maximum}", True, (198, 192, 211))
    screen.blit(label, (rect.x + 9, rect.y - 18))
    screen.blit(count, count.get_rect(topright=(rect.right - 9, rect.y - 18)))
    inner = rect.inflate(-12, -8)
    fill = round(inner.width * max(0, min(1, value / maximum)))
    pg.draw.rect(screen, (41, 39, 58), inner)
    if fill > 0:
        pg.draw.rect(screen, dark, (inner.x, inner.y, fill, inner.height))
        pg.draw.rect(screen, light, (inner.x, inner.y, fill, 3))
        pg.draw.line(screen, (24, 23, 38), (inner.x, inner.bottom - 1), (inner.x + fill - 1, inner.bottom - 1), 2)
    for x in range(inner.x + 12, inner.right, 12):
        pg.draw.line(screen, (28, 27, 44), (x, inner.y + 2), (x, inner.bottom - 1), 1)


def Drawstatus(screen, font, player):

    outer = pg.Rect(14, 14, 514, 78)
    panel(screen, outer)
    crest = pg.Rect(24, 24, 53, 58)
    pg.draw.polygon(screen, (65, 53, 90), [crest.topleft, crest.topright, (crest.right, crest.bottom - 13), (crest.centerx, crest.bottom), (crest.left, crest.bottom - 13)])
    pg.draw.polygon(screen, (154, 125, 183), [crest.topleft, crest.topright, (crest.right, crest.bottom - 13), (crest.centerx, crest.bottom), (crest.left, crest.bottom - 13)], 2)
    initials = "".join(word[0] for word in player.clan.split()[:2])
    mark = font.render(initials, True, (232, 215, 246))
    screen.blit(mark, mark.get_rect(center=(crest.centerx, crest.centery - 3)))
    name = font.render(player.clan.upper(), True, (188, 161, 214))
    screen.blit(name, (89, 22))

    rail = pg.Rect(84, 54, 427, 23)
    pg.draw.rect(screen, (72, 66, 91), rail)
    pg.draw.rect(screen, (29, 28, 44), rail.inflate(-4, -4))
    pg.draw.line(screen, (120, 106, 132), rail.topleft, (rail.right - 1, rail.top), 2)
    health = pg.Rect(rail.x, rail.y, 171, rail.height)
    mana = pg.Rect(health.right, rail.y, 136, rail.height)
    lives = pg.Rect(mana.right, rail.y, rail.right - mana.right, rail.height)
    meter(screen, font, health, "HEALTH", player.Currenthp, player.Maxhp, (149, 44, 64), (233, 113, 127))
    meter(screen, font, mana, "MANA", player.Currentmana, player.Maxmana, (49, 92, 159), (108, 201, 228))
    for x in (health.right, mana.right):
        pg.draw.rect(screen, (159, 128, 91), (x - 1, rail.y + 2, 2, rail.height - 4))
    screen.blit(font.render("LIVES", True, TEXT), (lives.x + 9, lives.y - 18))
    count = font.render(f"{player.Currentlives}/{player.Maxlives}", True, (198, 192, 211))
    screen.blit(count, count.get_rect(topright=(lives.right - 9, lives.y - 18)))
    spacing = min(15, (lives.width - 12) / max(1, player.Maxlives))
    size = max(2, min(6, round(spacing / 2) - 1))
    Startx = lives.centerx - (player.Maxlives - 1) * spacing / 2
    for i in range(player.Maxlives):
        x = round(Startx + i * spacing)
        y = lives.centery
        points = [(x, y - 7), (x + size, y), (x, y + 7), (x - size, y)]
        active = i < player.Currentlives
        pg.draw.polygon(screen, (184, 131, 67) if active else (60, 54, 72), points)
        if active:
            pg.draw.line(screen, (249, 216, 142), (x - size + 1, y - 1), (x, y - 6), 2)


def Maprect(rect, Originx, Originy, scale):

    left = round(Originx + rect.left * scale)
    top = round(Originy + rect.top * scale)
    right = round(Originx + rect.right * scale)
    bottom = round(Originy + rect.bottom * scale)
    return pg.Rect(left, top, max(1, right - left), max(1, bottom - top))


def Paintmap(screen, Gamemap, area, Originx, Originy, scale, local=False):

    clip = screen.get_clip()
    screen.set_clip(area)
    pg.draw.rect(screen, (12, 17, 28), area)
    for x in range(area.left + 12, area.right, 15 if local else 19):
        for y in range(area.top + 12, area.bottom, 15 if local else 19):
            pg.draw.rect(screen, (28, 32, 46), (x, y, 1, 1))
    for region, rect in Gamemap.corridors:
        pg.draw.rect(screen, (77, 79, 100), Maprect(rect, Originx, Originy, scale))
    for name, region, rect in Gamemap.Roomfloors:
        pg.draw.rect(screen, FLOORCOLOURS[region], Maprect(rect, Originx, Originy, scale))
    lake = pg.Rect(LAKEX - LAKEWIDTH // 2, LAKEY - LAKEHEIGHT // 2, LAKEWIDTH, LAKEHEIGHT)
    pg.draw.ellipse(screen, (42, 82, 117), Maprect(lake, Originx, Originy, scale))
    for pool in Gamemap.Harpart.pools:
        pg.draw.ellipse(screen, (37, 82, 101), Maprect(pool, Originx, Originy, scale))
    for rect in Gamemap.Arenaart.partitions:
        pg.draw.rect(screen, (43, 47, 65), Maprect(rect, Originx, Originy, scale))
    for door in Gamemap.Arenaart.doors:
        x = round(Originx + door.x * scale)
        y = round(Originy + door.y * scale)
        pg.draw.rect(screen, GOLD, (x - 2, y - 2, 5, 5))
    if local:
        props = Gamemap.Ruinsart.props + Gamemap.Frostart.props + Gamemap.Guitarart.props + Gamemap.Fluteart.props + Gamemap.Celloart.props + Gamemap.Harpart.props
        for prop in props:
            x = round(Originx + prop.x * scale)
            y = round(Originy + prop.y * scale)
            if area.collidepoint(x, y):
                pg.draw.rect(screen, (64, 61, 77), (x - 2, y - 2, 4, 4))
    else:
        for Regiona, Regionb, x, y in GATES:
            pg.draw.circle(screen, (131, 123, 107), (round(Originx + x * scale), round(Originy + y * scale)), 2)
        for name, region, rect in Gamemap.rooms:
            if name in BOSSROOMS:
                x = round(Originx + rect.centerx * scale)
                y = round(Originy + rect.centery * scale)
                if name == BOSSROOMS[0]:
                    colour = (244, 204, 143)
                else:
                    colour = (225, 163, 185)
                pg.draw.polygon(screen, (37, 35, 55), [(x, y - 7), (x + 7, y), (x, y + 7), (x - 7, y)])
                pg.draw.polygon(screen, colour, [(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)])
    screen.set_clip(clip)


def Drawminimap(screen, font, Gamemap, player):

    rect = pg.Rect(screen.get_width() - 218, 14, 204, 214)
    panel(screen, rect)
    area = pg.Rect(rect.x + 9, rect.y + 25, 186, 178)
    # The minimap reaches twice as far from the Rogue as the clear view.
    scale = area.height / (player.pvisionRadius() * 4)
    Paintmap(screen, Gamemap, area, area.centerx - player.x * scale, area.centery - player.y * scale, scale, local=True)
    pg.draw.rect(screen, EDGE, area, 1)
    center = pg.Vector2(area.center)
    forward = pg.Vector2(DIRECTIONS[player.facing]).normalize()
    side = forward.rotate(90)
    pg.draw.circle(screen, (135, 146, 167), area.center, round(player.pvisionRadius() * scale), 1)
    pg.draw.circle(screen, INK, area.center, 7)
    pg.draw.polygon(screen, (251, 238, 205), [center + forward * 7, center - forward * 4 + side * 4, center - forward * 4 - side * 4])
    screen.blit(font.render("LOCAL MAP", True, TEXT), (rect.x + 10, rect.y + 7))
    hint = font.render(Keyname(KEYS["Map"]), True, GOLD)
    screen.blit(hint, hint.get_rect(topright=(rect.right - 12, rect.top + 7)))


def Drawoverview(screen, Titlefont, font, Gamemap, player, Worldwidth, Worldheight):

    screen.fill((10, 13, 23))
    rect = pg.Rect(0, 0, 886, 724)
    rect.center = screen.get_rect().center
    panel(screen, rect)
    screen.blit(Titlefont.render("MELODY OF THE MIST", True, TEXT), (rect.x + 22, rect.y + 15))
    hint = font.render(f"{Keyname(KEYS['Map'])}   Return to game", True, GOLD)
    screen.blit(hint, hint.get_rect(topright=(rect.right - 22, rect.top + 21)))
    area = pg.Rect(rect.x + 18, rect.y + 52, 650, 650)
    scale = min((area.width - 22) / Worldwidth, (area.height - 22) / Worldheight)
    Originx = area.centerx - Worldwidth * scale / 2
    Originy = area.centery - Worldheight * scale / 2
    Paintmap(screen, Gamemap, area, Originx, Originy, scale)
    pg.draw.rect(screen, EDGE, area, 1)
    x, y = round(Originx + player.x * scale), round(Originy + player.y * scale)
    pg.draw.circle(screen, INK, (x, y), 6)
    pg.draw.circle(screen, (255, 247, 219), (x, y), 4)
    labels = [(name, FLOORCOLOURS[i]) for i, (name, colour) in enumerate(REGIONS)]
    labels += [("You", (255, 247, 219)), ("Boss entrance", GOLD), ("First boss arena", (244, 204, 143)), ("Ultra Boss arena", (225, 163, 185))]
    for i, (label, colour) in enumerate(labels):
        y = rect.y + 76 + i * 29
        if i >= 7:
            y += 19
        pg.draw.rect(screen, colour, (rect.x + 693, y + 3, 9, 9))
        screen.blit(font.render(label, True, TEXT), (rect.x + 710, y))



def Drawaimring(screen, position, direction):

    radius = 61
    guide = pg.Surface((128, 128), pg.SRCALPHA)
    center = pg.Vector2(64, 64)
    tip = center + direction * radius
    pg.draw.circle(guide, (15, 13, 24, 155), center, radius, 3)
    pg.draw.circle(guide, (190, 173, 190, 155), center, radius, 1)
    pg.draw.line(guide, (22, 16, 28, 190), center + direction * 27, tip, 4)
    pg.draw.line(guide, (235, 209, 167, 224), center + direction * 27, tip, 2)
    pg.draw.circle(guide, (235, 209, 167, 235), tip, 3)
    screen.blit(guide, guide.get_rect(center=position))
