import pygame as pg
from Items import ITEMS, POTIONS, REGIONGEAR, Itemicon
from Story import REQUIRED

# Base value, buy price, sell price and the level required to purchase.
PRICES = {}
for name, (Itemtype, form, colour, power, affinity, description) in ITEMS.items():
    region = next((index for index, (prefix, _, notes) in enumerate(REGIONGEAR) if name.startswith(prefix+" ") or name in notes), 0)
    if Itemtype == "Potions":
        rank = next(index for index, (potion, _, _) in enumerate(POTIONS) if potion==name)
        value, unlock = 3 + power//5, 1 + rank
    elif Itemtype == "Misc":
        value, unlock = 5 + region, 1 + region
    else:
        value, unlock = 8 + power + region*3, 1 + region*2
    PRICES[name] = (value, value, max(1, value//3), unlock)
for name in REQUIRED:
    PRICES[name] = (120, 120, 40, 12)


def Experienceneeded(level):

    return 50 + (level-1)*35


def Earnexperience(progress, amount):

    progress.experience += amount
    while progress.experience >= Experienceneeded(progress.level):
        progress.experience -= Experienceneeded(progress.level)
        progress.level += 1


class Store:

    def __init__(self, Storename, Playerinventory, progress, player):

        self.Storename = Storename
        self.Storeinventory = sorted(ITEMS, key=lambda item: (PRICES[item][3], ITEMS[item][0], item))
        self.Playerinventory = Playerinventory
        self.progress = progress
        self.player = player

    def buy(self, item):

        if item not in self.Storeinventory:
            return "This item is reserved for the story."
        _, Buyprice, _, level = PRICES[item]
        if self.progress.level < level:
            return f"Unlocks at level {level}."
        if self.progress.coins < Buyprice:
            return "You need more coins."
        self.progress.coins -= Buyprice
        self.Playerinventory[item] = self.Playerinventory.get(item, 0)+1
        return f"Bought {item} for {Buyprice} coins."

    def sell(self, item):

        if item not in self.Storeinventory:
            return "Story items cannot be sold."
        count = self.Playerinventory.get(item, 0)
        if count <= 0:
            return "You do not own this item."
        equipped = (self.player.Mainhand, self.player.Offhand, self.player.armour, self.player.charm)
        if count == 1 and item in equipped:
            return "Equip something else before selling your last copy."
        _, _, Sellprice, _ = PRICES[item]
        if count == 1:
            del self.Playerinventory[item]
        else:
            self.Playerinventory[item] -= 1
        self.progress.coins += Sellprice
        return f"Sold {item} for {Sellprice} coins."

    def run(self, menus):

        buying = True
        selected = 0
        notice = ""
        tabs = [pg.Rect(140, 218, 140, 38), pg.Rect(292, 218, 140, 38)]
        rows = [pg.Rect(140, 272+i*49, 920, 44) for i in range(8)]
        while not menus.closed:
            if buying:
                items = self.Storeinventory
            else:
                items = sorted(self.Playerinventory)
            selected = max(0, min(selected, len(items)-1))
            start = max(0, selected-len(rows)+1)
            menus.background(self.Storename, f"Level {self.progress.level}  |  XP {self.progress.experience}/{Experienceneeded(self.progress.level)}  |  {self.progress.coins} coins")
            for i, tab in enumerate(tabs):
                pg.draw.rect(menus.screen, (25, 39, 64) if buying==(i==0) else (29, 25, 35), tab)
                pg.draw.rect(menus.screen, (128, 128, 138), tab, 1)
                text=menus.small.render(("Buy", "Sell")[i], True, (231, 217, 202))
                menus.screen.blit(text, text.get_rect(center=tab.center))
            for i, item in enumerate(items[start:start+len(rows)]):
                row=rows[i]
                active=start+i==selected
                pg.draw.rect(menus.screen, (25, 39, 64) if active else (27, 24, 33), row)
                pg.draw.rect(menus.screen, (108, 108, 118), row, 1)
                _, Buyprice, Sellprice, level = PRICES.get(item, (0, 0, 0, 1))
                if item in PRICES:
                    icon=pg.transform.smoothscale(Itemicon(item), (34, 34))
                    menus.screen.blit(icon, (row.x+10, row.y+5))
                count=self.Playerinventory.get(item, 0)
                label=f"{item}  x{count}" if count else item
                price=f"Buy {Buyprice}   /   Sell {Sellprice}"
                if buying and self.progress.level<level:
                    price += f"   /   Level {level}"
                if item in REQUIRED:
                    price="Story reward"
                menus.screen.blit(menus.small.render(label, True, (233, 219, 207)), (row.x+55, row.y+14))
                text=menus.small.render(price, True, (190, 174, 172))
                menus.screen.blit(text, text.get_rect(midright=(row.right-14, row.centery)))
            menus.screen.blit(menus.small.render(notice or "Tab switches buy/sell. Enter trades. Esc leaves.", True, (220, 193, 152)), (140, 688))
            menus.present()
            for event in menus.events():
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_ESCAPE:
                        return
                    if event.key==pg.K_TAB:
                        buying, selected, notice=not buying, 0, ""
                        break
                    if event.key in (pg.K_UP, pg.K_DOWN):
                        selected += 1 if event.key==pg.K_DOWN else -1
                    elif event.key in (pg.K_PAGEUP, pg.K_PAGEDOWN):
                        selected += len(rows) if event.key==pg.K_PAGEDOWN else -len(rows)
                    elif event.key==pg.K_RETURN and items:
                        notice=(self.buy if buying else self.sell)(items[max(0, min(selected, len(items)-1))])
                        break
                if event.type==pg.MOUSEWHEEL:
                    selected-=event.y
                elif event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                    point=menus.point(event.pos)
                    if tabs[0].collidepoint(point) or tabs[1].collidepoint(point):
                        buying, selected, notice=tabs[0].collidepoint(point), 0, ""
                        break
                    for i, row in enumerate(rows[:len(items)-start]):
                        if row.collidepoint(point):
                            selected=start+i
                            break
