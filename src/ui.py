import pygame as pg

class Button():
    def __init__(self, x, y, width=50, height=20, text="Text"):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.draw_color = (255, 255, 255)
        self.text = "New Hitbox"

    def draw(self, dst: pg.Surface):
        pg.draw.rect(dst, self.draw_color, pg.Rect(self.x, self.y, self.width, self.height))
