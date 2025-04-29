import pygame as pg

event_keys = {}
text_input = ""
event_mouse = []

class Mouse:
    wheel = (0, 0)
    rel = (0, 0)
    j_m_down = False
    j_m_up = False

MODE_NORMAL = "normal"
MODE_CROSSHAIR = "crosshair"

MOD_CTRL = 4160
MOD_NONE = 4096

cursors = {
    MODE_NORMAL: pg.image.load("./assets/cursor.png"),
    MODE_CROSSHAIR: pg.image.load("./assets/crosshair.png")
}

current_crosshair: pg.Surface = cursors[MODE_NORMAL]

def set_cursor_mode(mode: str):
    global current_crosshair

    current_crosshair = cursors[mode]        

def update():
    global text_input
    event_keys.clear()
    text_input = ""
    
    Mouse.wheel = (0, 0)
    Mouse.rel = pg.mouse.get_rel()
    Mouse.j_m_down  = False
    Mouse.j_m_up = False

    for event in pg.event.get(pg.TEXTINPUT):
        text_input = event.text

    for event in pg.event.get(pg.KEYDOWN):
        event_keys[event.key] = event.mod   

        print(event)
    for event in pg.event.get((pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP)):
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            Mouse.j_m_down = True
        elif (event.type == pg.MOUSEBUTTONUP):
            Mouse.j_m_up = True


    for event in pg.event.get(pg.MOUSEWHEEL):
        Mouse.wheel = (event.x, event.y)
