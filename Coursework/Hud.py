import pygame as pg
from DungeonLayout import REGIONS, BOSS_ROOMS, GATES
from Frost import LAKE_X, LAKE_Y, LAKE_WIDTH, LAKE_HEIGHT
from RogueArt import DIRECTIONS
from Menus import KEYS, key_name

INK = (17, 21, 34)
EDGE = (86, 87, 113)
GOLD = (192, 157, 99)
TEXT = (231, 228, 237)
FLOOR_COLOURS = [
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


def draw_status(screen, font, player):

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
    meter(screen, font, health, "HEALTH", player.current_hp, player.max_hp, (149, 44, 64), (233, 113, 127))
    meter(screen, font, mana, "MANA", player.current_mana, player.max_mana, (49, 92, 159), (108, 201, 228))
    for x in (health.right, mana.right):
        pg.draw.rect(screen, (159, 128, 91), (x - 1, rail.y + 2, 2, rail.height - 4))
    screen.blit(font.render("LIVES", True, TEXT), (lives.x + 9, lives.y - 18))
    count = font.render(f"{player.current_lives}/{player.max_lives}", True, (198, 192, 211))
    screen.blit(count, count.get_rect(topright=(lives.right - 9, lives.y - 18)))
    spacing = min(15, (lives.width - 12) / max(1, player.max_lives))
    size = max(2, min(6, round(spacing / 2) - 1))
    start_x = lives.centerx - (player.max_lives - 1) * spacing / 2
    for i in range(player.max_lives):
        x = round(start_x + i * spacing)
        y = lives.centery
        points = [(x, y - 7), (x + size, y), (x, y + 7), (x - size, y)]
        active = i < player.current_lives
        pg.draw.polygon(screen, (184, 131, 67) if active else (60, 54, 72), points)
        if active:
            pg.draw.line(screen, (249, 216, 142), (x - size + 1, y - 1), (x, y - 6), 2)


def map_rect(rect, origin_x, origin_y, scale):

    left = round(origin_x + rect.left * scale)
    top = round(origin_y + rect.top * scale)
    right = round(origin_x + rect.right * scale)
    bottom = round(origin_y + rect.bottom * scale)
    return pg.Rect(left, top, max(1, right - left), max(1, bottom - top))


def paint_map(screen, game_map, area, origin_x, origin_y, scale, local=False):

    clip = screen.get_clip()
    screen.set_clip(area)
    pg.draw.rect(screen, (12, 17, 28), area)
    for x in range(area.left + 12, area.right, 15 if local else 19):
        for y in range(area.top + 12, area.bottom, 15 if local else 19):
            pg.draw.rect(screen, (28, 32, 46), (x, y, 1, 1))
    for region, rect in game_map.corridors:
        pg.draw.rect(screen, (77, 79, 100), map_rect(rect, origin_x, origin_y, scale))
    for name, region, rect in game_map.room_floors:
        pg.draw.rect(screen, FLOOR_COLOURS[region], map_rect(rect, origin_x, origin_y, scale))
    lake = pg.Rect(LAKE_X - LAKE_WIDTH // 2, LAKE_Y - LAKE_HEIGHT // 2, LAKE_WIDTH, LAKE_HEIGHT)
    pg.draw.ellipse(screen, (42, 82, 117), map_rect(lake, origin_x, origin_y, scale))
    for pool in game_map.harp_art.pools:
        pg.draw.ellipse(screen, (37, 82, 101), map_rect(pool, origin_x, origin_y, scale))
    for rect in game_map.arena_art.partitions:
        pg.draw.rect(screen, (43, 47, 65), map_rect(rect, origin_x, origin_y, scale))
    for door in game_map.arena_art.doors:
        x = round(origin_x + door.x * scale)
        y = round(origin_y + door.y * scale)
        pg.draw.rect(screen, GOLD, (x - 2, y - 2, 5, 5))
    if local:
        props = game_map.ruins_art.props + game_map.frost_art.props + game_map.guitar_art.props + game_map.flute_art.props + game_map.cello_art.props + game_map.harp_art.props
        for prop in props:
            x = round(origin_x + prop.x * scale)
            y = round(origin_y + prop.y * scale)
            if area.collidepoint(x, y):
                pg.draw.rect(screen, (64, 61, 77), (x - 2, y - 2, 4, 4))
    else:
        for region_a, region_b, x, y in GATES:
            pg.draw.circle(screen, (131, 123, 107), (round(origin_x + x * scale), round(origin_y + y * scale)), 2)
        for name, region, rect in game_map.rooms:
            if name in BOSS_ROOMS:
                x = round(origin_x + rect.centerx * scale)
                y = round(origin_y + rect.centery * scale)
                colour = (244, 204, 143) if name == BOSS_ROOMS[0] else (225, 163, 185)
                pg.draw.polygon(screen, (37, 35, 55), [(x, y - 7), (x + 7, y), (x, y + 7), (x - 7, y)])
                pg.draw.polygon(screen, colour, [(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)])
    screen.set_clip(clip)


def draw_minimap(screen, font, game_map, player):

    rect = pg.Rect(screen.get_width() - 218, 14, 204, 214)
    panel(screen, rect)
    area = pg.Rect(rect.x + 9, rect.y + 25, 186, 178)
    # The minimap reaches twice as far from the Rogue as the clear view.
    scale = area.height / (player.pvisionRadius() * 4)
    paint_map(screen, game_map, area, area.centerx - player.x * scale, area.centery - player.y * scale, scale, local=True)
    pg.draw.rect(screen, EDGE, area, 1)
    center = pg.Vector2(area.center)
    forward = pg.Vector2(DIRECTIONS[player.facing]).normalize()
    side = forward.rotate(90)
    pg.draw.circle(screen, (135, 146, 167), area.center, round(player.pvisionRadius() * scale), 1)
    pg.draw.circle(screen, INK, area.center, 7)
    pg.draw.polygon(screen, (251, 238, 205), [center + forward * 7, center - forward * 4 + side * 4, center - forward * 4 - side * 4])
    screen.blit(font.render("LOCAL MAP", True, TEXT), (rect.x + 10, rect.y + 7))
    hint = font.render(key_name(KEYS["Map"]), True, GOLD)
    screen.blit(hint, hint.get_rect(topright=(rect.right - 12, rect.top + 7)))


def draw_overview(screen, title_font, font, game_map, player, world_width, world_height):

    screen.fill((10, 13, 23))
    rect = pg.Rect(0, 0, 886, 724)
    rect.center = screen.get_rect().center
    panel(screen, rect)
    screen.blit(title_font.render("MELODY OF THE MIST", True, TEXT), (rect.x + 22, rect.y + 15))
    hint = font.render(f"{key_name(KEYS['Map'])}   Return to game", True, GOLD)
    screen.blit(hint, hint.get_rect(topright=(rect.right - 22, rect.top + 21)))
    area = pg.Rect(rect.x + 18, rect.y + 52, 650, 650)
    scale = min((area.width - 22) / world_width, (area.height - 22) / world_height)
    origin_x = area.centerx - world_width * scale / 2
    origin_y = area.centery - world_height * scale / 2
    paint_map(screen, game_map, area, origin_x, origin_y, scale)
    pg.draw.rect(screen, EDGE, area, 1)
    x, y = round(origin_x + player.x * scale), round(origin_y + player.y * scale)
    pg.draw.circle(screen, INK, (x, y), 6)
    pg.draw.circle(screen, (255, 247, 219), (x, y), 4)
    labels = [(name, FLOOR_COLOURS[i]) for i, (name, colour) in enumerate(REGIONS)]
    labels += [("You", (255, 247, 219)), ("Boss entrance", GOLD), ("First boss arena", (244, 204, 143)), ("Ultra Boss arena", (225, 163, 185))]
    for i, (label, colour) in enumerate(labels):
        y = rect.y + 76 + i * 29
        if i >= 7:
            y += 19
        pg.draw.rect(screen, colour, (rect.x + 693, y + 3, 9, 9))
        screen.blit(font.render(label, True, TEXT), (rect.x + 710, y))



def draw_aim_ring(screen, position, direction):

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
