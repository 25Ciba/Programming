import pygame as pg
from TestMap import TestMap
from Loot import BossDrop, CATEGORIES, VISIBLEITEMS, Categorytab, Drawhandhud, Drawinventory, Inventorybox, Inventoryitems, Itemrow, Makechests, Nearbychest
from Items import ITEMS, drink, equip
from Menus import Menus, KEYS, Keyname, Loadsettings, matches
from Saves import RunStats, slots, Slotlabels, Saverun, Restorerun
from Store import Store, Earnexperience, Experienceneeded
from Scoreboard import Drawscoreboard, Recordscore, Showscoreboard
from Clans import SKILLS, Chooseclass, Configureclass
from Story import TUTORIALSTART, Playprologue
from DungeonLayout import STARTX, STARTY
from Hud import GOLD, Drawstatus, Drawminimap, Drawoverview, Drawaimring
from Classes import Player, EnemyManager, Camera, Map, MAPWIDTH, MAPHEIGHT

###

# Start Pygame
pg.display.init()
pg.font.init()
WIDTH = 1200
HEIGHT = 800
Desktopwidth, Desktopheight = pg.display.get_desktop_sizes()[0]
Windowscale = min(1, (Desktopwidth - 80) / WIDTH, (Desktopheight - 150) / HEIGHT)
Windowsize = (round(WIDTH * Windowscale), round(HEIGHT * Windowscale))
display = pg.display.set_mode(Windowsize, pg.RESIZABLE)
screen = pg.Surface((WIDTH, HEIGHT)).convert()
Displayframe = display.get_rect()
scale = min(Displayframe.width / WIDTH, Displayframe.height / HEIGHT)
Displayframe.size = (round(WIDTH * scale), round(HEIGHT * scale))
Displayframe.center = display.get_rect().center
pg.display.set_caption("Melody of the Mist")

###

def Playrun(display, screen, Displayframe, profile, saved=None):

    fullscreen = False
    Windowsize = display.get_size()
    clock = pg.time.Clock()
    running = True
    Showmap = Showtestmap = Showinventory = Showcoordinates = False
    Bossprompt = None
    font = pg.font.Font(None, 28)
    Smallfont = pg.font.Font(None, 22)
    
    ###

    # Create the game objects
    Gamemap = Map()
    player = Player(screen)
    player.character = profile.get("character", "Male")
    player.fragment = profile.get("fragment", "Piano")
    inventory = Configureclass(player, profile["class"])
    starter = profile.get("starter")
    if starter:
        inventory[starter] = 1
        equip(player, starter)
    if profile.get("tutorial", True):
        player.x, player.y = TUTORIALSTART
    else:
        player.x, player.y = (STARTX, STARTY)
    Selecteditem = 0
    Inventorycategory = CATEGORIES.index("Misc")
    Bossdrops = []
    Rewardedbosses = set()
    chests = Makechests(screen, Gamemap, player)
    Enemymanager = EnemyManager(screen, player, Gamemap)
    camera = Camera(screen, MAPWIDTH, MAPHEIGHT)
    Testmap = TestMap(Gamemap, Enemymanager.enemies, 23040, 23040)
    stats = RunStats()
    player.progress = stats
    Endingrecord = None
    if saved:
        Restorerun(saved, screen, player, inventory, Gamemap, Enemymanager, chests, Bossdrops, Rewardedbosses, stats)
    camera.update(player)
    menus = Menus(display, screen, Displayframe)
    leave = False
    message = "Progress loaded." if saved else ("Traveller's Passage. Follow the path north to leave." if profile.get("tutorial", True) else f"Lantern Shelter. You attuned to {player.fragment}.")
    Messagetimer = 6.0

    ###

    # Make the fog of war surface
    vision = player.pvisionRadius()
    Fogradius = vision + 150
    mist = pg.Surface((Fogradius * 2, Fogradius * 2), pg.SRCALPHA)
    mist.fill((11, 14, 24, 240))
    for radius in range(Fogradius, vision - 1, -1):
        fade = (radius - vision) / (Fogradius - vision)
        pg.draw.circle(mist, (11, 14, 24, int(240 * fade)), (Fogradius, Fogradius), radius)
    Fogsurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

    ###

    def Pickposition(Mouseposition, frame, camera):

        if not frame.collidepoint(Mouseposition):
            return None
        x = round((Mouseposition[0] - frame.x) * WIDTH / frame.width)
        y = round((Mouseposition[1] - frame.y) * HEIGHT / frame.height)
        return x, y, round(x + camera.offset.x), round(y + camera.offset.y)

    ###

    def Collectdefeats():

        for enemy in Enemymanager.enemies:
            if enemy.Currenthp <= 0 and not enemy.Rewardclaimed:
                enemy.Rewardclaimed = True
                coins, experience = {
                    "Common":(3, 10), "Strong":(6, 18), "Elite":(9, 28),
                    "Boss":(14, 48), "Overture":(25, 90)
                }.get(enemy.Enemytype, (42, 160))
                stats.coins += coins
                stats.Enemiesfelled += 1
                stats.score += experience
                Earnexperience(stats, experience)
            if enemy.Currenthp > 0 or enemy.name in Rewardedbosses:
                continue
            if enemy.Enemytype == "Overture":
                item = "Primordial Instrument Blueprint"
            elif enemy.name.endswith(" Ultra Boss"):
                item = enemy.instrument + " Fragment"
            else:
                continue
            Bossdrops.append(BossDrop(screen, enemy.x, enemy.y, item))
            Rewardedbosses.add(enemy.name)
            stats.Areascleared = len(Rewardedbosses)

###

    # Main game loop
    while running:
        elapsed = clock.tick(60) / 1000
        dt = min(elapsed, 0.05)

        # Read the keyboard and mouse
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE and not fullscreen:
                Windowsize = event.size
                scale = min(event.w / WIDTH, event.h / HEIGHT)
                Displayframe.size = (round(WIDTH * scale), round(HEIGHT * scale))
                Displayframe.center = display.get_rect().center
            elif Gamemap.story.ending is not None:
                continue
            elif event.type == pg.KEYDOWN:
                if Bossprompt:
                    if event.key in (pg.K_RETURN, pg.K_y):
                        Bossprompt.allowed = True
                        Bossprompt = None
                    elif event.key in (pg.K_ESCAPE, pg.K_n):
                        Bossprompt = None
                    continue
                if Showinventory:
                    if matches(event, "Inventory") or event.key == pg.K_ESCAPE:
                        Showinventory = False
                    elif event.key in (pg.K_LEFT, pg.K_RIGHT):
                        Inventorycategory = (Inventorycategory + (1 if event.key == pg.K_RIGHT else -1)) % len(CATEGORIES)
                        Selecteditem = 0
                    elif event.key in (pg.K_UP, pg.K_DOWN, pg.K_RETURN):
                        items = Inventoryitems(inventory, Inventorycategory)
                        if items and event.key == pg.K_RETURN:
                            item = items[Selecteditem][0]
                            if item in ITEMS:
                                if ITEMS[item][0] == "Potions":
                                    message = drink(player, inventory, item)
                                else:
                                    message = equip(player, item)
                                Messagetimer = 3.0 if message else 0
                                Selecteditem = min(Selecteditem, max(0, len(Inventoryitems(inventory, Inventorycategory)) - 1))
                        elif items:
                            Selecteditem = (Selecteditem + (1 if event.key == pg.K_DOWN else -1)) % len(items)
                    continue
                Skillindex = None
                for index in range(4):
                    if matches(event, f"Skill {index + 1}"):
                        Skillindex = index
                        break

                if matches(event, "Inventory") and not Showtestmap and not Showcoordinates:
                    Showmap = False
                    Showinventory = True
                elif event.key == pg.K_F4:
                    Showtestmap = not Showtestmap
                    Showmap = False
                    Showcoordinates = False
                elif Showtestmap:
                    if event.key == pg.K_F8:
                        Gamemap.story.Testingfinale = True
                        Gamemap.story.move(player, (9950, 30780))
                        camera.update(player)
                        Showtestmap = False
                        message = "Finale test. Follow the stairs and press E at the altar."
                        Messagetimer = 5
                    elif event.key == pg.K_ESCAPE:
                        Showtestmap = False
                    continue
                elif event.key == pg.K_ESCAPE:
                    menus.display = display
                    option = menus.choose("Paused", ["Resume", "Save and Return", "General Settings", "Return to Main Menu"], f"{stats.coins} coins   |   Score {stats.score}")
                    if option == 1:
                        saves = slots()
                        slot = menus.choose("Save Game", Slotlabels(saves), "Choose a slot.")
                        if slot is not None:
                            if not saves[slot] or menus.choose("Overwrite save?", ["Keep existing save", "Overwrite this slot"]) == 1:
                                Collectdefeats()
                                Saverun(slot, player, inventory, Gamemap, Enemymanager, chests, Bossdrops, Rewardedbosses, stats)
                                leave = True
                                running = False
                    elif option == 2:
                        menus.settings()
                    elif option == 3:
                        leave = True
                        running = False
                    if menus.closed:
                        running = False
                    clock.tick()
                elif event.key == pg.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                    else:
                        display = pg.display.set_mode(Windowsize, pg.RESIZABLE)
                    scale = min(display.get_width() / WIDTH, display.get_height() / HEIGHT)
                    Displayframe.size = (round(WIDTH * scale), round(HEIGHT * scale))
                    Displayframe.center = display.get_rect().center
                elif event.key == pg.K_F3:
                    Showcoordinates = not Showcoordinates
                    Showmap = False
                elif matches(event, "Map"):
                    Showcoordinates = False
                    Showmap = not Showmap
                elif Skillindex is not None and not Showmap and not Showcoordinates:
                    point = Pickposition(pg.mouse.get_pos(), Displayframe, camera)
                    if point:
                        cursor = point[2:]
                    else:
                        cursor = (player.x, player.y + 120)
                    message = player.powers.cast(Skillindex, cursor, Gamemap)
                    Messagetimer = 2.0
                elif matches(event, "Heal") and not Showmap and not Showcoordinates:
                    message = drink(player, inventory)
                    Messagetimer = 3.0
                elif matches(event, "Interact") and not Showmap and not Showcoordinates:
                    Storymessage = Gamemap.story.interact(player, inventory, (STARTX, STARTY))
                    if Storymessage:
                        message = Storymessage
                        Messagetimer = 6.0
                        camera.update(player)
                        continue
                    Previouscount = sum(inventory.values())
                    Settlementmessage = Gamemap.settlements.interact(player, inventory)
                    if Settlementmessage:
                        stats.Itemscollected += max(0, sum(inventory.values())-Previouscount)
                        message = Settlementmessage
                        Messagetimer = 6.0
                        camera.update(player)
                        continue
                    action = Gamemap.Arenaart.Nearbyaction(player)
                    if action:
                        door, confirm = action
                        if confirm:
                            Bossprompt = door
                        else:
                            message = door.inscription
                            Messagetimer = 6.0
                        continue
                    drop = Nearbychest(Bossdrops, player)
                    if drop:
                        message = drop.open(inventory)
                        Bossdrops.remove(drop)
                        stats.Itemscollected += 1
                        Messagetimer = 4.0
                        continue
                    chest = Nearbychest(chests, player)
                    if chest:
                        Previouscount = sum(inventory.values())
                        message = chest.open(inventory)
                        stats.Itemscollected += max(0, sum(inventory.values())-Previouscount)
                        Messagetimer = 3.0
                        continue
                    readable = Gamemap.Ruinsart.interact(player) or Gamemap.Frostart.interact(player) or Gamemap.Guitarart.interact(player) or Gamemap.Fluteart.interact(player) or Gamemap.Celloart.interact(player) or Gamemap.Harpart.interact(player) or Gamemap.Violinart.interact(player)
                    if readable:
                        message = readable[1]
                        Messagetimer = 6.0
                elif matches(event, "Market") and not Showmap and not Showcoordinates:
                    trader = Gamemap.settlements.nearby(player)
                    if trader and trader[1] == "Speak to Market trader":
                        menus.display = display
                        Store("Village Market", inventory, stats, player).run(menus)
                        clock.tick()
                    else:
                        message = "Visit a village market trader."
                    if menus.closed:
                        running = False
                    Messagetimer = 3.0
                elif matches(event, "Attack") and not Showmap and not Showcoordinates:
                    point = Pickposition(pg.mouse.get_pos(), Displayframe, camera)
                    player.Attackenemies(Enemymanager.enemies, Gamemap, point[2:] if point else None)
                    Gamemap.story.practice(player)
                elif matches(event, "Defend") and not Showmap and not Showcoordinates:
                    if player.Beginblock():
                        message = "Block!"
                        Messagetimer = .6
                elif matches(event, "Dash") and not Showmap and not Showcoordinates:
                    if player.Begindash():
                        message = "Dash!"
                        Messagetimer = 0.6
            elif event.type == pg.MOUSEBUTTONDOWN and Showinventory:
                point = Pickposition(event.pos, Displayframe, camera)
                if event.button == 1 and point:
                    for index in range(len(CATEGORIES)):
                        if Categorytab(Inventorybox(screen), index).collidepoint(point[:2]):
                            Inventorycategory = index
                            Selecteditem = 0
                            break
                    else:
                        items = Inventoryitems(inventory, Inventorycategory)
                        start = max(0, Selecteditem - VISIBLEITEMS + 1)
                        for index in range(min(VISIBLEITEMS, len(items) - start)):
                            if Itemrow(Inventorybox(screen), index).collidepoint(point[:2]):
                                Selecteditem = start + index
                                break
            elif event.type == pg.MOUSEWHEEL and Showinventory:
                items = Inventoryitems(inventory, Inventorycategory)
                Selecteditem = max(0, min(len(items) - 1, Selecteditem - event.y))
            elif event.type == pg.MOUSEBUTTONDOWN and Showtestmap:
                point = Pickposition(event.pos, Displayframe, camera)
                if event.button == 1 and point:
                    destination = Testmap.destination(point[:2], player)
                    if destination:
                        player.x, player.y = destination
                        player.Dashtime = player.Blocktime = player.Attackanimationtime = 0
                        player.Dashtrail.clear()
                        player.shots.clear()
                        player.powers.Leavearea()
                        player.Attackstage = 0
                        player.Attacktargets.clear()
                        player.Attackqueued = False
                        camera.update(player)
                        Showtestmap = False
            elif event.type == pg.MOUSEBUTTONDOWN and Showcoordinates:
                if event.button == 1:
                    point = Pickposition(event.pos, Displayframe, camera)
                    if point:
                        x, y, Worldx, Worldy = point
                        print(f"({Worldx}, {Worldy})  {Gamemap.Locationname(Worldx, Worldy)}", flush=True)
            elif event.type == pg.MOUSEBUTTONDOWN and not Showmap and not Bossprompt:
                if matches(event, "Attack"):
                    point = Pickposition(event.pos, Displayframe, camera)
                    if point:
                        player.Attackenemies(Enemymanager.enemies, Gamemap, point[2:])
                        Gamemap.story.practice(player)
                elif matches(event, "Defend"):
                    if player.Beginblock():
                        message = "Block!"
                        Messagetimer = 0.6

        if not running:
            break

        # Update the game objects
        if Gamemap.story.ending is None and not Showmap and not Showtestmap and not Showcoordinates and not Showinventory and not Bossprompt:
            stats.Timesurvived += dt
            player.update(dt)
            Gamemap.story.update(dt)
            Gamemap.gate.update(dt, player)
            Gamemap.Arenaart.update(dt, player, Enemymanager.enemies)
            player.keybinds(dt, Gamemap)
            Collectdefeats()
            Enemymanager.update(dt)
            camera.update(player)

        if player.Currentlives <= 0:
            leave = True
            running = False
        if Messagetimer > 0:
            Messagetimer -= dt

        # Draw the map and game objects
        screen.fill((10, 13, 21))
        Gamemap.render(screen, camera)
        Gamemap.Frostart.Renderlake(screen, camera, player)
        player.powers.render(screen, camera)
        actors = Gamemap.Ruinsart.props + Gamemap.Frostart.props + Gamemap.Guitarart.props + Gamemap.Fluteart.props + Gamemap.Celloart.props + Gamemap.Harpart.props + Gamemap.Violinart.props + Gamemap.Arenaart.relics + chests + Bossdrops + Enemymanager.enemies + [player]
        actors.sort(key=lambda actor: actor.y)
        for actor in actors:
            if actor in Enemymanager.enemies:
                Enemymanager.Renderenemy(actor, camera)
            else:
                actor.render(camera)

        if Gamemap.story.ending is not None:
            running = Gamemap.story.finish(screen, camera, player, elapsed) and running
            if Gamemap.story.ending >= 11.5:
                if Endingrecord is None:
                    Endingrecord = Recordscore(stats.score)
                Drawscoreboard(screen, stats, *Endingrecord, top=340)
            display.fill((0, 0, 0))
            display.blit(pg.transform.scale(screen, Displayframe.size), Displayframe)
            pg.display.flip()
            continue

        # Draw fog of war
        Fogsurface.fill((11, 14, 24, 240))
        Playerscreenpos = camera.apply(player.x, player.y)
        Mistrect = mist.get_rect(center=Playerscreenpos)
        Fogsurface.blit(mist, Mistrect, special_flags=pg.BLEND_RGBA_MIN)
        Gamemap.Arenaart.Revealfog(Fogsurface, camera, Gamemap.Roomfloors)
        Gamemap.Arenaart.Hidebeyonddoors(Fogsurface, camera, player)
        screen.blit(Fogsurface, (0, 0))

        if player.Usesrangedweapon() and not (Showinventory or Showmap or Showtestmap or Showcoordinates or Bossprompt):
            point = Pickposition(pg.mouse.get_pos(), Displayframe, camera)
            if point:
                for enemy in Enemymanager.enemies:
                    if enemy.Currenthp <= 0:
                        continue
                    Distancex = enemy.x - player.x
                    Distancey = enemy.y - player.y
                    if Distancex ** 2 + Distancey ** 2 <= vision ** 2:
                        Drawaimring(screen, Playerscreenpos, player.Aimdirection(point[2:]))
                        break

        # Draw health, equipment and skill information
        Drawstatus(screen, Smallfont, player)
        counters = Smallfont.render(f"Level {stats.level}   /   XP {stats.experience}/{Experienceneeded(stats.level)}   /   {stats.coins} coins", True, GOLD)
        screen.blit(counters, (20, 102))
        Drawhandhud(screen, Smallfont, player, inventory)
        for index, (name, _, _) in enumerate(SKILLS[player.clan]):
            slot = pg.Rect(WIDTH - 410 + index * 98, HEIGHT - 67, 94, 42)
            pg.draw.rect(screen, (23, 20, 34), slot)
            pg.draw.rect(screen, (80, 72, 92), slot, 1)
            remaining = player.powers.cooldowns[index]
            key = Keyname(KEYS[f"Skill {index + 1}"])
            if remaining:
                caption = f"{key}   {round(remaining, 1)}s"
            else:
                caption = f"{key}   Ready"
            if name == "Summon" and player.powers.familiar is not None:
                caption = f"{key}   Dismiss"
            screen.blit(Smallfont.render(caption, True, GOLD), (slot.x + 5, slot.y + 4))
            screen.blit(pg.font.Font(None, 17).render(name, True, (221, 210, 218)), (slot.x + 5, slot.y + 23))
        Drawminimap(screen, Smallfont, Gamemap, player)

        readable = Gamemap.Ruinsart.Nearbyreadable(player) or Gamemap.Frostart.Nearbyreadable(player) or Gamemap.Guitarart.Nearbyreadable(player) or Gamemap.Fluteart.Nearbyreadable(player) or Gamemap.Celloart.Nearbyreadable(player) or Gamemap.Harpart.Nearbyreadable(player) or Gamemap.Violinart.Nearbyreadable(player)
        chest = Nearbychest(chests, player)
        drop = Nearbychest(Bossdrops, player)
        feature = Gamemap.settlements.nearby(player)
        Storytarget = Gamemap.story.target(player)
        if Messagetimer <= 0 and Storytarget:
            hint = Smallfont.render(f"{Keyname(KEYS['Interact'])}   {Storytarget[0]}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif Messagetimer <= 0 and feature:
            hint = Smallfont.render(f"{Keyname(KEYS['Interact'])}   {feature[1]}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif Messagetimer <= 0 and drop:
            hint = Smallfont.render(f"{Keyname(KEYS['Interact'])}   Pick up {drop.item}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif Messagetimer <= 0 and chest and not chest.Isopen:
            hint = Smallfont.render(f"{Keyname(KEYS['Interact'])}   Open chest", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif Messagetimer <= 0 and readable:
            prompt = Smallfont.render(f"{Keyname(KEYS['Interact'])}   {readable[0]}", True, (241, 213, 157))
            screen.blit(prompt, prompt.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))

        if Messagetimer > 0:
            Messagetext = Smallfont.render(message, True, (235, 242, 250))
            Messagebox = Messagetext.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)).inflate(24, 14)
            pg.draw.rect(screen, (20, 24, 34), Messagebox)
            screen.blit(Messagetext, Messagetext.get_rect(center=Messagebox.center))

        if Showmap:
            Drawoverview(screen, font, Smallfont, Gamemap, player, MAPWIDTH, MAPHEIGHT)

        # Show the finished frame
        if Bossprompt:
            panel = pg.Rect(0, 0, 710, 150)
            panel.center = (WIDTH // 2, HEIGHT // 2)
            pg.draw.rect(screen, (17, 21, 33), panel)
            pg.draw.rect(screen, Bossprompt.metal, panel, 2)
            title = font.render(f"Challenge {Bossprompt.Bossname}?", True, (244, 234, 221))
            line = Smallfont.render(Bossprompt.challenge, True, (218, 222, 235))
            controls = Smallfont.render("Enter / Y   Open the door       Esc / N   Step away", True, Bossprompt.metal)
            screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.y + 20)))
            screen.blit(line, line.get_rect(midtop=(panel.centerx, panel.y + 60)))
            screen.blit(controls, controls.get_rect(midtop=(panel.centerx, panel.y + 108)))
        elif not Showmap and not Showcoordinates and Messagetimer <= 0:
            action = Gamemap.Arenaart.Nearbyaction(player)
            if action:
                door, confirm = action
                if confirm:
                    label = "E   Approach the sealed door"
                else:
                    label = "E   Read the traveller's note"
                hint = Smallfont.render(label, True, (248, 229, 188))
                box = hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 22))
                pg.draw.rect(screen, (20, 24, 34), box.inflate(14, 8))
                screen.blit(hint, box)

        if Showcoordinates:
            point = Pickposition(pg.mouse.get_pos(), Displayframe, camera)
            text = "F3: resume  |  Left click to print the position in the terminal"
            if point:
                x, y, Worldx, Worldy = point
                if Gamemap.Canmovecircle(Worldx, Worldy, player.size):
                    colour = (122, 230, 191)
                else:
                    colour = (241, 125, 109)
                pg.draw.line(screen, colour, (x - 11, y), (x + 11, y), 2)
                pg.draw.line(screen, colour, (x, y - 11), (x, y + 11), 2)
                text = f"({Worldx}, {Worldy})  |  {Gamemap.Locationname(Worldx, Worldy)}  |  Click to print  |  F3 to resume"
            label = Smallfont.render(text, True, (234, 241, 246))
            box = label.get_rect(midtop=(WIDTH // 2, 15))
            pg.draw.rect(screen, (20, 24, 34), box.inflate(18, 10))
            screen.blit(label, box)

        if Showtestmap:
            point = Pickposition(pg.mouse.get_pos(), Displayframe, camera)
            Testmap.render(screen, font, Smallfont, player, point[:2] if point else None)

        if Showinventory:
            Drawinventory(screen, inventory, Inventorycategory, Selecteditem, player)

        display.fill((0, 0, 0))
        display.blit(pg.transform.scale(screen, Displayframe.size), Displayframe)
        pg.display.flip()

    if leave:
        menus.display = pg.display.get_surface()
        Showscoreboard(menus, stats)
    return leave and not menus.closed


Loadsettings()
while True:
    display = pg.display.get_surface()
    scale = min(display.get_width()/WIDTH, display.get_height()/HEIGHT)
    Displayframe.size = (round(WIDTH*scale), round(HEIGHT*scale))
    Displayframe.center = display.get_rect().center
    menu = Menus(display, screen, Displayframe)
    choice = menu.choose("Melody of the Mist", ["New Game", "Game Saves", "General Settings", "Quit"], "A tale of six fragments and a forgotten song.", True)
    if choice is None or choice == 3:
        break
    if choice == 2:
        menu.settings()
        if menu.closed:
            break
        continue
    saved = None
    if choice == 1:
        saves = slots()
        selected = menu.choose("Game Saves", Slotlabels(saves)+["Back"], "Choose a saved playthrough.")
        if selected is None or selected == 3:
            continue
        saved = saves[selected]
        if not saved:
            menu.choose("No save game found", ["Back"])
            continue
        profile = saved
    else:
        chosen = Chooseclass(display, screen, Displayframe)
        if chosen is False:
            break
        if chosen is None:
            continue
        character = menu.choose("Character Selection", ["Male", "Female"], "Choose a character.")
        if character is None:
            continue
        fragments = ["Piano", "Guitar", "Flute", "Harp", "Cello", "Violin"]
        fragment = menu.choose("Fragment Selection", fragments, "Choose the instrument your character is attuned to.")
        if fragment is None:
            continue
        weapons = ["Ivory Blade", "Ivory Knife", "Ivory Maul", "Ivory Focus", "Ivory Bow"]
        weapon = menu.choose("Starting Weapon", ["Class default"]+weapons)
        if weapon is None:
            continue
        start = menu.choose("Begin the Journey", ["Tutorial", "Start Game"], "Start in the Traveller's Passage or skip to Lantern Shelter.")
        if start is None:
            continue
        if not Playprologue(display, screen, Displayframe):
            break
        profile = {"class":chosen, "character":("Male", "Female")[character], "fragment":fragments[fragment], "starter":weapons[weapon-1] if weapon else None, "tutorial":start==0}
    try:
        if not Playrun(display, screen, Displayframe, profile, saved):
            break
    except (KeyError, ValueError, TypeError) as error:
        if not saved:
            raise
        menu.choose("Save could not be loaded", ["Back"], "The save is incomplete or from a different build.")
pg.quit()
