import pygame as pg
import sys
from typing import Callable
from collections import deque 


# implement focus later.
class InfoToast:
    class Text:
        def __init__(self, text: str, text_color: tuple[int, int, int], time: float=4000, still_time=2000):
            self.surf = InfoToast.get_().font.render(text, True, text_color).convert_alpha()
            self.start_time = pg.time.get_ticks() + still_time
            self.time = time

    INSTANCE: "InfoToast" = None

    def __init__(self):
        self.text: list[InfoToast.Text] = list()
        self.padding = 5
        self.font = pg.font.SysFont("Comic Sans MS", 14)


    
    def update(self):
        i = 0

        while (i < len(self.text)):
            text = self.text[0]

            if (pg.time.get_ticks() - text.start_time > text.time):
                self.text.pop(0)
                i -= 1

            i += 1

    def draw(self, dst: pg.Surface, corner_position: tuple[int, int]):
        current_y = corner_position[1]

        for i, text in enumerate(self.text):
            size = text.surf.get_size()
            
            x = corner_position[0] - size[0]
            y = current_y - size[1]            
            
            transparent = text.surf.copy()
            opacity = max(0, min(255 - (255 * (pg.time.get_ticks() - text.start_time) / text.time), 255))


            transparent.fill((255, 255, 255, opacity), None, pg.BLEND_RGBA_MULT)
            dst.blit(transparent, (x, y))

            current_y -= (size[1] + self.padding)
        
    def _toast(self, text: str, text_color: tuple[int, int, int]=(255, 0, 0), time: float=1000):
        self.text.append(InfoToast.Text(text, text_color, time))

    @staticmethod
    def toast(*args, **kwargs):
        InfoToast.get_()._toast(*args, **kwargs)
    
    @staticmethod
    def get_() -> "InfoToast":
        if (InfoToast.INSTANCE is None):
            InfoToast.INSTANCE = InfoToast()

        return InfoToast.INSTANCE


            
def set_info_text(text: str, color: tuple[int, int, int], timeout_time=1.0):
    current_info_text = text

    
    pass

class Button():
    def __init__(self, x, y, width=50, height=20, text="Text"):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.draw_color = (255, 255, 255)
        self.text = "New Hitbox"
        
        self.on_click: Callable | None = None
        self.clked_last_frame = False

    def update(self, mouse_position: tuple[int, int]):
        mouse_inp = pg.mouse.get_pressed()

        if (mouse_position[0] > self.x and mouse_position[1] > self.y and mouse_position[0] < self.x + self.width and \
            mouse_position[1] < self.y + self.height and mouse_inp[0]):
            
            if (self.on_click is not None and not self.clked_last_frame):
                self.on_click()

            self.clked_last_frame = True
        
        else:
            self.clked_last_frame = False

    def draw(self, dst: pg.Surface):
        pg.draw.rect(dst, self.draw_color, pg.Rect(self.x, self.y, self.width, self.height))
