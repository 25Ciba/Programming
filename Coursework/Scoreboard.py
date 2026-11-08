import pygame as pg
from Menus import DATA, read_data, write_data


def record_score(score):

    save_file = DATA/"records.json"
    top_score = read_data(save_file).get("top_score",0)
    new_record = score > top_score
    if new_record:
        top_score = score
        write_data(save_file,{"top_score":top_score})
    return top_score,new_record


def draw_scoreboard(screen, progress, top_score, new_record, top=254):

    title_font = pg.font.Font(None,26)
    font = pg.font.Font(None,24)
    minutes,seconds = divmod(int(progress["time_survived"]),60)
    entries = [
        ("Score",progress["score"]),("Top score",top_score),
        ("Coins",progress["coins"]),("Time survived",f"{minutes}:{seconds:02}"),
        ("Areas cleared",progress["areas_cleared"]),("Level",progress["level"]),
        ("Enemies felled",progress["enemies_felled"]),("Items collected",progress["items_collected"]),
        ("Damage dealt",progress["damage_dealt"]),("Damage taken",progress["damage_taken"]),
        ("Highest hit",progress["highest_hit"])
    ]
    for index,(label,value) in enumerate(entries):
        rect = pg.Rect(150+index%2*455,top+index//2*45,445,38)
        pg.draw.rect(screen,(26,31,43),rect)
        pg.draw.rect(screen,(96,96,106),rect,1)
        screen.blit(font.render(label,True,(220,208,203)),(rect.x+12,rect.y+10))
        amount=font.render(str(value),True,(238,214,168))
        screen.blit(amount,amount.get_rect(midright=(rect.right-12,rect.centery)))
    if new_record:
        pulse=(pg.time.get_ticks()//180)%4
        label=title_font.render("New top score",True,(228+pulse*7,184+pulse*9,123+pulse*10))
        screen.blit(label,label.get_rect(center=(600,top-25)))


def show_scoreboard(menus, progress):

    top_score,new_record=record_score(progress["score"])
    button=pg.Rect(440,621,320,54)
    while not menus.closed:
        menus.background("Run Summary","Your results for this playthrough.")
        draw_scoreboard(menus.screen,progress,top_score,new_record)
        pg.draw.rect(menus.screen,(25,39,64),button,border_radius=6)
        pg.draw.rect(menus.screen,(145,145,151),button,1,border_radius=6)
        label=menus.font.render("Return to Main Menu",True,(232,217,199))
        menus.screen.blit(label,label.get_rect(center=button.center))
        menus.present()
        for event in menus.events():
            if event.type==pg.KEYDOWN and event.key in (pg.K_RETURN,pg.K_ESCAPE):
                return
            if event.type==pg.MOUSEBUTTONDOWN and event.button==1 and button.collidepoint(menus.point(event.pos)):
                return
