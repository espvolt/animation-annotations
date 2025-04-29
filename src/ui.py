import pygame as pg
import sys
import input
from typing import Callable
from collections import deque 
from shared import Dt
import tupmath
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

def rounded_border(surf: pg.Surface, radius: float, col: tuple[int, int, int]):
    surf_size = surf.get_size()
    pg.draw.rect(surf, col, pg.Rect(0, 0, surf_size[0], surf_size[1]), border_radius=radius)

def set_info_text(text: str, color: tuple[int, int, int], timeout_time=1.0):
    current_info_text = text

    

POSITION_BELOW = "position_below"

TEXT_ALIGN_LEFT = "text_align_left"
TEXT_ALIGN_RIGHT = "text_align_right"
TEXT_ALIGN_CENTER = "text_align_center"

class UiElement():
    ID_COUNT = 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.z_ind = 0

        self.hidden = False

        self._posed_to: "UiElement" | None = None
        self._pos_relativity: str = ""
        self._pos_padding = 5

        self.id = UiElement.ID_COUNT
        UiElement.ID_COUNT += 1

    def handle_click(self, mouse_pos: tuple[int, int], buttons: tuple[bool, bool, bool]) -> bool:
        # True for takes focus, false for pass through
        return False

    def update(self, mouse_pos: tuple[int, int]):
        pass

    def draw(self, dst: pg.Surface):
        pass

class CurrentUiState:
    curr_focus: UiElement | None = None


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

    def __init__(self, x, y, width=200, height=60, text="Text", draw_col=(255, 255, 255), text_col=(0, 0, 0)):
        super().__init__()

        if (Button.BUTTON_FONT is None):
            Button.BUTTON_FONT = pg.font.SysFont("Comic Sans MS", 20)

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.draw_color = draw_col
        self.bg_col = draw_col
        self.hov_col = (0, 0, 0)


        self.txt_draw_col = text_col
        self.text_col = text_col
        self.txt_hov_col = (255, 255, 255)

        self.hover_val = 0.0

        self.text = text
        self.text_surf: pg.Surface = Button.BUTTON_FONT.render(self.text, True, self.txt_draw_col)
        self.text_align = TEXT_ALIGN_CENTER

        text_surf_size = self.text_surf.get_size()

        if (text_surf_size[0] > self.width):
            self.width = text_surf_size[0] + 5

        if (text_surf_size[1] > self.height):
            self.height = text_surf_size[1] + 5

        self.on_click: Callable | None = None

    def update(self, mouse_pos: tuple[int, int]):
        if (tupmath.pinrect(mouse_pos, (self.x, self.y, self.width, self.height))):
            self.hover_val = min(1, self.hover_val + (1 * Dt.millis))

        else:
            self.hover_val = max(0, self.hover_val - (1 * Dt.millis))

        self.draw_color = tupmath.lerp_3(self.bg_col, self.hov_col, self.hover_val)
        self.txt_draw_col = tupmath.lerp_3(self.text_col, self.txt_hov_col, self.hover_val)

        self.text_surf: pg.Surface = Button.BUTTON_FONT.render(self.text, True, self.txt_draw_col)

    def handle_click(self, mouse_pos: tuple[int, int], buttons: tuple[bool, bool, bool]) -> bool:
        mouse_inp = pg.mouse.get_pressed()

        if (mouse_pos[0] > self.x and mouse_pos[1] > self.y and mouse_pos[0] < self.x + self.width and \
            mouse_pos[1] < self.y + self.height and mouse_inp[0]):
            
            if (self.on_click is not None):
                self.on_click()
                return True
            
        return False
    
    def draw(self, dst: pg.Surface):
        pg.draw.rect(dst, self.draw_color, pg.Rect(self.x, self.y, self.width, self.height), border_radius=40)
        
        txt_size = self.text_surf.get_size()

        dst_x = self.x
        dst_y = self.y + self.height / 2 - txt_size[1] / 2

        if (self.text_align == TEXT_ALIGN_CENTER):

            dst_x = self.x + self.width / 2 - txt_size[0] / 2

        elif (self.text_align == TEXT_ALIGN_RIGHT):
            dst_x = self.x + self.width - txt_size[0]

        dst.blit(self.text_surf, (dst_x, dst_y))

class TextField(UiElement):
    TEXT_FIELD_FONT = None
    CURSOR_BLINK_TIME = 500

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
        
        self.placeholder = placeholder
        self.text_surf: pg.Surface | None = None
        
        self.curr_text: list[str] = []
        self.curr_pos = 0
        
        self.on_text_changed: Callable | None = None

        self.cursor_showing = False
        self.cursor_col = (0, 0, 0)

        self.last_millis = pg.time.get_ticks()

        self._render_curr_text()

    def handle_click(self, mouse_pos: tuple[int, int], buttons: tuple[bool, bool, bool]) -> bool:
        if (mouse_pos[0] > self.x and mouse_pos[1] > self.y 
            and mouse_pos[0] < self.x + self.width and mouse_pos[1] < self.y + self.height and buttons[0]):
            return True
    
    def _render_curr_text(self):
        if (self.curr_text == ""):
            self.text_surf = TextField.TEXT_FIELD_FONT.render(self.placeholder, True, self.plchol_col)
        else:
            self.text_surf = TextField.TEXT_FIELD_FONT.render("".join(self.curr_text), True, self.text_col)

    def update(self, mouse_pos: tuple[int, int]):
        if (CurrentUiState.curr_focus == self):
            if (pg.time.get_ticks() - self.last_millis > TextField.CURSOR_BLINK_TIME):
                self.cursor_showing = not self.cursor_showing
                self.last_millis = pg.time.get_ticks()
        else:
            self.cursor_showing = False

        txt_surf_size = self.text_surf.get_size()

        self.width =  max(txt_surf_size[0] + 5, self.width_min)
        self.height = max(txt_surf_size[1] + 5, self.height_min)

        curr_foc = CurrentUiState.curr_focus
        
        if (curr_foc is not None and curr_foc.id == self.id):
            text_changed = False

            if (input.text_input != ""):
                self.curr_text.insert(self.curr_pos, input.text_input)
                self.curr_pos += len(input.text_input)

                text_changed = True

            if (pg.K_BACKSPACE in input.event_keys and len(self.curr_text) != 0 and self.curr_pos > 0):
                self.curr_text.pop(self.curr_pos - 1)
                self.curr_pos -= 1
                text_changed = True

            if (pg.K_LEFT in input.event_keys):
                self.curr_pos = max(0, self.curr_pos - 1)

            if (pg.K_RIGHT in input.event_keys):
                self.curr_pos = min(len(self.curr_text), self.curr_pos + 1)
        
            if (text_changed):
                self._render_curr_text()
                
                if (self.on_text_changed is not None):
                    self.on_text_changed()

            
    def draw(self, dst: pg.Surface):
        pg.draw.rect(dst, self.bg_col, pg.Rect(self.x, self.y, self.width, self.height))
        dst.blit(self.text_surf, (self.x, self.y))
        
        if (self.cursor_showing):
            metrics = TextField.TEXT_FIELD_FONT.size("".join(self.curr_text[:self.curr_pos]))

            cursor_x = metrics[0] + 3
                # print(metrics)
                # cursor_x += metrics[len(metrics) - 1][3]
            
            pg.draw.rect(dst, self.cursor_col, pg.Rect(cursor_x, self.y + 2, 2, self.height - 2))
        
class ComboBox(UiElement):
    def __init__(self, x, y, starting_options: list[str]=[]):
        super().__init__()

        self.x = x
        self.y = y
        
        self.placeholder_col = (30, 30, 30)
        self.main_col = (0, 0, 0)
        self.bg_col = (255, 255, 255)
        self.dd_main_col = (20, 20, 20)
        self.dd_bg_col = (255, 255, 255)

        self.box_dropped = False
        
        self.height = 20
        self.min_width = 100

        self.curr_sel: str | None = None
        
        self.options: dict[str, pg.Surface] = {}

        self.sel_surf: pg.Surface = None
        self.dd_bg_surf: pg.Surface = None
        self.render_selected(None)

        self.sel_h = self.sel_surf.get_size()[1]
        self.box_h = self.sel_surf.get_size()[1]

        self.box_surf: pg.Surface = pg.Surface((self.min_width, self.box_h))
        self.box_surf.fill(self.bg_col)
        self.width = self.min_width

        self.on_option_changed: Callable | None = None

        for option in starting_options:
            self.add_option(option)

    def add_option(self, text: str):
        self.options[text] = Button.BUTTON_FONT.render(text, True, self.dd_main_col, self.dd_bg_col)
        max_w = self.width

        for val in self.options.values():
            max_w = max(max_w, val.get_size()[0])

        self.dd_bg_surf = pg.Surface((max_w, self.box_h * len(self.options)))
        self.dd_bg_surf.fill(self.dd_bg_col)

    def render_selected(self, text: str | None):
        if (text is None):
            self.sel_surf = Button.BUTTON_FONT.render("Placeholder", True, self.placeholder_col, self.bg_col)
        
        else:
            self.sel_surf = Button.BUTTON_FONT.render(text, True, self.placeholder_col, self.bg_col)

    def handle_click(self, mouse_pos, buttons):
        if (not buttons[0]):
            return False
        
        if (self.box_dropped):
            for i, s in enumerate(self.options.keys()):
                if (tupmath.pinrect(mouse_pos, (self.x, self.y + self.box_h * (i + 1), self.width, self.box_h))):
                    self.render_selected(s)

                    if (self.on_option_changed is not None):
                        self.on_option_changed(s)
                    
                    self.box_dropped = False
                    return True
                
        if (tupmath.pinrect(mouse_pos, (self.x, self.y, self.width, self.height)) and buttons[0]):
            self.box_dropped = not self.box_dropped

            return True
        
    def update(self, mouse_pos):
        if (self.box_dropped): # height should change
            add_h = len(self.options) * self.box_h
            self.height = self.box_h + add_h
        
        else:            
            self.height = self.box_surf.get_size()[1]

        self.width = max(self.min_width, self.sel_surf.get_size()[0])
        
        return super().update(mouse_pos)
    
    def draw(self, dst: pg.Surface):
        dst.blit(self.box_surf, (self.x, self.y))

        if (self.sel_surf is not None):
            dst.blit(self.sel_surf, (self.x, self.y))

        if (self.box_dropped and len(self.options) != 0):
            y_off = (self.y + self.box_h)
            
            if (self.dd_bg_surf is not None):
                dst.blit(self.dd_bg_surf, (self.x, y_off))

            for i, option_surf in enumerate(self.options.values()):
                dst.blit(option_surf, (self.x, self.y + self.box_h * (i + 1)))
