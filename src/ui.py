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

    

POSITION_BELOW = "position_below"
class UiElement():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

        self._posed_to: "UiElement" | None = None
        self._pos_relativity: str = ""
        self._pos_padding = 5
    def update(self, mouse_pos: tuple[int, int]):
        pass

    def draw(self, dst: pg.Surface):
        pass

def put_elem_bel(ui0: UiElement, ui1: UiElement, padding=5) -> UiElement:
    x = ui1.x
    y = ui1.y + ui1.height + padding

    ui0._posed_to = ui1
    ui0._pos_relativity = POSITION_BELOW
    ui0._pos_padding = padding

    ui0.x = x
    ui0.y = y

    return ui0

position_functions = {
    POSITION_BELOW: put_elem_bel
}

class Button(UiElement):
    BUTTON_FONT: pg.font.Font | None = None

    def __init__(self, x, y, width=50, height=20, text="Text", draw_col=(255, 255, 255), text_col=(0, 0, 0)):
        super().__init__()

        if (Button.BUTTON_FONT is None):
            Button.BUTTON_FONT = pg.font.SysFont("Comic Sans MS", 20)

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.draw_color = draw_col
        self.text_color = text_col
        self.text = text
        self.text_surf: pg.Surface = Button.BUTTON_FONT.render(self.text, True, self.text_color)

        text_surf_size = self.text_surf.get_size()

        if (text_surf_size[0] > self.width):
            self.width = text_surf_size[0] + 5

        if (text_surf_size[1] > self.height):
            self.height = text_surf_size[1] + 5

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
        dst.blit(self.text_surf, (self.x, self.y))

class TextField(UiElement):
    TEXT_FIELD_FONT = None
    def __init__(self, x, y, bg_col=(255, 255, 255), text_col=(0, 0, 0), placeholder="", shape_min: tuple[int, int]=(50, 20)):
        super().__init__()

        if (TextField.TEXT_FIELD_FONT is None):
            TextField.TEXT_FIELD_FONT = pg.font.SysFont("Arial", 17)
        
        self.x = x
        self.y = y

        self.width_min = shape_min[0]
        self.height_min = shape_min[1]
        
        self.width = self.width_min
        self.height = self.height_min

        self.bg_col = bg_col
        self.text_col = text_col
        self.plchol_col = (30, 30, 30)
        
        self.text_surf = TextField.TEXT_FIELD_FONT.render(placeholder, True, self.plchol_col)

    def update(self, mouse_pos: tuple[int, int]):
        txt_surf_size = self.text_surf.get_size()

        self.width =  max(txt_surf_size[0] + 5, self.width_min)
        self.height = max(txt_surf_size[1] + 5, self.height_min)
    
    def draw(self, dst: pg.Surface):
        pg.draw.rect(dst, self.bg_col, pg.Rect(self.x, self.y, self.width, self.height))
        print(self.x, self.y)
        dst.blit(self.text_surf, (self.x, self.y))