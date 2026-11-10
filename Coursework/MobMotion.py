import math
from functools import lru_cache
import pygame as pg
from Guitar import Creatureposeframes
from Ruins import Creatureframes

# Keep the original four rows in place so the bosses can still use them.
DIRECTIONROWS = (2, 4, 0, 5, 1, 6, 3, 7)

AIRBORNE = ("Echo Bat", "Glasswing Moth", "Rustwing Bat", "Reed Wisp", "Rosin Spirit", "Ripple Wisp", "Bowshade")

POSES = {
    "Copper Crawler": ("GuitarCaverns", "Crawler"),
    "Rustwing Bat": ("GuitarCaverns", "Rustwing"),
    "Chalk Skitter": ("FluteCloister", "Skitter"),
    "Reed Wisp": ("FluteCloister", "Wisp"),
    "Silt Scorpion": ("CelloCatacombs", "Scorpion"),
    "Rosin Spirit": ("CelloCatacombs", "Spirit"),
    "Mossback Snapper": ("HarpReservoir", "Snapper"),
    "Ripple Wisp": ("HarpReservoir", "Wisp")
}


def Facingrow(x, y):

    return DIRECTIONROWS[round(math.atan2(y, x) / (math.pi / 4)) % 8]


def Directionalrows(frames, Sourceangle, airborne):

    rows = [[] for _ in range(8)]
    for heading, row in enumerate(DIRECTIONROWS):
        if row in (3, 6, 7):
            continue
        left = heading in (3, 4)
        angle = (180 - heading * 45 if left else heading * 45) % 360
        for frame in frames:
            box = frame.get_bounding_rect()
            body = frame.subsurface(box)
            if airborne:
                # Keep flying bodies upright. Banking follows the heading while the wings flap.
                body = pg.transform.rotate(body, {0: -10, 45: -4, 90: 0}[angle])
                if angle == 90:
                    body = pg.transform.scale(body, (max(1, body.get_width() * 4 // 5), body.get_height()))
            else:
                body = pg.transform.rotate(body, Sourceangle - angle)
                if angle != Sourceangle:
                    body = pg.transform.scale(body, (body.get_width(), max(1, round(body.get_height() * .83))))
            if left:
                body = pg.transform.flip(body, True, False)
            Centeroffset = box.centerx - frame.get_width() // 2
            canvas = pg.Surface((frame.get_width() + 40, frame.get_height() + 32), pg.SRCALPHA)
            Centerx = canvas.get_width() // 2 + (-Centeroffset if left else Centeroffset)
            bottom = canvas.get_height() - (frame.get_height() - box.bottom)
            canvas.blit(body, body.get_rect(midbottom=(Centerx, bottom)))
            rows[row].append(canvas)
    return rows


def Addviewrows(actions, sprites, headings, airborne, winged, forward):

    frame = actions[0][0][0]
    bounds = frame.get_bounding_rect()
    # Compare filled pixels so a narrower silhouette does not shrink the whole mob.
    front = [actions[0][row][0] for row in (0, 2, 4)]
    Frontarea = sum(pg.mask.from_surface(pose).count() for pose in front) / len(front)
    if winged:
        reference = sprites[1]
    else:
        reference = sprites[0]
    Referencearea = pg.mask.from_surface(reference).count()
    ratio = math.sqrt(Frontarea / Referencearea)
    ratio = min(ratio, (frame.get_width() - 16) / max(pose.get_width() for pose in sprites))
    sprites = [pg.transform.scale(pose, (round(pose.get_width() * ratio), round(pose.get_height() * ratio))) for pose in sprites]
    poses = [
        [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 1)],
        [(0, -1, 0), (0, 0, 1), (1, 1, 2), (1, 1, 1), (1, 0, 0), (0, -1, 1)],
        [(2, 0, 5), (2, 0, 8), (2, 0, 5), (1, 0, 3), (1, 0, 1), (0, 0, 0)],
        [(0, 0, 0), (0, 0, -1), (1, 0, -2), (1, 0, -3)],
        [(1, 0, 0), (0, 0, -1), (0, 0, -2), (0, 0, -3)]
    ]
    if winged:
        poses[1] = [(0, 0, 0), (1, 0, 1), (2, 0, 3), (2, 0, 4), (1, 0, 2), (0, 0, 1)]
    for Actionindex, animation in enumerate(poses):
        for row, bank in headings:
            frames = []
            for index, (Poseindex, x, lift) in enumerate(animation):
                body = sprites[Poseindex]
                if Actionindex == 1 and not airborne and index >= 4:
                    body = pg.transform.flip(body, True, False)
                if bank:
                    body = pg.transform.rotate(body, bank // 2 if airborne else bank)
                if Actionindex == 4:
                    height = max(2, round(body.get_height() * (1 - index * .18)))
                    body = pg.transform.scale(body, (body.get_width(), height))
                canvas = pg.Surface(frame.get_size(), pg.SRCALPHA)
                if forward and Actionindex == 2:
                    lift = -lift
                center = canvas.get_width() // 2 + x - round(bank * lift / 30)
                canvas.blit(body, body.get_rect(midbottom=(center, bounds.bottom - lift)))
                frames.append(canvas)
            actions[Actionindex][row] = frames


def Steadywispsize(actions):

    size = actions[0][2][0].get_bounding_rect().size
    for action in actions[:4]:
        for row in action:
            for index, frame in enumerate(row):
                bounds = frame.get_bounding_rect()
                body = pg.transform.scale(frame.subsurface(bounds), size)
                stable = pg.Surface(frame.get_size(), pg.SRCALPHA)
                stable.blit(body, body.get_rect(midbottom=bounds.midbottom))
                row[index] = stable


def Scoreswarmframes():

    actions = []
    for action in range(5):
        frames = []
        for step in range(8):
            progress = step / 7
            frame = pg.Surface((124, 112), pg.SRCALPHA)
            center = pg.Vector2(62, 75)
            spread = 21
            if action == 3:
                spread -= round(11 * progress)
            elif action == 2:
                spread += round(22 * math.sin(math.pi * progress))
            elif action == 4:
                spread += round(18 * progress)
            pg.draw.ellipse(frame, (25, 19, 34, 120), (44, 94, 36, 9))
            for index in range(5):
                phase = index * math.tau / 5 + step * math.tau / 8
                position = center + pg.Vector2(math.cos(phase) * spread, math.sin(phase) * spread * .52)
                position.y -= 5 + index * 4
                if action == 4:
                    position.y += round(progress * 16)
                page = pg.Surface((24, 31), pg.SRCALPHA)
                edge = [(2, 2), (18, 1), (22, 6), (21, 26), (16, 29), (12, 26), (9, 29), (3, 26)]
                pg.draw.polygon(page, (57, 35, 50), edge)
                pg.draw.polygon(page, (209, 181, 142), [(4, 4), (17, 3), (20, 7), (19, 24), (16, 26), (12, 24), (9, 26), (5, 24)])
                pg.draw.polygon(page, (242, 212, 165), [(17, 3), (17, 8), (20, 7)])
                for y in (10, 13, 16, 19):
                    pg.draw.line(page, (117, 74, 82), (7, y), (17, y))
                pg.draw.circle(page, (75, 45, 60), (11, 17), 2)
                pg.draw.line(page, (75, 45, 60), (13, 17), (13, 10), 1)
                page = pg.transform.rotate(page, round(math.sin(phase) * 32))
                frame.blit(page, page.get_rect(center=position))
            frames.append(frame)
        actions.append([frames] * 8)
    return actions


@lru_cache(maxsize=16)
def Mobframes(Imagefolder, name):

    airborne = name in AIRBORNE
    if name == "Score Swarm":
        return Scoreswarmframes()
    if name == "Bowshade":
        folder = Imagefolder / "ViolinHall" / name
        front = [pg.image.load(folder / f"{index}.png").convert_alpha() for index in range(2)]
        rear = pg.image.load(folder / "2.png").convert_alpha()
        size = 55 if airborne else 71
        body = pg.transform.scale_by(front[0], size / max(front[0].get_size()))
        frame = pg.Surface((112, 106), pg.SRCALPHA)
        frame.blit(body, body.get_rect(midbottom=(56, 94)))
        actions = [[[frame] if row in (0, 2, 4) else [] for row in range(8)] for _ in range(5)]
        stride = pg.transform.rotate(front[0], 4)
        Backstride = pg.transform.rotate(rear, 4)
        Backattack = pg.transform.scale_by(rear, (1.08, 1.03))
        Addviewrows(actions, [front[0], stride, front[1]], [(0, 0), (1, -58), (2, 58), (4, 24), (5, -24)], airborne, False, True)
        Addviewrows(actions, [rear, Backstride, Backattack], [(3, 0), (6, 23), (7, -23)], airborne, False, False)
        return actions
    if name in POSES:
        region, stem = POSES[name]
        actions = Creatureposeframes(Imagefolder / region / "MobPoses", stem, 68 if airborne else 94, airborne)
        idle, run, strike, windup, death = [action[2] for action in actions]
    else:
        scale = 66 if airborne else 94
        idle, run, strike = [Creatureframes(Imagefolder, name, action, scale)[2] for action in ("Idle", "Run", "Attack")]
        windup = [idle[0], strike[0], strike[1]]
        death = []
        body = idle[0]
        for height in (90, 74, 51, 30):
            pose = pg.transform.scale(body, (body.get_width(), body.get_height() * height // 100))
            frame = pg.Surface(body.get_size(), pg.SRCALPHA)
            frame.blit(pose, pose.get_rect(midbottom=body.get_rect().midbottom))
            death.append(frame)
    if name == "Mossback Snapper":
        angle = 0
    else:
        angle = 45
    actions = [Directionalrows(action, angle, airborne) for action in (idle, run, strike, windup, death)]
    Rearfolder = Imagefolder / "MobRear" / name
    rear = [pg.image.load(Rearfolder / f"{index}.png").convert_alpha() for index in range(3)]
    winged = name in ("Echo Bat", "Glasswing Moth", "Rustwing Bat")
    Frontfolder = Imagefolder / "MobFront" / name
    if Frontfolder.is_dir():
        front = [pg.image.load(Frontfolder / f"{index}.png").convert_alpha() for index in range(3)]
        headings = [(0, 0), (4, 19), (5, -19)]
        if name in ("Echo Bat", "Reed Wisp"):
            headings += [(1, -39), (2, 39)]
        Addviewrows(actions, front, headings, airborne, winged, True)
    Addviewrows(actions, rear, [(3, 0), (6, 18), (7, -18)], airborne, winged, False)
    if name == "Reed Wisp":
        Steadywispsize(actions)
    return actions
