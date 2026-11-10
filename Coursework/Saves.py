from datetime import datetime
from Menus import DATA, Readdata, Writedata
from Items import ITEMS, equip
from Loot import BossDrop
from Story import REQUIRED


# Stats for the current run

class RunStats:

    def __init__(self):

        self.score = 0
        self.coins = 12
        self.Timesurvived = 0
        self.level = 1
        self.experience = 0
        self.Areascleared = 0
        self.Enemiesfelled = 0
        self.Itemscollected = 0
        self.Damagedealt = 0
        self.Damagetaken = 0
        self.Highesthit = 0


def Slotpath(slot):

    return DATA / f"run-{slot+1}.json"


def slots():

    return [Readdata(Slotpath(i)) for i in range(3)]


def Slotlabels(saves):

    return [f"{i+1}. {save.get('class', 'Unknown')}  |  {save.get('saved_at', '')}" if save else f"{i+1}. Empty slot" for i, save in enumerate(saves)]


def Enemykey(enemy):

    return f"{enemy.name}:{enemy.home}"


def Saverun(slot, player, inventory, Gamemap, manager, chests, drops, rewarded, stats):

    village = Gamemap.settlements
    Savedenemies = {}
    for enemy in manager.enemies:
        if enemy.Currenthp <= 0:
            continue
        Teleportindex = getattr(enemy, "Teleportindex", 0)
        Secondphase = getattr(enemy, "Secondphase", False)
        speed = getattr(enemy, "speed", 0)
        Savedenemies[Enemykey(enemy)] = [
            enemy.x, enemy.y, enemy.Currenthp, Teleportindex,
            Secondphase, enemy.Maxhp, enemy.attack, speed
        ]

    data = {
        "version": 1,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "class": player.clan,
        "character": player.character,
        "fragment": player.fragment,
        "player": [player.x, player.y, player.Currenthp, player.Currentmana, player.Currentlives, player.facing],
        "inventory": inventory,
        "equipment": [player.Mainhand, player.Offhand, player.armour, player.charm],
        "enemies": Savedenemies,
        "chests": [index for index, chest in enumerate(chests) if chest.Isopen],
        "drops": [[drop.x, drop.y, drop.item] for drop in drops if not drop.Isopen],
        "rewarded": sorted(rewarded),
        "doors": [[door.allowed, door.cleared] for door in Gamemap.Arenaart.doors],
        "villages": {
            "loot": list(village.Loottaken),
            "levers": sorted(village.levers),
            "sequence": village.sequence,
            "solved": sorted(village.solved),
            "desk": sorted(village.Deskseals),
            "orchard": sorted(village.Orchardseals)
        },
        "stats": {
            "score": stats.score,
            "coins": stats.coins,
            "time_survived": stats.Timesurvived,
            "level": stats.level,
            "experience": stats.experience,
            "areas_cleared": stats.Areascleared,
            "enemies_felled": stats.Enemiesfelled,
            "items_collected": stats.Itemscollected,
            "damage_dealt": stats.Damagedealt,
            "damage_taken": stats.Damagetaken,
            "highest_hit": stats.Highesthit,
        }
    }
    Writedata(Slotpath(slot), data)


def Restorerun(data, screen, player, inventory, Gamemap, manager, chests, drops, rewarded, stats):

    x, y, hp, mana, lives, facing = data["player"]
    player.x, player.y, player.facing = x, y, facing
    player.Currenthp = max(1, min(player.Maxhp, hp))
    player.Currentmana = max(0, min(player.Maxmana, mana))
    player.Currentlives = lives
    inventory.clear()
    inventory.update(data["inventory"])
    for item in data["equipment"]:
        if item in ITEMS and inventory.get(item, 0)>0:
            equip(player, item)
    living = data["enemies"]
    manager.enemies[:] = [enemy for enemy in manager.enemies if Enemykey(enemy) in living]
    for enemy in manager.enemies:
        stored=living[Enemykey(enemy)]
        enemy.x, enemy.y, enemy.Currenthp, teleport, phase, enemy.Maxhp, enemy.attack, enemy.speed=stored
        if hasattr(enemy, "Teleportindex"):
            enemy.Teleportindex, enemy.Secondphase=teleport, phase
    for index in data["chests"]:
        if 0<=index<len(chests):
            chests[index].Isopen=True
    drops.extend(BossDrop(screen, x, y, item) for x, y, item in data["drops"] if item in REQUIRED)
    rewarded.update(data["rewarded"])
    for door, (allowed, cleared) in zip(Gamemap.Arenaart.doors, data["doors"]):
        door.allowed, door.cleared=allowed, cleared
        if not Gamemap.Canmovecircle(player.x, player.y, player.size):
            door.progress=1 if allowed or cleared else 0
    village=Gamemap.settlements
    state=data["villages"]
    village.Loottaken.update(tuple(item) for item in state["loot"])
    village.levers.update(state["levers"])
    village.sequence[:]=state["sequence"]
    village.solved.update(state["solved"])
    village.Deskseals.update(state["desk"])
    village.Orchardseals.update(state["orchard"])
    Savedstats = data["stats"]
    stats.score = Savedstats.get("score", stats.score)
    stats.coins = Savedstats.get("coins", stats.coins)
    stats.Timesurvived = Savedstats.get("time_survived", stats.Timesurvived)
    stats.level = Savedstats.get("level", stats.level)
    stats.experience = Savedstats.get("experience", stats.experience)
    stats.Enemiesfelled = Savedstats.get("enemies_felled", stats.Enemiesfelled)
    stats.Itemscollected = Savedstats.get("items_collected", stats.Itemscollected)
    stats.Damagedealt = Savedstats.get("damage_dealt", stats.Damagedealt)
    stats.Damagetaken = Savedstats.get("damage_taken", stats.Damagetaken)
    stats.Highesthit = Savedstats.get("highest_hit", stats.Highesthit)
    if "seconds" in Savedstats:
        stats.Timesurvived = Savedstats["seconds"]
    stats.Areascleared = len(rewarded)
