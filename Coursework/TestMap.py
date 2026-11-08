import pygame as pg
from Hud import GOLD, TEXT, paint_map, panel


class TestMap:

    def __init__(self, game_map, enemies, world_width, world_height):

        self.game_map = game_map
        self.area = pg.Rect(58, 94, 640, 640)
        self.scale = min((self.area.width - 20) / world_width, (self.area.height - 20) / world_height)
        self.origin_x = self.area.centerx - world_width * self.scale / 2
        self.origin_y = self.area.centery - world_height * self.scale / 2
        self.targets = []
        bosses = []
        added = set()
        for enemy in enemies:
            if enemy.name in added:
                continue
            added.add(enemy.name)
            if enemy.directional_mob:
                self.targets.append((enemy.name, enemy.home, False))
            else:
                door = next((door for door in game_map.arena_art.doors if door.boss_name == enemy.name), None)
                if door:
                    x = door.x - 120 * door.inside if door.vertical else door.x
                    y = door.y if door.vertical else door.y - 120 * door.inside
                    bosses.append((enemy.name, (x, y), True))
        self.targets.extend(bosses)

    def row(self, index):

        return pg.Rect(724, 99 + index * 30, 410, 27)

    def map_point(self, x, y):

        return round(self.origin_x + x * self.scale), round(self.origin_y + y * self.scale)

    def destination(self, point, player):

        for index, (name, position, boss) in enumerate(self.targets):
            if self.row(index).collidepoint(point):
                return self.safe_position(position, player, 0 if boss else 105)
        if self.area.collidepoint(point):
            x = round((point[0] - self.origin_x) / self.scale)
            y = round((point[1] - self.origin_y) / self.scale)
            return self.safe_position((x, y), player)
        return None

    def safe_position(self, position, player, start=0):

        x, y = position
        for radius in range(start, start + 145, 24):
            for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)]:
                px, py = round(x + radius * dx), round(y + radius * dy)
                if not self.game_map.can_move_circle(px, py, player.size):
                    continue
                if any(enemy.current_hp > 0 and enemy.blocks_player(px, py, player.size) for enemy in player.enemies):
                    continue
                return px, py
        return None

    def render(self, screen, title_font, font, player, mouse):

        screen.fill((10, 13, 23))
        panel(screen, pg.Rect(38, 34, 1124, 730))
        screen.blit(title_font.render("ENCOUNTER TEST MAP", True, TEXT), (58, 53))
        hint = font.render("Click the map or choose an encounter  |  F4 or Esc to close", True, GOLD)
        screen.blit(hint, hint.get_rect(topright=(1134, 58)))
        screen.blit(font.render("F8   Test the finale", True, GOLD), (724, 738))
        paint_map(screen, self.game_map, self.area, self.origin_x, self.origin_y, self.scale)
        for index, (name, (x, y), boss) in enumerate(self.targets):
            row = self.row(index)
            hovered = mouse is not None and row.collidepoint(mouse)
            colour = GOLD if boss else (139, 212, 206)
            pg.draw.rect(screen, (47, 53, 67) if hovered else (26, 32, 46), row)
            pg.draw.rect(screen, colour, (row.x + 9, row.y + 11, 7, 7))
            label = name + ("  /  Entrance" if boss else "")
            screen.blit(font.render(label, True, TEXT), (row.x + 25, row.y + 6))
            pg.draw.circle(screen, colour, self.map_point(x, y), 5 if hovered else 3)
        pg.draw.circle(screen, (255, 250, 219), self.map_point(player.x, player.y), 5)
