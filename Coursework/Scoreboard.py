import pygame as pg
from Menus import DATA, Readdata, Writedata


def Recordscore(score):

    Savefile = DATA/"records.json"
    Topscore = Readdata(Savefile).get("top_score", 0)
    Newrecord = score > Topscore
    if Newrecord:
        Topscore = score
        Writedata(Savefile, {"top_score":Topscore})
    return Topscore, Newrecord


def Drawscoreboard(screen, progress, Topscore, Newrecord, top=254):

    Titlefont = pg.font.Font(None, 26)
    font = pg.font.Font(None, 24)
    minutes, seconds = divmod(int(progress.Timesurvived), 60)
    entries = [
        ("Score", progress.score), ("Top score", Topscore),
        ("Coins", progress.coins), ("Time survived", f"{minutes}:{seconds:02}"),
        ("Areas cleared", progress.Areascleared), ("Level", progress.level),
        ("Enemies felled", progress.Enemiesfelled), ("Items collected", progress.Itemscollected),
        ("Damage dealt", progress.Damagedealt), ("Damage taken", progress.Damagetaken),
        ("Highest hit", progress.Highesthit)
    ]
    for index, (label, value) in enumerate(entries):
        rect = pg.Rect(150+index%2*455, top+index//2*45, 445, 38)
        pg.draw.rect(screen, (26, 31, 43), rect)
        pg.draw.rect(screen, (96, 96, 106), rect, 1)
        screen.blit(font.render(label, True, (220, 208, 203)), (rect.x+12, rect.y+10))
        amount=font.render(str(value), True, (238, 214, 168))
        screen.blit(amount, amount.get_rect(midright=(rect.right-12, rect.centery)))
    if Newrecord:
        pulse=(pg.time.get_ticks()//180)%4
        label=Titlefont.render("New top score", True, (228+pulse*7, 184+pulse*9, 123+pulse*10))
        screen.blit(label, label.get_rect(center=(600, top-25)))


def Showscoreboard(menus, progress):

    Topscore, Newrecord=Recordscore(progress.score)
    button=pg.Rect(440, 621, 320, 54)
    while not menus.closed:
        menus.background("Run Summary", "Your results for this playthrough.")
        Drawscoreboard(menus.screen, progress, Topscore, Newrecord)
        pg.draw.rect(menus.screen, (25, 39, 64), button, border_radius=6)
        pg.draw.rect(menus.screen, (145, 145, 151), button, 1, border_radius=6)
        label=menus.font.render("Return to Main Menu", True, (232, 217, 199))
        menus.screen.blit(label, label.get_rect(center=button.center))
        menus.present()
        for event in menus.events():
            if event.type==pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_ESCAPE):
                return
            if event.type==pg.MOUSEBUTTONDOWN and event.button==1 and button.collidepoint(menus.point(event.pos)):
                return
