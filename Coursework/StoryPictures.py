import pygame as pg


def Storypicture(page):

    image = pg.Surface((108, 108))
    night = (9, 7, 14)
    image.fill(night)
    gold = (240, 184, 92)
    stone = (95, 103, 125)
    if page == 0:
        pg.draw.circle(image, (251, 194, 117), (80, 24), 12)
        pg.draw.polygon(image, (55, 94, 81), [(8, 76), (28, 48), (49, 62), (70, 44), (101, 76)])
        pg.draw.polygon(image, (82, 132, 93), [(8, 76), (33, 62), (52, 73), (79, 59), (101, 76), (101, 94), (8, 94)])
        pg.draw.lines(image, (201, 158, 102), False, [(49, 94), (47, 87), (66, 75), (67, 64)], 3)
        for x, y, roof in [(24, 70, (194, 83, 70)), (72, 61, (91, 142, 192)), (84, 73, (203, 116, 73))]:
            pg.draw.rect(image, (230, 205, 157), (x, y, 11, 8))
            pg.draw.polygon(image, roof, [(x-2, y), (x+5, y-6), (x+12, y)])
            pg.draw.rect(image, (81, 53, 62), (x+4, y+3, 3, 5))
        for x, y in [(42, 85), (52, 84), (59, 78), (65, 72), (68, 69), (67, 63)]:
            pg.draw.rect(image, gold, (x, y, 2, 2))
    elif page == 1:
        for x in (18, 85):
            pg.draw.rect(image, stone, (x, 40, 5, 42))
            pg.draw.rect(image, (139, 145, 159), (x-2, 37, 9, 4))
        pg.draw.lines(image, (106, 114, 145), False, [(20, 40), (29, 25), (44, 18), (65, 18), (81, 27), (87, 40)], 4)
        pg.draw.rect(image, (69, 61, 90), (27, 83, 54, 5))
        pg.draw.rect(image, stone, (34, 77, 40, 6))
        pg.draw.rect(image, (176, 136, 100), (42, 69, 24, 9))
        pg.draw.lines(image, gold, True, [(44, 64), (50, 34), (67, 42), (63, 62)], 3)
        for x in (50, 54, 58):
            pg.draw.line(image, (255, 226, 148), (x, 61), (x+4, 42))
        for x, y in [(37, 47), (72, 35), (75, 60), (47, 23), (64, 29)]:
            pg.draw.rect(image, (255, 226, 148), (x, y, 2, 2))
    elif page == 2:
        colours = [(123, 192, 241), (244, 126, 83), (140, 219, 142), (241, 177, 93), (88, 207, 190), (216, 132, 210)]
        for index, (x, y) in enumerate([(22, 42), (39, 28), (67, 27), (85, 43), (76, 66), (29, 65)]):
            colour = colours[index]
            pg.draw.polygon(image, colour, [(x, y-6), (x+5, y-1), (x+2, y+7), (x-5, y+3)])
            pg.draw.line(image, (254, 230, 185), (x, y-4), (x-2, y+3))
        pg.draw.lines(image, gold, False, [(47, 74), (40, 80), (58, 84), (66, 76), (61, 69)], 3)
        pg.draw.lines(image, (189, 127, 64), False, [(49, 70), (51, 61), (57, 65), (60, 57)], 3)
        pg.draw.rect(image, (145, 189, 220), (47, 89, 15, 10))
        pg.draw.lines(image, (66, 100, 149), False, [(49, 96), (54, 91), (59, 96)])
    else:
        pg.draw.polygon(image, (51, 64, 91), [(24, 85), (24, 41), (36, 25), (53, 18), (71, 25), (83, 41), (83, 85)])
        pg.draw.polygon(image, (24, 31, 54), [(32, 85), (32, 43), (41, 31), (53, 25), (66, 31), (75, 43), (75, 85)])
        pg.draw.line(image, stone, (25, 44), (25, 82), 2)
        pg.draw.line(image, stone, (82, 44), (82, 82), 2)
        for x in (22, 83):
            pg.draw.rect(image, gold, (x, 63, 4, 6))
        pg.draw.polygon(image, (111, 74, 152), [(45, 81), (45, 72), (50, 67), (56, 67), (61, 73), (61, 82), (64, 90), (43, 90)])
        pg.draw.rect(image, (41, 29, 63), (51, 74, 10, 6))
        pg.draw.rect(image, (144, 219, 225), (58, 76, 2, 2))
        pg.draw.rect(image, (76, 49, 109), (46, 90, 6, 4))
        pg.draw.rect(image, (76, 49, 109), (56, 90, 6, 4))
    return pg.transform.scale(image, (432, 432))
