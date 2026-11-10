import pygame as pg
from Hud import GOLD, TEXT, Paintmap, panel


class TestMap:

    def __init__(self, Gamemap, enemies, Worldwidth, Worldheight):

        self.Gamemap = Gamemap
        self.area = pg.Rect(58, 94, 640, 640)
        self.scale = min((self.area.width - 20) / Worldwidth, (self.area.height - 20) / Worldheight)
        self.Originx = self.area.centerx - Worldwidth * self.scale / 2
        self.Originy = self.area.centery - Worldheight * self.scale / 2
        self.targets = []
        bosses = []
        added = set()
        for enemy in enemies:
            if enemy.name in added:
                continue
            added.add(enemy.name)
            if enemy.Directionalmob:
                self.targets.append((enemy.name, enemy.home, False))
            else:
                door = next((door for door in Gamemap.Arenaart.doors if door.Bossname == enemy.name), None)
                if door:
                    if door.vertical:
                        x = door.x - 120 * door.inside
                    else:
                        x = door.x
                    if door.vertical:
                        y = door.y
                    else:
                        y = door.y - 120 * door.inside
                    bosses.append((enemy.name, (x, y), True))
        self.targets.extend(bosses)

    def row(self, index):

        return pg.Rect(724, 99 + index * 30, 410, 27)

    def Mappoint(self, x, y):

        return round(self.Originx + x * self.scale), round(self.Originy + y * self.scale)

    def destination(self, point, player):

        for index, (name, position, boss) in enumerate(self.targets):
            if self.row(index).collidepoint(point):
                return self.Safeposition(position, player, 0 if boss else 105)
        if self.area.collidepoint(point):
            x = round((point[0] - self.Originx) / self.scale)
            y = round((point[1] - self.Originy) / self.scale)
            return self.Safeposition((x, y), player)
        return None

    def Safeposition(self, position, player, start=0):

        x, y = position
        for radius in range(start, start + 145, 24):
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)]:
                px, py = round(x + radius * dx), round(y + radius * dy)
                if not self.Gamemap.Canmovecircle(px, py, player.size):
                    continue
                if any(enemy.Currenthp > 0 and enemy.Blocksplayer(px, py, player.size) for enemy in player.enemies):
                    continue
                return px, py
        return None

    def render(self, screen, Titlefont, font, player, mouse):

        screen.fill((10, 13, 23))
        panel(screen, pg.Rect(38, 34, 1124, 730))
        screen.blit(Titlefont.render("ENCOUNTER TEST MAP", True, TEXT), (58, 53))
        hint = font.render("Click the map or choose an encounter  |  F4 or Esc to close", True, GOLD)
        screen.blit(hint, hint.get_rect(topright=(1134, 58)))
        screen.blit(font.render("F8   Test the finale", True, GOLD), (724, 738))
        Paintmap(screen, self.Gamemap, self.area, self.Originx, self.Originy, self.scale)
        for index, (name, (x, y), boss) in enumerate(self.targets):
            row = self.row(index)
            hovered = mouse is not None and row.collidepoint(mouse)
            colour = GOLD if boss else (139, 212, 206)
            pg.draw.rect(screen, (47, 53, 67) if hovered else (26, 32, 46), row)
            pg.draw.rect(screen, colour, (row.x + 9, row.y + 11, 7, 7))
            label = name + ("  /  Entrance" if boss else "")
            screen.blit(font.render(label, True, TEXT), (row.x + 25, row.y + 6))
            pg.draw.circle(screen, colour, self.Mappoint(x, y), 5 if hovered else 3)
        pg.draw.circle(screen, (255, 250, 219), self.Mappoint(player.x, player.y), 5)
