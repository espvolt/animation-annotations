import pygame as pg

clock = pg.time.Clock()

class Dt:
    millis = 0
    _last_millis = pg.time.get_ticks()

def update():
    Dt.millis = 1 / (pg.time.get_ticks() - Dt._last_millis)
    Dt._last_millis = pg.time.get_ticks()