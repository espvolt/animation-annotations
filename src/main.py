import pygame as pg

import config
from animation_panel import AnimationPanel
import input

pg.init()
display = pg.display.set_mode(config.SCREEN_SIZE)

running = True

animation_panel = AnimationPanel()
animation_panel.load_animation("./test/FreeKnight_v1/Colour1/NoOutline/120x80_PNGSheets/_Attack.png")

while (running):
    display.fill(config.CLEAR_COLOR)

    for event in pg.event.get(pg.QUIT):
        if (event.type == pg.QUIT):
            running = False
    
    input.update()

    animation_panel.update()
    animation_panel.draw(display)

    pg.display.flip()