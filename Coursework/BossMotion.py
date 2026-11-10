import math
import pygame as pg


def Loadbosssteps(folder, ready):

    idle = pg.image.load(folder / "Motion0.png").convert_alpha()
    idle = pg.transform.scale(idle, ready.get_size())
    frames = [idle]
    for index, side in [(1, -1), (2, 1)]:
        step = pg.image.load(folder / f"Motion{index}.png").convert_alpha()
        step = pg.transform.scale(step, ready.get_size())
        # Passing, planted stride, then weight settling over the front foot.
        passing = pg.Surface(ready.get_size(), pg.SRCALPHA)
        passing.blit(ready, (side * 2, -2))
        planted = pg.Surface(ready.get_size(), pg.SRCALPHA)
        planted.blit(step, (side * 3, 0))
        settle = pg.Surface(ready.get_size(), pg.SRCALPHA)
        shape = pg.transform.scale(step, (step.get_width(), step.get_height() - 4))
        settle.blit(shape, (side * 2, 4))
        frames.extend([passing, planted, settle])
    return frames


def Originalkeepersteps(ready):

    # Move the feet separately while keeping the original armour and mask.
    bounds = ready.get_bounding_rect()
    split = bounds.top + round(bounds.height * 0.78)
    center = bounds.centerx
    frames = []
    for stride in (0, -1, 1):
        frame = pg.Surface(ready.get_size(), pg.SRCALPHA)
        for left, width, side in [(bounds.left, center - bounds.left, -1), (center, bounds.right - center, 1)]:
            foot = pg.Rect(left, split - 8, width, bounds.bottom - split + 8)
            frame.blit(ready, (left + side * stride * 5, foot.y - max(0, side * stride) * 5), foot)
        torso = ready.subsurface((bounds.left, bounds.top, bounds.width, split - bounds.top + 4))
        drop = 3 if stride == 0 else 2
        torso = pg.transform.scale(torso, (torso.get_width(), torso.get_height() - drop))
        frame.blit(torso, (bounds.left, bounds.top + drop))
        frames.append(frame)
    return frames


def Drawfrostfold(screen, camera, position, elapsed, arriving):

    x, y = camera.apply(*position)
    if arriving:
        tint = (124, 188, 233)
    else:
        tint = (190, 224, 246)
    spread = max(0, min(1, elapsed))
    for ring in range(3):
        radius = max(7, round(16 + 23 * ring + spread * 39))
        pg.draw.ellipse(screen, tint, (x - radius, y - radius // 2, radius * 2, radius), 2)
    for i in range(22):
        angle = i * math.tau / 22 + spread * 1.5
        dx = math.cos(angle) * (22 + 74 * spread)
        dy = math.sin(angle) * (12 + 29 * spread)
        lift = round(spread * (i % 6) * 12)
        pg.draw.rect(screen, (200, 245, 251), (round(x + dx), round(y + dy - lift), 3, 3))
    for i in range(5):
        dx = (i - 2) * 13
        top = y - 48 - round(45 * spread) + i % 2 * 12
        pg.draw.line(screen, (141, 210, 246), (x + dx, top), (x + dx, top + 14), 2)


def Bosspixelframe(frame):

    width, height = frame.get_size()
    opacity = frame.get_alpha()
    small = pg.transform.scale(frame, (max(1, round(width / 2.5)), max(1, round(height / 2.5))))
    result = pg.transform.scale(small, (width, height))
    result.set_alpha(opacity)
    return result


def Bossposeoffset(boss):

    if boss.Teleporttime > 0:
        return 0, 0
    if boss.windup > 0:
        charge = 1 - boss.windup / boss.Winduplength
        return round(-boss.aim.x * charge * 3), round(charge * 2)
    if boss.Attackanimationtime > 0:
        progress = 1 - boss.Attackanimationtime / 0.3
        recoil = math.sin(math.pi * progress)
        return round(boss.aim.x * recoil * 4), round(-recoil * 2)
    if boss.moving:
        return 0, -round(abs(math.sin(boss.walked / 11)) * 2)
    return 0, -round((1 + math.sin(boss.Animationtime * 2.4)) * 1.2)


def Bossidleframes(ready, name):

    # Shift the upper silhouette a few pixels while keeping the lower stance fixed.
    sway, lift = {
        "Piano": (1, 2), "Guitar": (2, 1), "Flute": (1, 2),
        "Cello": (2, 1), "Harp": (1, 2), "Violin": (2, 1)
    }[name]
    bounds = ready.get_bounding_rect()
    frames = []
    for index in range(12):
        phase = index * math.tau / 12
        frame = pg.Surface((ready.get_width() + 8, ready.get_height() + 6), pg.SRCALPHA)
        for y in range(-lift, ready.get_height()):
            weight = max(0, min(1, (bounds.top + bounds.height * .76 - y) / (bounds.height * .46)))
            shift = round(math.sin(phase) * sway * weight)
            rise = round((1 - math.cos(phase)) * lift * weight / 2)
            Sourcey = y + rise
            if Sourcey >= 0:
                frame.blit(ready, (4 + shift, 6 + y), (0, Sourcey, ready.get_width(), 1))
        frames.append(frame)
    return frames
