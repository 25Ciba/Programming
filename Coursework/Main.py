import pygame as pg
from TestMap import TestMap
from Loot import BossDrop, CATEGORIES, VISIBLE_ITEMS, category_tab, draw_hand_hud, draw_inventory, inventory_box, inventory_items, item_row, make_chests, nearby_chest
from Items import ITEMS, drink, equip
from Menus import Menus, KEYS, key_name, load_settings, matches
from Saves import slots, slot_labels, save_run, restore_run
from Store import Store, earn_experience, experience_needed
from Scoreboard import draw_scoreboard, record_score, show_scoreboard
from Clans import SKILLS, choose_class, configure_class
from Story import TUTORIAL_START, play_prologue
from DungeonLayout import START_X, START_Y
from Hud import GOLD, draw_status, draw_minimap, draw_overview, draw_aim_ring
from Classes import Player, EnemyManager, Camera, Map, MAP_WIDTH, MAP_HEIGHT

# Start Pygame
pg.display.init()
pg.font.init()
WIDTH = 1200
HEIGHT = 800
desktop_width, desktop_height = pg.display.get_desktop_sizes()[0]
window_scale = min(1, (desktop_width - 80) / WIDTH, (desktop_height - 150) / HEIGHT)
window_size = (round(WIDTH * window_scale), round(HEIGHT * window_scale))
display = pg.display.set_mode(window_size, pg.RESIZABLE)
screen = pg.Surface((WIDTH, HEIGHT)).convert()
display_frame = display.get_rect()
scale = min(display_frame.width / WIDTH, display_frame.height / HEIGHT)
display_frame.size = (round(WIDTH * scale), round(HEIGHT * scale))
display_frame.center = display.get_rect().center
pg.display.set_caption("Melody of the Mist")
def play_run(display, screen, display_frame, profile, saved=None):

    fullscreen = False
    window_size = display.get_size()
    clock = pg.time.Clock()
    running = True
    show_map = show_test_map = show_inventory = show_coordinates = False
    boss_prompt = None
    font = pg.font.Font(None,28)
    small_font = pg.font.Font(None,22)
    # Create the game objects
    game_map = Map()
    player = Player(screen)
    player.character = profile.get("character","Male")
    player.fragment = profile.get("fragment","Piano")
    inventory = configure_class(player, profile["class"])
    starter = profile.get("starter")
    if starter:
        inventory[starter] = 1
        equip(player,starter)
    player.x, player.y = TUTORIAL_START if profile.get("tutorial",True) else (START_X,START_Y)
    selected_item = 0
    inventory_category = CATEGORIES.index("Misc")
    boss_drops = []
    rewarded_bosses = set()
    chests = make_chests(screen, game_map, player)
    enemy_manager = EnemyManager(screen, player, game_map)
    camera = Camera(screen, MAP_WIDTH, MAP_HEIGHT)
    test_map = TestMap(game_map, enemy_manager.enemies, 23040, 23040)
    stats = {"score":0,"coins":12,"time_survived":0,"level":1,"experience":0,
             "areas_cleared":0,"enemies_felled":0,"items_collected":0,
             "damage_dealt":0,"damage_taken":0,"highest_hit":0}
    player.progress = stats
    ending_record = None
    if saved:
        restore_run(saved,screen,player,inventory,game_map,enemy_manager,chests,boss_drops,rewarded_bosses,stats)
    camera.update(player)
    menus = Menus(display,screen,display_frame)
    leave = False
    message = "Progress loaded." if saved else ("Traveller's Passage. Follow the path north to leave." if profile.get("tutorial",True) else f"Lantern Shelter. You attuned to {player.fragment}.")
    message_timer = 6.0

    # Make the mist once. The clear part follows the player.
    vision = player.pvisionRadius()
    fog_radius = vision + 150
    mist = pg.Surface((fog_radius * 2, fog_radius * 2), pg.SRCALPHA)
    mist.fill((11, 14, 24, 240))
    for radius in range(fog_radius, vision - 1, -1):
        fade = (radius - vision) / (fog_radius - vision)
        pg.draw.circle(mist, (11, 14, 24, int(240 * fade)), (fog_radius, fog_radius), radius)
    fog_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

    def pick_position(mouse_position, frame, camera):

        if not frame.collidepoint(mouse_position):
            return None
        x = round((mouse_position[0] - frame.x) * WIDTH / frame.width)
        y = round((mouse_position[1] - frame.y) * HEIGHT / frame.height)
        return x, y, round(x + camera.offset.x), round(y + camera.offset.y)


    def collect_defeats():

        for enemy in enemy_manager.enemies:
            if enemy.current_hp <= 0 and not enemy.reward_claimed:
                enemy.reward_claimed = True
                coins,experience = {
                    "Common":(3,10),"Strong":(6,18),"Elite":(9,28),
                    "Boss":(14,48),"Overture":(25,90)
                }.get(enemy.enemy_type,(42,160))
                stats["coins"] += coins
                stats["enemies_felled"] += 1
                stats["score"] += experience
                earn_experience(stats,experience)
            if enemy.current_hp > 0 or enemy.name in rewarded_bosses:
                continue
            if enemy.enemy_type == "Overture":
                item = "Primordial Instrument Blueprint"
            elif enemy.name.endswith(" Ultra Boss"):
                item = enemy.instrument + " Fragment"
            else:
                continue
            boss_drops.append(BossDrop(screen, enemy.x, enemy.y, item))
            rewarded_bosses.add(enemy.name)
            stats["areas_cleared"] = len(rewarded_bosses)

    # Main game loop
    while running:
        elapsed = clock.tick(60) / 1000
        dt = min(elapsed, 0.05)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE and not fullscreen:
                window_size = event.size
                scale = min(event.w / WIDTH, event.h / HEIGHT)
                display_frame.size = (round(WIDTH * scale), round(HEIGHT * scale))
                display_frame.center = display.get_rect().center
            elif game_map.story.ending is not None:
                continue
            elif event.type == pg.KEYDOWN:
                if boss_prompt:
                    if event.key in (pg.K_RETURN, pg.K_y):
                        boss_prompt.allowed = True
                        boss_prompt = None
                    elif event.key in (pg.K_ESCAPE, pg.K_n):
                        boss_prompt = None
                    continue
                if show_inventory:
                    if matches(event,"Inventory") or event.key == pg.K_ESCAPE:
                        show_inventory = False
                    elif event.key in (pg.K_LEFT, pg.K_RIGHT):
                        inventory_category = (inventory_category + (1 if event.key == pg.K_RIGHT else -1)) % len(CATEGORIES)
                        selected_item = 0
                    elif event.key in (pg.K_UP, pg.K_DOWN, pg.K_RETURN):
                        items = inventory_items(inventory, inventory_category)
                        if items and event.key == pg.K_RETURN:
                            item = items[selected_item][0]
                            if item in ITEMS:
                                message = drink(player, inventory, item) if ITEMS[item][0] == "Potions" else equip(player, item)
                                message_timer = 3.0 if message else 0
                                selected_item = min(selected_item, max(0, len(inventory_items(inventory, inventory_category)) - 1))
                        elif items:
                            selected_item = (selected_item + (1 if event.key == pg.K_DOWN else -1)) % len(items)
                    continue
                if matches(event,"Inventory") and not show_test_map and not show_coordinates:
                    show_map = False
                    show_inventory = True
                elif event.key == pg.K_F4:
                    show_test_map = not show_test_map
                    show_map = False
                    show_coordinates = False
                elif show_test_map:
                    if event.key == pg.K_F8:
                        game_map.story.testing_finale = True
                        game_map.story.move(player,(9950,30780))
                        camera.update(player)
                        show_test_map = False
                        message = "Finale test. Follow the stairs and press E at the altar."
                        message_timer = 5
                    elif event.key == pg.K_ESCAPE:
                        show_test_map = False
                    continue
                elif event.key == pg.K_ESCAPE:
                    menus.display = display
                    option = menus.choose("Paused",["Resume","Save and Return","General Settings","Return to Main Menu"],f"{stats['coins']} coins   |   Score {stats['score']}")
                    if option == 1:
                        saves = slots()
                        slot = menus.choose("Save Game",slot_labels(saves),"Choose a slot.")
                        if slot is not None:
                            if not saves[slot] or menus.choose("Overwrite save?",["Keep existing save","Overwrite this slot"]) == 1:
                                collect_defeats()
                                save_run(slot,player,inventory,game_map,enemy_manager,chests,boss_drops,rewarded_bosses,stats)
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
                        display = pg.display.set_mode(window_size, pg.RESIZABLE)
                    scale = min(display.get_width() / WIDTH, display.get_height() / HEIGHT)
                    display_frame.size = (round(WIDTH * scale), round(HEIGHT * scale))
                    display_frame.center = display.get_rect().center
                elif event.key == pg.K_F3:
                    show_coordinates = not show_coordinates
                    show_map = False
                elif matches(event,"Map"):
                    show_coordinates = False
                    show_map = not show_map
                elif any(matches(event,f"Skill {index}") for index in range(1,5)) and not show_map and not show_coordinates:
                    point = pick_position(pg.mouse.get_pos(), display_frame, camera)
                    cursor = point[2:] if point else (player.x, player.y + 120)
                    index = next(index for index in range(4) if matches(event,f"Skill {index+1}"))
                    message = player.powers.cast(index, cursor, game_map)
                    message_timer = 2.0
                elif matches(event,"Heal") and not show_map and not show_coordinates:
                    message = drink(player, inventory)
                    message_timer = 3.0
                elif matches(event,"Interact") and not show_map and not show_coordinates:
                    story_message = game_map.story.interact(player, inventory, (START_X, START_Y))
                    if story_message:
                        message = story_message
                        message_timer = 6.0
                        camera.update(player)
                        continue
                    previous_count = sum(inventory.values())
                    settlement_message = game_map.settlements.interact(player, inventory)
                    if settlement_message:
                        stats["items_collected"] += max(0,sum(inventory.values())-previous_count)
                        message = settlement_message
                        message_timer = 6.0
                        camera.update(player)
                        continue
                    action = game_map.arena_art.nearby_action(player)
                    if action:
                        door, confirm = action
                        if confirm:
                            boss_prompt = door
                        else:
                            message = door.inscription
                            message_timer = 6.0
                        continue
                    drop = nearby_chest(boss_drops, player)
                    if drop:
                        message = drop.open(inventory)
                        boss_drops.remove(drop)
                        stats["items_collected"] += 1
                        message_timer = 4.0
                        continue
                    chest = nearby_chest(chests, player)
                    if chest:
                        previous_count = sum(inventory.values())
                        message = chest.open(inventory)
                        stats["items_collected"] += max(0,sum(inventory.values())-previous_count)
                        message_timer = 3.0
                        continue
                    readable = game_map.ruins_art.interact(player) or game_map.frost_art.interact(player) or game_map.guitar_art.interact(player) or game_map.flute_art.interact(player) or game_map.cello_art.interact(player) or game_map.harp_art.interact(player) or game_map.violin_art.interact(player)
                    if readable:
                        message = readable[1]
                        message_timer = 6.0
                elif matches(event,"Market") and not show_map and not show_coordinates:
                    trader = game_map.settlements.nearby(player)
                    if trader and trader[1] == "Speak to Market trader":
                        menus.display = display
                        Store("Village Market",inventory,stats,player).run(menus)
                        clock.tick()
                    else:
                        message = "Visit a village market trader."
                    if menus.closed:
                        running = False
                    message_timer = 3.0
                elif matches(event,"Attack") and not show_map and not show_coordinates:
                    point = pick_position(pg.mouse.get_pos(),display_frame,camera)
                    player.attack_enemies(enemy_manager.enemies,game_map,point[2:] if point else None)
                    game_map.story.practice(player)
                elif matches(event,"Defend") and not show_map and not show_coordinates:
                    if player.begin_block():
                        message = "Block!"
                        message_timer = .6
                elif matches(event,"Dash") and not show_map and not show_coordinates:
                    if player.begin_dash():
                        message = "Dash!"
                        message_timer = 0.6
            elif event.type == pg.MOUSEBUTTONDOWN and show_inventory:
                point = pick_position(event.pos, display_frame, camera)
                if event.button == 1 and point:
                    for index in range(len(CATEGORIES)):
                        if category_tab(inventory_box(screen), index).collidepoint(point[:2]):
                            inventory_category = index
                            selected_item = 0
                            break
                    else:
                        items = inventory_items(inventory, inventory_category)
                        start = max(0, selected_item - VISIBLE_ITEMS + 1)
                        for index in range(min(VISIBLE_ITEMS, len(items) - start)):
                            if item_row(inventory_box(screen), index).collidepoint(point[:2]):
                                selected_item = start + index
                                break
            elif event.type == pg.MOUSEWHEEL and show_inventory:
                items = inventory_items(inventory, inventory_category)
                selected_item = max(0, min(len(items) - 1, selected_item - event.y))
            elif event.type == pg.MOUSEBUTTONDOWN and show_test_map:
                point = pick_position(event.pos, display_frame, camera)
                if event.button == 1 and point:
                    destination = test_map.destination(point[:2], player)
                    if destination:
                        player.x, player.y = destination
                        player.dash_time = player.block_time = player.attack_animation_time = 0
                        player.dash_trail.clear()
                        player.shots.clear()
                        player.powers.leave_area()
                        player.attack_stage = 0
                        player.attack_targets.clear()
                        player.attack_queued = False
                        camera.update(player)
                        show_test_map = False
            elif event.type == pg.MOUSEBUTTONDOWN and show_coordinates:
                if event.button == 1:
                    point = pick_position(event.pos, display_frame, camera)
                    if point:
                        x, y, world_x, world_y = point
                        print(f"({world_x}, {world_y})  {game_map.location_name(world_x, world_y)}", flush=True)
            elif event.type == pg.MOUSEBUTTONDOWN and not show_map and not boss_prompt:
                if matches(event,"Attack"):
                    point = pick_position(event.pos, display_frame, camera)
                    if point:
                        player.attack_enemies(enemy_manager.enemies, game_map, point[2:])
                        game_map.story.practice(player)
                elif matches(event,"Defend"):
                    if player.begin_block():
                        message = "Block!"
                        message_timer = 0.6

        if not running:
            break

        # Update the game objects
        if game_map.story.ending is None and not show_map and not show_test_map and not show_coordinates and not show_inventory and not boss_prompt:
            stats["time_survived"] += dt
            player.update(dt)
            game_map.story.update(dt)
            game_map.gate.update(dt, player)
            game_map.arena_art.update(dt, player, enemy_manager.enemies)
            player.keybinds(dt, game_map)
            collect_defeats()
            enemy_manager.update(dt)
            camera.update(player)

        if player.current_lives <= 0:
            leave = True
            running = False
        if message_timer > 0:
            message_timer -= dt

        # Draw the map and game objects
        screen.fill((10, 13, 21))
        game_map.render(screen, camera)
        game_map.frost_art.render_lake(screen, camera, player)
        player.powers.render(screen, camera)
        actors = game_map.ruins_art.props + game_map.frost_art.props + game_map.guitar_art.props + game_map.flute_art.props + game_map.cello_art.props + game_map.harp_art.props + game_map.violin_art.props + game_map.arena_art.relics + chests + boss_drops + enemy_manager.enemies + [player]
        actors.sort(key=lambda actor: actor.y)
        for actor in actors:
            if actor in enemy_manager.enemies:
                enemy_manager.render_enemy(actor,camera)
            else:
                actor.render(camera)

        if game_map.story.ending is not None:
            running = game_map.story.finish(screen, camera, player, elapsed) and running
            if game_map.story.ending >= 11.5:
                if ending_record is None:
                    ending_record = record_score(stats["score"])
                draw_scoreboard(screen,stats,*ending_record,top=340)
            display.fill((0, 0, 0))
            display.blit(pg.transform.scale(screen, display_frame.size), display_frame)
            pg.display.flip()
            continue

        # Draw fog of war
        fog_surface.fill((11, 14, 24, 240))
        player_screen_pos = camera.apply(player.x, player.y)
        mist_rect = mist.get_rect(center=player_screen_pos)
        fog_surface.blit(mist, mist_rect, special_flags=pg.BLEND_RGBA_MIN)
        game_map.arena_art.reveal_fog(fog_surface, camera, game_map.room_floors)
        game_map.arena_art.hide_beyond_doors(fog_surface, camera, player)
        screen.blit(fog_surface, (0, 0))

        if player.uses_ranged_weapon() and not (show_inventory or show_map or show_test_map or show_coordinates or boss_prompt):
            point = pick_position(pg.mouse.get_pos(), display_frame, camera)
            if point and any(enemy.current_hp > 0 and (enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2 <= vision ** 2 for enemy in enemy_manager.enemies):
                draw_aim_ring(screen, player_screen_pos, player.aim_direction(point[2:]))

        draw_status(screen, small_font, player)
        counters = small_font.render(f"Level {stats['level']}   /   XP {stats['experience']}/{experience_needed(stats['level'])}   /   {stats['coins']} coins", True, GOLD)
        screen.blit(counters,(20,102))
        draw_hand_hud(screen, small_font, player, inventory)
        for index, (name, _, _) in enumerate(SKILLS[player.clan]):
            slot = pg.Rect(WIDTH - 410 + index * 98, HEIGHT - 67, 94, 42)
            pg.draw.rect(screen, (23, 20, 34), slot)
            pg.draw.rect(screen, (80, 72, 92), slot, 1)
            remaining = player.powers.cooldowns[index]
            key = key_name(KEYS[f"Skill {index + 1}"])
            caption = f"{key}   {round(remaining, 1)}s" if remaining else f"{key}   Ready"
            if name == "Summon" and player.powers.familiar is not None:
                caption = f"{key}   Dismiss"
            screen.blit(small_font.render(caption, True, GOLD), (slot.x + 5, slot.y + 4))
            screen.blit(pg.font.Font(None, 17).render(name, True, (221, 210, 218)), (slot.x + 5, slot.y + 23))
        draw_minimap(screen, small_font, game_map, player)

        readable = game_map.ruins_art.nearby_readable(player) or game_map.frost_art.nearby_readable(player) or game_map.guitar_art.nearby_readable(player) or game_map.flute_art.nearby_readable(player) or game_map.cello_art.nearby_readable(player) or game_map.harp_art.nearby_readable(player) or game_map.violin_art.nearby_readable(player)
        chest = nearby_chest(chests, player)
        drop = nearby_chest(boss_drops, player)
        feature = game_map.settlements.nearby(player)
        story_target = game_map.story.target(player)
        if message_timer <= 0 and story_target:
            hint = small_font.render(f"{key_name(KEYS['Interact'])}   {story_target[0]}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif message_timer <= 0 and feature:
            hint = small_font.render(f"{key_name(KEYS['Interact'])}   {feature[1]}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif message_timer <= 0 and drop:
            hint = small_font.render(f"{key_name(KEYS['Interact'])}   Pick up {drop.item}", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif message_timer <= 0 and chest and not chest.is_open:
            hint = small_font.render(f"{key_name(KEYS['Interact'])}   Open chest", True, GOLD)
            screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))
        elif message_timer <= 0 and readable:
            prompt = small_font.render(f"{key_name(KEYS['Interact'])}   {readable[0]}", True, (241, 213, 157))
            screen.blit(prompt, prompt.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)))

        if message_timer > 0:
            message_text = small_font.render(message, True, (235, 242, 250))
            message_box = message_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 18)).inflate(24, 14)
            pg.draw.rect(screen, (20, 24, 34), message_box)
            screen.blit(message_text, message_text.get_rect(center=message_box.center))

        if show_map:
            draw_overview(screen, font, small_font, game_map, player, MAP_WIDTH, MAP_HEIGHT)

        # Show the finished frame
        if boss_prompt:
            panel = pg.Rect(0, 0, 710, 150)
            panel.center = (WIDTH // 2, HEIGHT // 2)
            pg.draw.rect(screen, (17, 21, 33), panel)
            pg.draw.rect(screen, boss_prompt.metal, panel, 2)
            title = font.render(f"Challenge {boss_prompt.boss_name}?", True, (244, 234, 221))
            line = small_font.render(boss_prompt.challenge, True, (218, 222, 235))
            controls = small_font.render("Enter / Y   Open the door       Esc / N   Step away", True, boss_prompt.metal)
            screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.y + 20)))
            screen.blit(line, line.get_rect(midtop=(panel.centerx, panel.y + 60)))
            screen.blit(controls, controls.get_rect(midtop=(panel.centerx, panel.y + 108)))
        elif not show_map and not show_coordinates and message_timer <= 0:
            action = game_map.arena_art.nearby_action(player)
            if action:
                door, confirm = action
                label = "E   Approach the sealed door" if confirm else "E   Read the traveller's note"
                hint = small_font.render(label, True, (248, 229, 188))
                box = hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 22))
                pg.draw.rect(screen, (20, 24, 34), box.inflate(14, 8))
                screen.blit(hint, box)

        if show_coordinates:
            point = pick_position(pg.mouse.get_pos(), display_frame, camera)
            text = "F3: resume  |  Left click to print the position in the terminal"
            if point:
                x, y, world_x, world_y = point
                colour = (122, 230, 191) if game_map.can_move_circle(world_x, world_y, player.size) else (241, 125, 109)
                pg.draw.line(screen, colour, (x - 11, y), (x + 11, y), 2)
                pg.draw.line(screen, colour, (x, y - 11), (x, y + 11), 2)
                text = f"({world_x}, {world_y})  |  {game_map.location_name(world_x, world_y)}  |  Click to print  |  F3 to resume"
            label = small_font.render(text, True, (234, 241, 246))
            box = label.get_rect(midtop=(WIDTH // 2, 15))
            pg.draw.rect(screen, (20, 24, 34), box.inflate(18, 10))
            screen.blit(label, box)

        if show_test_map:
            point = pick_position(pg.mouse.get_pos(), display_frame, camera)
            test_map.render(screen, font, small_font, player, point[:2] if point else None)

        if show_inventory:
            draw_inventory(screen, inventory, inventory_category, selected_item, player)

        display.fill((0, 0, 0))
        display.blit(pg.transform.scale(screen, display_frame.size), display_frame)
        pg.display.flip()

    if leave:
        menus.display = pg.display.get_surface()
        show_scoreboard(menus,stats)
    return leave and not menus.closed


load_settings()
while True:
    display = pg.display.get_surface()
    scale = min(display.get_width()/WIDTH,display.get_height()/HEIGHT)
    display_frame.size = (round(WIDTH*scale),round(HEIGHT*scale))
    display_frame.center = display.get_rect().center
    menu = Menus(display,screen,display_frame)
    choice = menu.choose("Melody of the Mist",["New Game","Game Saves","General Settings","Quit"],"A tale of six fragments and a forgotten song.",True)
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
        selected = menu.choose("Game Saves",slot_labels(saves)+["Back"],"Choose a saved playthrough.")
        if selected is None or selected == 3:
            continue
        saved = saves[selected]
        if not saved:
            menu.choose("No save game found",["Back"])
            continue
        profile = saved
    else:
        chosen = choose_class(display,screen,display_frame)
        if chosen is False:
            break
        if chosen is None:
            continue
        character = menu.choose("Character Selection",["Male","Female"],"Choose a character.")
        if character is None:
            continue
        fragments = ["Piano","Guitar","Flute","Harp","Cello","Violin"]
        fragment = menu.choose("Fragment Selection",fragments,"Choose the instrument your character is attuned to.")
        if fragment is None:
            continue
        weapons = ["Ivory Blade","Ivory Knife","Ivory Maul","Ivory Focus","Ivory Bow"]
        weapon = menu.choose("Starting Weapon",["Class default"]+weapons)
        if weapon is None:
            continue
        start = menu.choose("Begin the Journey",["Tutorial","Start Game"],"Start in the Traveller's Passage or skip to Lantern Shelter.")
        if start is None:
            continue
        if not play_prologue(display,screen,display_frame):
            break
        profile = {"class":chosen,"character":("Male","Female")[character],"fragment":fragments[fragment],"starter":weapons[weapon-1] if weapon else None,"tutorial":start==0}
    try:
        if not play_run(display,screen,display_frame,profile,saved):
            break
    except (KeyError,ValueError,TypeError) as error:
        if not saved:
            raise
        menu.choose("Save could not be loaded",["Back"],"The save is incomplete or from a different build.")
pg.quit()
