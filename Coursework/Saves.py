from datetime import datetime
from Menus import DATA, read_data, write_data
from Items import ITEMS, equip
from Loot import BossDrop
from Story import REQUIRED


def slot_path(slot):

    return DATA / f"run-{slot+1}.json"


def slots():

    return [read_data(slot_path(i)) for i in range(3)]


def slot_labels(saves):

    return [f"{i+1}. {save.get('class','Unknown')}  |  {save.get('saved_at','')}" if save else f"{i+1}. Empty slot" for i,save in enumerate(saves)]


def enemy_key(enemy):

    return f"{enemy.name}:{enemy.home}"


def save_run(slot, player, inventory, game_map, manager, chests, drops, rewarded, stats):

    village = game_map.settlements
    data = {
        "version": 1,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "class": player.clan,
        "character": player.character,
        "fragment": player.fragment,
        "player": [player.x,player.y,player.current_hp,player.current_mana,player.current_lives,player.facing],
        "inventory": inventory,
        "equipment": [player.main_hand,player.off_hand,player.armour,player.charm],
        "enemies": {enemy_key(enemy):[enemy.x,enemy.y,enemy.current_hp, getattr(enemy,"teleport_index",0),getattr(enemy,"second_phase",False),enemy.max_hp,enemy.attack,getattr(enemy,"speed",0)] for enemy in manager.enemies if enemy.current_hp>0},
        "chests": [index for index,chest in enumerate(chests) if chest.is_open],
        "drops": [[drop.x,drop.y,drop.item] for drop in drops if not drop.is_open],
        "rewarded": sorted(rewarded),
        "doors": [[door.allowed,door.cleared] for door in game_map.arena_art.doors],
        "villages": {
            "loot": list(village.loot_taken),
            "levers": sorted(village.levers),
            "sequence": village.sequence,
            "solved": sorted(village.solved),
            "desk": sorted(village.desk_seals),
            "orchard": sorted(village.orchard_seals)
        },
        "stats": stats
    }
    write_data(slot_path(slot),data)


def restore_run(data, screen, player, inventory, game_map, manager, chests, drops, rewarded, stats):

    x,y,hp,mana,lives,facing = data["player"]
    player.x,player.y,player.facing = x,y,facing
    player.current_hp = max(1,min(player.max_hp,hp))
    player.current_mana = max(0,min(player.max_mana,mana))
    player.current_lives = lives
    inventory.clear()
    inventory.update(data["inventory"])
    for item in data["equipment"]:
        if item in ITEMS and inventory.get(item,0)>0:
            equip(player,item)
    living = data["enemies"]
    manager.enemies[:] = [enemy for enemy in manager.enemies if enemy_key(enemy) in living]
    for enemy in manager.enemies:
        stored=living[enemy_key(enemy)]
        enemy.x,enemy.y,enemy.current_hp,teleport,phase,enemy.max_hp,enemy.attack,enemy.speed=stored
        if hasattr(enemy,"teleport_index"):
            enemy.teleport_index,enemy.second_phase=teleport,phase
    for index in data["chests"]:
        if 0<=index<len(chests):
            chests[index].is_open=True
    drops.extend(BossDrop(screen,x,y,item) for x,y,item in data["drops"] if item in REQUIRED)
    rewarded.update(data["rewarded"])
    for door,(allowed,cleared) in zip(game_map.arena_art.doors,data["doors"]):
        door.allowed,door.cleared=allowed,cleared
        if not game_map.can_move_circle(player.x,player.y,player.size):
            door.progress=1 if allowed or cleared else 0
    village=game_map.settlements
    state=data["villages"]
    village.loot_taken.update(tuple(item) for item in state["loot"])
    village.levers.update(state["levers"])
    village.sequence[:]=state["sequence"]
    village.solved.update(state["solved"])
    village.desk_seals.update(state["desk"])
    village.orchard_seals.update(state["orchard"])
    stats.update(data["stats"])
    if "seconds" in stats:
        stats["time_survived"] = stats.pop("seconds")
    stats["areas_cleared"] = len(rewarded)
    stats.setdefault("level",1)
    stats.setdefault("experience",0)
