import pygame as pg

event_keys = []
event_mouse = []

class Mouse:
    wheel = (0, 0)
    rel = (0, 0)
    j_m_down = False
    j_m_up = False

MODE_NORMAL = "normal"
MODE_CROSSHAIR = "crosshair"

cursors = {
    MODE_NORMAL: pg.image.load("./assets/cursor.png"),
    MODE_CROSSHAIR: pg.image.load("./assets/crosshair.png")
}

current_crosshair: pg.Surface = cursors[MODE_NORMAL]

def set_cursor_mode(mode: str):
    global current_crosshair

    current_crosshair = cursors[mode]        

def update():
    event_keys.clear()

    Mouse.wheel = (0, 0)
    Mouse.rel = pg.mouse.get_rel()
    Mouse.j_m_down  = False
    Mouse.j_m_up = False

    for event in pg.event.get(pg.KEYDOWN):
        event_keys.append(event.key)

    for event in pg.event.get((pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP)):
        if (event.type == pg.MOUSEBUTTONDOWN):
            Mouse.j_m_down = True
        elif (event.type == pg.MOUSEBUTTONUP):
            Mouse.j_m_up = True


    for event in pg.event.get(pg.MOUSEWHEEL):
        Mouse.wheel = (event.x, event.y)