import pygame as pg
import config
import tupmath
from PIL import Image
import ui
import input

FORMAT_HORIZONTAL = "horizontal"
FORMAT_VERTICAL = "vertical"
FORMAT_GIF = "gif"

MODE_NOTTHING = "nothing"
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

        self.draw_color = (255, 0, 0)


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

        self.curr_mode = MODE_NOTTHING
        self.hb_start_x = 0
        self.hb_start_y = 0
        self.hb_select_started = False

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

        current_surf = self.curr_frames_obj.frames[self.curr_disp_frame].surf

        _size = current_surf.get_size()
        _size_scaled = (_size[0] * self.zoom, _size[1] * self.zoom)
        
        surf_size = self.anim_surf.get_size()

        centered = ((surf_size[0] - _size_scaled[0]) / 2 - self.cam_x,
                    (surf_size[1] - _size_scaled[1]) / 2 - self.cam_y)
        
        return (pos[0] - centered[0], pos[1] - centered[1])

    def update(self):
        div = 1 / self.fps * 1000
        time_millis = int(self.time_millis / div)
        
        if (pg.K_SPACE in input.event_keys):
            self.paused = not self.paused

        if (input.Mouse.j_m_down and self.curr_mode == MODE_HITBOX):
            if (not self.hb_select_started):
                self.hb_select_started = True

                self.hb_start_x = pg.mous
        
        print(self._get_disp_mouse())
        # camera movement
        if (pg.mouse.get_pressed()[1]):
            self.cam_x = self.cam_x - input.Mouse.rel[0] / self.zoom
            self.cam_y = self.cam_y - input.Mouse.rel[1] / self.zoom
        else:
            self.zoom = max(0.01, self.zoom + input.Mouse.wheel[1])

        
        if (not self.paused):
            frame_idx = time_millis % len(self.curr_frames_obj.frames)
            self.curr_disp_frame = frame_idx

            self.time_millis += pg.time.get_ticks() - self.last_time_millis

        self.last_time_millis = pg.time.get_ticks()
        self._update_widgets()

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