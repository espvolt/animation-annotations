import pygame as pg

import config
from animation_panel import AnimationPanel
import input
import ui
import shared

pg.init()
pg.mouse.set_visible(False)

display = pg.display.set_mode(config.SCREEN_SIZE, pg.SRCALPHA)

running = True

animation_panel = AnimationPanel()
animation_panel.load_animation("./test/FreeKnight_v1/Colour1/NoOutline/120x80_PNGSheets/_Attack.png")

toast_instance = ui.InfoToast.get_()

while (running):
    display.fill(config.CLEAR_COLOR)

    for event in pg.event.get(pg.QUIT):
        if (event.type == pg.QUIT):
            running = False

    shared.update()    
    input.update()
    toast_instance.update()


    animation_panel.update()
    animation_panel.draw(display)
    
    toast_instance.draw(display, config.SCREEN_SIZE)
    display.blit(input.current_crosshair, pg.mouse.get_pos())

    pg.display.flip()