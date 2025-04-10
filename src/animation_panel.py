import pygame as pg
import config
import tupmath
from PIL import Image
import ui
import input

FORMAT_HORIZONTAL = "horizontal"
FORMAT_VERTICAL = "vertical"
FORMAT_GIF = "gif"

MODE_NOTHING = "nothing"
MODE_HITBOX = "hitbox"

def _pil2pg(img: Image):
    return pg.image.fromstring(
        img.tobytes(), img.size, img.mode).convert_alpha()


class Hitbox():
    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y

        self.x2 = x2
        self.y2 = y2

        self.draw_color = (255, 0, 0, 255 / 2)
        self.surf = pg.Surface((1, 1), pg.SRCALPHA)

        self.surf.fill(self.draw_color)

class AnimationFrame():
    def __init__(self, surf: pg.Surface):
        self.hitboxes: list[Hitbox] = []
        self.surf = surf

class AnimationFrames():
    def __init__(self, src: str, is_gif=False):
        if (is_gif):
            return
        
        self.src = src
        self.frames = self._load_image_frames(n_frames=4)

    def _load_image_frames(self, n_frames=1, horiz=True):
        res: list[AnimationFrame] = []

        image = Image.open(self.src)
        img_alpha = image.convert("RGBA")
        step = 0

        if (horiz):
            step = image.width / n_frames
        else:
            step = image.height / n_frames

        for i in range(n_frames):
            if (horiz):
                crop_rect = (i * step, 0, (i + 1) * step, image.height)
                surface = _pil2pg(img_alpha.crop(crop_rect))
                res.append(AnimationFrame(surface))
            # TODO vertical

        image.close()
        return res
    

class AnimationPanel():
    def __init__(self):
        self.curr_split = .6

        self.anim_surf = pg.Surface((config.SCREEN_SIZE[0] * self.curr_split, config.SCREEN_SIZE[1]), pg.SRCALPHA)
        self.anim_bg_surf: pg.Surface | None = None

        self.animation_src: str = ""
        self.animation_offset: int = -1 # for flipbook animations
        self.animation_format: str = ""
        self.curr_disp_frame = 0
        self.curr_frames_obj: AnimationFrames | None = None
        
        self.zoom = 1
        
        self.cam_x = 0
        self.cam_y = 0

        self.paused = False

        self.fps = 1
        self.time_millis = pg.time.get_ticks()
        self.last_time_millis = self.time_millis

        # panel stuff
        self.panel_surf = pg.Surface((config.SCREEN_SIZE[0] * (1 - self.curr_split), config.SCREEN_SIZE[1]))

        self.hitbox_button = ui.Button(5, 5)

        self.hitbox_button.on_click = self._hitbox_button_pressed

        self.curr_mode = MODE_NOTHING
        self.hb_start_x = 0
        self.hb_start_y = 0
        self.hb_select_obj: Hitbox | None = None

    def _hitbox_button_pressed(self):
        if (not self.paused):
            ui.InfoToast.toast("Animation must be paused")
            return
    
        input.set_cursor_mode(input.MODE_CROSSHAIR)
        self.curr_mode = MODE_HITBOX


    def load_animation(self, src: str):
        self.curr_frames_obj = AnimationFrames(src)

        if (len(self.curr_frames_obj.frames) > 0):
            first = self.curr_frames_obj.frames[0].surf

            self.anim_bg_surf = pg.Surface(first.get_size(), pg.SRCALPHA)
            self.anim_bg_surf.fill(config.ANIMATION_BACKGROUND_COLOR0)

    def _update_widgets(self):
        self.hitbox_button.update(pg.mouse.get_pos())

    def _get_disp_mouse(self):
        pos = pg.mouse.get_pos()
        off = (config.SCREEN_SIZE[0] * (1 - self.curr_split), 0)

        scaled_cam = (self.cam_x * self.zoom, self.cam_y * self.zoom)
        world_pos = ((pos[0] - off[0]) + scaled_cam[0], (pos[1] - off[1]) + scaled_cam[1])

        return (world_pos[0] / self.zoom, world_pos[1] / self.zoom)

    def _get_bg_mouse(self):
        pos = self._get_disp_mouse()

        split_size = (config.SCREEN_SIZE[0] * self.curr_split, config.SCREEN_SIZE[1])

        return (pos[0] - split_size[0] / 2, pos[1] - split_size[1] / 2)

    def update(self):
        div = 1 / self.fps * 1000
        time_millis = int(self.time_millis / div)
        
        if (pg.K_SPACE in input.event_keys):
            self.paused = not self.paused

        if (pg.K_ESCAPE in input.event_keys):
            if (self.curr_mode == MODE_HITBOX):
                self.curr_mode = MODE_NOTHING
                input.set_cursor_mode(input.MODE_NORMAL)

        if (input.Mouse.j_m_down and self.curr_mode == MODE_HITBOX):
            if (self.hb_select_obj is not None):
                curr_frame = self.curr_frames_obj.frames[self.curr_disp_frame]
                curr_frame.hitboxes.append(self.hb_select_obj)
                self.hb_select_obj = None

                self.curr_mode = MODE_NOTHING
                input.set_cursor_mode(input.MODE_NORMAL)

            if (self.hb_select_obj is None):
                disp_mouse = self._get_bg_mouse()

                self.hb_select_obj = Hitbox(disp_mouse[0], disp_mouse[1], disp_mouse[0], disp_mouse[1])
                
        if (self.hb_select_obj is not None):
            mouse_pos = self._get_bg_mouse()
            self.hb_select_obj.x2 = mouse_pos[0]
            self.hb_select_obj.y2 = mouse_pos[1]
        # camera movement
        if (pg.mouse.get_pressed()[0]):
            self.cam_x = self.cam_x - input.Mouse.rel[0] / self.zoom
            self.cam_y = self.cam_y - input.Mouse.rel[1] / self.zoom

        else:
            if (input.Mouse.wheel[1] != 0):
                split_size = (config.SCREEN_SIZE[0] * self.curr_split,
                              config.SCREEN_SIZE[1] * self.curr_split)

                cen_pos = (split_size[0] / self.zoom / 2 + self.cam_x,
                           split_size[1] / self.zoom / 2 + self.cam_y)

                self.zoom = max(0.01, self.zoom + input.Mouse.wheel[1])

                self.cam_x = cen_pos[0] - split_size[0] / 2 / self.zoom
                self.cam_y = cen_pos[1] - split_size[1] / 2 / self.zoom
        
        if (not self.paused):
            frame_idx = time_millis % len(self.curr_frames_obj.frames)
            self.curr_disp_frame = frame_idx

            self.time_millis += pg.time.get_ticks() - self.last_time_millis

        self.last_time_millis = pg.time.get_ticks()
        self._update_widgets()
    
    def get_center(self):
        return (config.SCREEN_SIZE[0] * self.curr_split / 2, config.SCREEN_SIZE / 2)

    def _draw_hitbox_bg(self, hitbox: Hitbox):
        center = self.get_center()

        hb = self.hb_select_obj

        x0 = (center[0] + hb.x - self.cam_x) * self.zoom
        y0 = (center[0] + hb.y - self.cam_y) * self.zoom

        x1 = (hb.x2 - self.cam_x) * self.zoom
        y1 = (hb.y2 - self.cam_y) * self.zoom
        
        if (y0 > y1):
            y0, y1 = y1, y0
        
        if (x0 > x1):
            x0, x1 = x1, x0

        
        scaled = pg.transform.scale(hb.surf, (abs(x0 - x1), abs(y0 - y1)))

        self.anim_surf.blit(scaled, (x0, y0))
    def _draw_animation_panel(self):
        current_surf = self.curr_frames_obj.frames[self.curr_disp_frame].surf

        _size = current_surf.get_size()
        _size_scaled = (_size[0] * self.zoom, _size[1] * self.zoom)

        current_frame_scaled = pg.transform.scale(current_surf, _size_scaled)
        surf_size = self.anim_surf.get_size()
        
        centered = ((surf_size[0] / 2 - self.cam_x) * self.zoom, (surf_size[1] / 2 - self.cam_y) * self.zoom)

        if (self.anim_bg_surf is not None):
            bg_frame_scaled = pg.transform.scale(self.anim_bg_surf, _size_scaled)
            self.anim_surf.blit(bg_frame_scaled, centered)

        self.anim_surf.blit(current_frame_scaled, centered)


        if (self.hb_select_obj is not None):
            hb = self.hb_select_obj

            x0 = (hb.x - self.cam_x) * self.zoom
            y0 = (hb.y - self.cam_y) * self.zoom

            x1 = (hb.x2 - self.cam_x) * self.zoom
            y1 = (hb.y2 - self.cam_y) * self.zoom
            
            print((x0, y0), (x1, y1))

            if (y0 > y1):
                y0, y1 = y1, y0
            
            if (x0 > x1):
                x0, x1 = x1, x0

            print((x0, y0), (x1, y1))
            
            scaled = pg.transform.scale(hb.surf, (abs(x0 - x1), abs(y0 - y1)))

            self.anim_surf.blit(scaled, (x0, y0))
            draw_col = hb.draw_color
            # pg.draw.rect(self.anim_surf, (draw_col[0], draw_col[1], draw_col[2], 255 / 2), 
            #              pg.Rect(pos0, (pos1[0] - pos0[0], pos1[1] - pos0[1])))

    def _draw_side_panel(self):
        self.panel_surf.fill(tupmath.add2all(config.CLEAR_COLOR, 30))

        self.hitbox_button.draw(self.panel_surf)

    def draw(self, dst: pg.Surface):
        self.anim_surf.fill(config.CLEAR_COLOR)
        
        self._draw_animation_panel()
        self._draw_side_panel()

        dst.blit(self.anim_surf, (config.SCREEN_SIZE[0] * (1 - self.curr_split),
                                  0))
        
        dst.blit(self.panel_surf, (0, 0))