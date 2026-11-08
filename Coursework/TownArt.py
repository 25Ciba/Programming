import pygame as pg

ROOFS = ((144,72,66),(71,114,157),(157,99,58),(76,122,104),(133,83,66),(70,130,142),(125,74,111))


def town_house(region, style):

    sprite = pg.Surface((134, 104), pg.SRCALPHA)
    roof = ROOFS[region]
    if style % 3 == 1:
        roof = tuple(min(255,c+18) for c in roof)
    elif style % 3 == 2:
        roof = tuple(round(c*.79) for c in roof)
    shade = tuple(round(c*.73) for c in roof)
    light = tuple(min(255,c+24) for c in roof)
    ink = (48,40,48)
    wall = (186,173,152) if style % 2 == 0 else (163,152,148)
    pg.draw.polygon(sprite,(49,43,49),[(10,87),(113,88),(131,97),(110,103),(26,101)])
    pg.draw.rect(sprite,ink,(10,43,114,48))
    pg.draw.rect(sprite,wall,(13,44,108,43))
    pg.draw.rect(sprite,(130,119,115),(13,81,108,6))
    for x in (17,117):
        pg.draw.rect(sprite,(102,78,69),(x-2,48,4,37))
    if style % 3 == 0:
        peak = [(6,51),(25,16),(108,16),(128,51)]
        pg.draw.polygon(sprite,ink,peak)
        pg.draw.polygon(sprite,roof,[(9,48),(27,19),(106,19),(125,48)])
        pg.draw.line(sprite,light,(28,20),(104,20),2)
        for y in range(26,49,7):
            inset = (50-y)//2
            pg.draw.line(sprite,shade,(11+inset,y),(123-inset,y))
            for x in range(24 + (y%3)*4,116,13):
                if 11+inset < x < 123-inset:
                    pg.draw.line(sprite,shade,(x,y),(x-2,y+5))
    elif style % 3 == 1:
        pg.draw.polygon(sprite,ink,[(5,51),(6,37),(67,6),(128,37),(129,51),(67,25)])
        pg.draw.polygon(sprite,roof,[(8,48),(9,39),(67,9),(125,39),(126,48),(67,23)])
        pg.draw.polygon(sprite,shade,[(67,9),(125,39),(126,48),(67,23)])
        pg.draw.lines(sprite,light,False,[(10,39),(67,10),(124,39)],2)
        for x in range(19,63,10):
            y=39-(x-9)//2
            pg.draw.line(sprite,shade,(x,y),(x,y+11))
        for x in range(76,120,10):
            y=11+(x-67)//2
            pg.draw.line(sprite,roof,(x,y),(x,y+12))
    else:
        pg.draw.rect(sprite,ink,(6,21,122,34))
        pg.draw.rect(sprite,roof,(9,24,116,28))
        pg.draw.rect(sprite,shade,(9,45,116,7))
        pg.draw.rect(sprite,light,(13,26,108,2))
        for x in range(15,121,12):
            pg.draw.line(sprite,shade,(x,29),(x,45))
    for x in (30,95):
        pg.draw.rect(sprite,ink,(x-11,59,22,16))
        pg.draw.rect(sprite,(76,117,142),(x-9,61,18,12))
        pg.draw.rect(sprite,(137,174,182),(x-8,62,16,4))
        pg.draw.line(sprite,ink,(x,60),(x,74),1)
        pg.draw.rect(sprite,(116,89,76),(x-13,75,26,3))
    pg.draw.rect(sprite,ink,(55,59,24,31))
    pg.draw.rect(sprite,(103,72,60),(58,62,18,26))
    pg.draw.rect(sprite,(154,107,71),(59,63,16,3))
    pg.draw.rect(sprite,(199,160,95),(70,75,3,3))
    pg.draw.rect(sprite,(122,112,111),(53,89,28,4))
    if style in (1,4,7):
        pg.draw.rect(sprite,ink,(93,14,13,18))
        pg.draw.rect(sprite,(128,102,91),(95,15,9,15))
        pg.draw.rect(sprite,(171,138,115),(92,13,15,4))
    return pg.transform.scale(sprite,(268,208))


def street_prop(screen, x, y, kind, region):

    ink = (52,41,47)
    if kind == "stall":
        pg.draw.rect(screen,ink,(x-41,y-35,82,37))
        pg.draw.rect(screen,(135,93,66),(x-37,y-30,74,21))
        pg.draw.rect(screen,(188,141,91),(x-40,y-13,80,8))
        for i in range(8):
            colour = ROOFS[region] if i % 2 else (192,169,126)
            pg.draw.rect(screen,colour,(x-44+i*11,y-50,11,16))
        for i in range(4):
            pg.draw.circle(screen,(169+i*13,110+i*8,65),(x-22+i*14,y-21),4)
    elif kind == "well":
        pg.draw.ellipse(screen,ink,(x-30,y-25,60,35))
        pg.draw.ellipse(screen,(151,145,135),(x-27,y-24,54,27))
        pg.draw.ellipse(screen,(62,91,104),(x-19,y-19,38,17))
        pg.draw.line(screen,(127,174,171),(x-12,y-13),(x+9,y-13),2)
    elif kind == "garden":
        pg.draw.rect(screen,ink,(x-40,y-21,80,42))
        pg.draw.rect(screen,(111,76,56),(x-36,y-17,72,34))
        for row in range(3):
            for col in range(5):
                px,py=x-28+col*14,y-11+row*11
                pg.draw.rect(screen,(80,111,72),(px,py,6,7))
                pg.draw.rect(screen,(175,129+col*5,117),(px+2,py-2,3,3))
    elif kind == "bench":
        pg.draw.rect(screen,ink,(x-25,y-12,50,18))
        pg.draw.rect(screen,(139,94,64),(x-23,y-10,46,10))
        pg.draw.line(screen,(182,132,87),(x-21,y-7),(x+21,y-7),2)
    else:
        pg.draw.rect(screen,ink,(x-11,y-13,22,23))
        pg.draw.rect(screen,(145,103,70),(x-8,y-10,16,17))
        pg.draw.line(screen,(199,148,94),(x-8,y-8),(x+8,y+5),2)
