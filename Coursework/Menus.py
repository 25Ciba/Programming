import json
from pathlib import Path
import pygame as pg

DATA = Path(__file__).resolve().parent / "Saves"
DEFAULTS = {
    "Move up":pg.K_w, "Move down":pg.K_s, "Move left":pg.K_a, "Move right":pg.K_d,
    "Dash":pg.K_SPACE, "Attack":-1, "Defend":-3, "Heal":pg.K_h,
    "Interact":pg.K_e, "Inventory":pg.K_i, "Market":pg.K_k, "Map":pg.K_m,
    "Skill 1":pg.K_1, "Skill 2":pg.K_2, "Skill 3":pg.K_3, "Skill 4":pg.K_4
}
KEYS = DEFAULTS.copy()
VOLUMES = {"Music":100, "Sound effects":100, "Ambient":100}


def Readdata(path):

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def Writedata(path, data):

    path.parent.mkdir(exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(path)


def Loadsettings():

    saved = Readdata(DATA/"settings.json")
    for action in DEFAULTS:
        value = saved.get("keys", {}).get(action, DEFAULTS[action])
        if isinstance(value, int):
            KEYS[action] = value
    for name in VOLUMES:
        value = saved.get("volumes", {}).get(name, 100)
        if isinstance(value, int):
            VOLUMES[name] = max(0, min(100, value))


def matches(event, action):

    key = KEYS[action]
    return (event.type == pg.KEYDOWN and event.key == key) or (event.type == pg.MOUSEBUTTONDOWN and event.button == -key)


def held(keys, action, alternate):

    binding = KEYS[action]
    return keys[binding] or (binding == DEFAULTS[action] and keys[alternate])


def Keyname(key):

    return {-1:"Left mouse", -2:"Middle mouse", -3:"Right mouse"}.get(key) if key < 0 else pg.key.name(key).title()


class Menus:

    def __init__(self, display, screen, frame):

        self.display, self.screen, self.frame = display, screen, frame
        self.clock = pg.time.Clock()
        self.title = pg.font.Font(None, 52)
        self.font = pg.font.Font(None, 30)
        self.small = pg.font.Font(None, 22)
        self.closed = False

    def point(self, mouse):

        if not self.frame.collidepoint(mouse):
            return (-1, -1)
        return ((mouse[0]-self.frame.x)*1200/self.frame.width, (mouse[1]-self.frame.y)*800/self.frame.height)

    def events(self):

        self.clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.closed = True
            elif event.type == pg.VIDEORESIZE:
                scale = min(event.w/1200, event.h/800)
                self.frame.size = (round(1200*scale), round(800*scale))
                self.frame.center = self.display.get_rect().center
            else:
                yield event

    def background(self, title, subtitle):

        self.screen.fill((19, 18, 22))
        pg.draw.rect(self.screen, (145, 145, 150), (34, 30, 1132, 740), 1)
        pg.draw.rect(self.screen, (62, 62, 68), (42, 38, 1116, 724), 1)
        banner = [(205, 81), (995, 81), (1022, 123), (995, 165), (205, 165), (178, 123)]
        pg.draw.lines(self.screen, (132, 132, 138), True, banner, 1)
        text = self.title.render(title, True, (234, 222, 207))
        self.screen.blit(text, text.get_rect(center=(600, 123)))
        note = self.small.render(subtitle, True, (174, 163, 169))
        self.screen.blit(note, note.get_rect(center=(600, 190)))

    def trim(self):

        for y in (56, 724):
            for x in range(150, 1040, 76):
                pg.draw.lines(self.screen, (88, 77, 84), True, [(x, y+9), (x+13, y), (x+43, y), (x+30, y+9)], 1)

    def present(self):

        self.display.fill((0, 0, 0))
        self.display.blit(pg.transform.scale(self.screen, self.frame.size), self.frame)
        pg.display.flip()

    def choose(self, title, options, subtitle="", illustration=False):

        selected = 0
        rows = [pg.Rect(340, 225+i*56, 520, 45) for i in range(len(options))]
        if illustration:
            rows = [pg.Rect(340+i%2*280, 310+i//2*133, 240, 72) for i in range(len(options))]
        elif title == "Fragment Selection":
            rows = [pg.Rect(370+i%2*290, 278+i//2*105, 215, 57) for i in range(len(options))]
        elif title == "Character Selection":
            rows = [pg.Rect(440, 295+i*153, 250, 60) for i in range(len(options))]
        decorated = title in ("Game Saves", "Save Game", "Fragment Selection", "Character Selection")
        while not self.closed:
            self.background(title, subtitle)
            if decorated:
                self.trim()
            mouse = self.point(pg.mouse.get_pos())
            for i, (name, row) in enumerate(zip(options, rows)):
                active = i==selected or row.collidepoint(mouse)
                pg.draw.rect(self.screen, (25, 39, 64) if active else (23, 21, 26), row, border_radius=8)
                pg.draw.rect(self.screen, (163, 168, 179) if active else (110, 110, 115), row, 1, border_radius=8)
                text = self.font.render(name, True, (239, 223, 203))
                self.screen.blit(text, text.get_rect(center=row.center))
                if decorated:
                    x, y = row.x-36, row.centery
                    pg.draw.lines(self.screen, (163, 168, 179) if active else (110, 110, 115), True, [(x-15, y), (x, y-15), (x+15, y), (x, y+15)], 1)
            self.present()
            for event in self.events():
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_ESCAPE:
                        return None
                    if event.key in (pg.K_UP, pg.K_DOWN):
                        selected=(selected+(1 if event.key==pg.K_DOWN else -1))%len(rows)
                    if event.key==pg.K_RETURN:
                        return selected
                if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                    for i, row in enumerate(rows):
                        if row.collidepoint(self.point(event.pos)):
                            return i
        return None

    def settings(self):

        self.controls()
        Writedata(DATA/"settings.json", {"keys":KEYS, "volumes":VOLUMES})

    def volume(self):

        bars = [pg.Rect(365, 237+i*76, 385, 18) for i in range(3)]
        dragging = None
        selected = 0
        names = list(VOLUMES)
        while not self.closed:
            self.background("Volume", "This build is silent. These levels are saved for when audio is added.")
            for i, (name, bar) in enumerate(zip(names, bars)):
                self.screen.blit(self.font.render(name, True, (230, 214, 199)), (145, bar.y-4))
                pg.draw.rect(self.screen, (53, 44, 59), bar)
                pg.draw.rect(self.screen, (138, 104, 83), (bar.x, bar.y, bar.width*VOLUMES[name]//100, bar.height))
                x = bar.x + bar.width*VOLUMES[name]//100
                pg.draw.rect(self.screen, (235, 204, 157), (x-4, bar.y-4, 8, 26))
                if i==selected:
                    pg.draw.rect(self.screen, (165, 128, 96), bar.inflate(14, 18), 1)
                self.screen.blit(self.small.render(f"{VOLUMES[name]}%", True, (224, 207, 187)), (bar.right+20, bar.y))
            self.screen.blit(self.small.render("Drag the sliders or use arrows. Esc to return.", True, (181, 162, 177)), (145, 500))
            self.present()
            for event in self.events():
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_ESCAPE:
                        return
                    if event.key in (pg.K_UP, pg.K_DOWN):
                        selected=(selected+(1 if event.key==pg.K_DOWN else -1))%3
                    if event.key in (pg.K_LEFT, pg.K_RIGHT):
                        name=names[selected]
                        VOLUMES[name]=max(0, min(100, VOLUMES[name]+(5 if event.key==pg.K_RIGHT else -5)))
                if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                    point=self.point(event.pos)
                    dragging=next((i for i, bar in enumerate(bars) if bar.inflate(14, 18).collidepoint(point)), None)
                    if dragging is not None:
                        selected=dragging
                elif event.type==pg.MOUSEBUTTONUP and event.button==1:
                    dragging=None
                if dragging is not None and event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION):
                    bar=bars[dragging]
                    VOLUMES[names[dragging]]=max(0, min(100, round((self.point(event.pos)[0]-bar.x)*100/bar.width)))

    def controls(self):

        actions=list(KEYS)
        rows=[pg.Rect(100+(i//6)*246, 266+(i%6)*43, 230, 36) for i in range(12)]
        rows.extend(pg.Rect(100+(i//2)*246, 565+(i%2)*43, 230, 36) for i in range(4))
        bars=[pg.Rect(682, 294+i*108, 342, 16) for i in range(3)]
        reset=pg.Rect(100, 676, 190, 34)
        selected=None
        dragging=None
        notice=""
        while not self.closed:
            self.background("General Settings", "Click a key to rebind it, or drag a volume slider. Esc returns.")
            for text, x, y in [("Basic Info", 100, 232), ("Skills", 100, 531), ("Audio", 682, 232)]:
                self.screen.blit(self.font.render(text, True, (221, 199, 177)), (x, y))
            for (name, value), bar in zip(VOLUMES.items(), bars):
                self.screen.blit(self.small.render(name, True, (221, 199, 177)), (bar.x, bar.y-26))
                pg.draw.rect(self.screen, (92, 81, 89), bar, 1)
                pg.draw.rect(self.screen, (31, 53, 86), (bar.x+2, bar.y+2, round((bar.width-4)*value/100), bar.height-4))
                knob=bar.x+round(bar.width*value/100)
                pg.draw.rect(self.screen, (163, 168, 179), (knob-3, bar.y-3, 6, 22))
                self.screen.blit(self.small.render(f"{value}%", True, (210, 190, 172)), (bar.right+12, bar.y))
            self.screen.blit(self.small.render("Audio is silent in this build.", True, (165, 146, 155)), (682, 590))
            for action, row in zip(actions, rows):
                pg.draw.rect(self.screen, (25, 39, 64) if selected==action else (29, 24, 38), row)
                self.screen.blit(self.small.render(action, True, (233, 217, 203)), (row.x+12, row.y+13))
                label=self.small.render("Press a key" if selected==action else Keyname(KEYS[action]), True, (220, 177, 119))
                self.screen.blit(label, label.get_rect(midright=(row.right-11, row.centery)))
            pg.draw.rect(self.screen, (57, 43, 57), reset)
            self.screen.blit(self.small.render("Reset defaults", True, (233, 217, 203)), (reset.x+12, reset.y+12))
            self.screen.blit(self.small.render(notice, True, (224, 164, 137)), (310, 686))
            self.present()
            for event in self.events():
                if event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:
                    if selected:
                        selected=None
                        continue
                    return
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    dragging = None
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not selected:
                    dragging = next((i for i, bar in enumerate(bars) if bar.inflate(16, 16).collidepoint(self.point(event.pos))), None)
                if dragging is not None and event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION):
                    bar = bars[dragging]
                    VOLUMES[list(VOLUMES)[dragging]] = max(0, min(100, round((self.point(event.pos)[0]-bar.x)*100/bar.width)))
                    continue
                if selected and event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    if event.type==pg.KEYDOWN:
                        value = event.key
                    else:
                        value = -event.button
                    if value in (pg.K_F3, pg.K_F4, pg.K_F8, pg.K_F11) or (value<0 and (selected not in ("Attack", "Defend") or value not in (-1, -2, -3))):
                        notice="That input is reserved."
                        continue
                    other=next((a for a, k in KEYS.items() if k==value and a!=selected), None)
                    if other:
                        notice=f"Already assigned to {other}."
                        continue
                    KEYS[selected]=value
                    selected=None
                    notice="Control updated."
                elif event.type==pg.MOUSEBUTTONDOWN and event.button==1:
                    point=self.point(event.pos)
                    if reset.collidepoint(point):
                        KEYS.update(DEFAULTS)
                        notice="Defaults restored."
                    else:
                        selected=next((action for action, row in zip(actions, rows) if row.collidepoint(point)), None)
