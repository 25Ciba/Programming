import math
import pygame as pg


def familiar_frame(index, attack=False):

    frame = pg.Surface((46, 38), pg.SRCALPHA)
    phase = index * math.tau / 8
    lift = round(math.sin(phase) * 2)
    lunge = (0, -2, -3, 2, 7, 5, 2, 0)[index] if attack else 0
    x, y = 20 + lunge, 22 - lift
    ink, shade, mid, rim = (25, 32, 45), (48, 78, 76), (89, 146, 121), (151, 195, 150)
    pg.draw.polygon(frame, ink, [(x-11,y+5),(x-18,y+2),(x-19,y-4),(x-15,y-1),(x-11,y-2),(x-9,y-7),(x-11,y-15),(x-4,y-11),(x+3,y-12),(x+9,y-16),(x+10,y-8),(x+13,y-4),(x+14,y+2),(x+10,y+6),(x-7,y+8)])
    pg.draw.polygon(frame, shade, [(x-11,y+4),(x-17,y+1),(x-13,y+1),(x-9,y-5),(x-7,y-8),(x+7,y-9),(x+11,y-4),(x+12,y+2),(x+9,y+5),(x-6,y+7)])
    pg.draw.polygon(frame, mid, [(x-7,y-5),(x-7,y-11),(x-3,y-8),(x+4,y-9),(x+8,y-12),(x+8,y-7),(x+11,y-3),(x+8,y+2),(x+1,y+3),(x-5,y+1)])
    pg.draw.line(frame, rim, (x-4,y-6),(x+6,y-7))
    pg.draw.rect(frame, (242, 218, 147), (x+2,y-3,3,2))
    pg.draw.rect(frame, (242, 218, 147), (x+8,y-3,2,2))
    pg.draw.rect(frame, ink, (x-6,y+5,5,4))
    pg.draw.rect(frame, ink, (x+6,y+4,6,4))
    if attack and 3 <= index <= 5:
        pg.draw.lines(frame, (202, 232, 178), False, [(x+6,y+2),(x+12,y+3),(x+15,y-1)], 2)
    return pg.transform.scale(frame, (92, 76))


class FamiliarArt:

    def __init__(self):

        self.idle = [familiar_frame(i) for i in range(8)]
        self.attack = [familiar_frame(i, True) for i in range(8)]

    def render(self, screen, point, elapsed, attack, facing):

        frames = self.attack if attack else self.idle
        index = min(7,int((.30-attack)*8/.30)) if attack else int(elapsed*12)%8
        frame = frames[index]
        if facing < 0:
            frame = pg.transform.flip(frame,True,False)
        x,y = point
        pg.draw.ellipse(screen,(26,24,38),(x-18,y-4,36,11))
        screen.blit(frame,frame.get_rect(midbottom=(x,y+17)))

    def vanish(self, screen, point, progress, sacrifice):

        x,y = point
        frame = self.idle[0].copy()
        frame.set_alpha(round(255*(1-progress)))
        screen.blit(frame,frame.get_rect(midbottom=(x,y+17-round(progress*21))))
        count = 14 if sacrifice else 7
        for index in range(count):
            angle = index*math.tau/count
            radius = 9 + progress*(55 if sacrifice else 25)
            px = x + math.cos(angle)*radius
            py = y-23 + math.sin(angle)*radius*.6 - progress*15
            shade = round(80*(1-progress))
            colour = (168+shade,135+shade,86+shade) if sacrifice else (75+shade,124+shade,112+shade)
            pg.draw.rect(screen,colour,(round(px),round(py),3,3))
