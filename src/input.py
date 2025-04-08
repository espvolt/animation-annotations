import pygame as pg

event_keys = []
mouse_wheel = (0, 0)
mouse_rel = (0, 0)

def update():
    global mouse_wheel, mouse_rel
    event_keys.clear()

    mouse_wheel = (0, 0)
    mouse_rel = pg.mouse.get_rel()
    for event in pg.event.get(pg.KEYDOWN):
        event_keys.append(event.key)

    for event in pg.event.get(pg.MOUSEWHEEL):
        mouse_wheel = (event.x, event.y)