import pygame as pg

event_keys = []
mouse_wheel = (0, 0)
mouse_rel = (0, 0)

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
    global mouse_wheel, mouse_rel
    event_keys.clear()

    mouse_wheel = (0, 0)
    mouse_rel = pg.mouse.get_rel()
    for event in pg.event.get(pg.KEYDOWN):
        event_keys.append(event.key)

    for event in pg.event.get(pg.MOUSEWHEEL):
        mouse_wheel = (event.x, event.y)