import os
import clr
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Optional, Tuple, Callable
from pathlib import Path
from .style import Color
from .app import App

class Image(Forms.PictureBox):
    def __init__(
        self,
        image: Path = None,
        size: Tuple[int, int] = None,
        background_color: Optional[Color] = Color.TRANSPARENT,
        location: Optional[Tuple[int, int]] = (0, 0),
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None
    ):
        super().__init__()
        self._image_path = image
        self._size = size
        self._background_color = background_color
        self._location = location
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave

        self.app_path  = App().app_path

        self.BackColor = self._background_color
        self.ForeColor = self._background_color

        if self._location:
            self.Location = Drawing.Point(*self._location)

        if self._image_path:
            self._set_image(self._image_path)

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave


    def _set_image(self, image_path: Path):
        try:
            full_path = str(os.path.join(self.app_path , image_path))
            image = Drawing.Bitmap(full_path)
            self.Image = image
            
            if self._size is None:
                self._size = (image.Width, image.Height)
                self.Size = Drawing.Size(*self._size)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.Image = None



    @property
    def image(self) -> Path:
        return self._image_path
    


    @image.setter
    def image(self, value):
        self._image_path = value
        if value:
            self._set_image(value)
        else:
            self.Image = None



    @property
    def size(self) -> Tuple[int, int]:
        return self._size
    


    @size.setter
    def size(self, value: Optional[Tuple[int, int]]):
        if value:
            self._size = value
            self.Size = Drawing.Size(*value)
        else:
            if self.Image:
                self._size = (self.Image.Width, self.Image.Height)
                self.Size = Drawing.Size(*self._size)



    @property
    def background_color(self) -> Optional[Color]:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Optional[Color]):
        self._background_color = value
        if value:
            self.BackColor = value


    
    @property
    def location(self) -> Tuple[int, int]:
        return self._location
    

    @location.setter
    def location(self, value: Tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(*value)


    @property
    def mouse_enter(self) -> Optional[Callable[[], None]]:
        return self._mouse_enter
    



    @mouse_enter.setter
    def mouse_enter(self, value: Optional[Callable[[], None]]):
        if self._mouse_enter:
            self.MouseEnter -= self._handle_mouse_enter
        self._mouse_enter = value
        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter


    
    @property
    def mouse_leave(self) -> Optional[Callable[[], None]]:
        return self._mouse_leave


    @mouse_leave.setter
    def mouse_leave(self, value: Optional[Callable[[], None]]):
        if self._mouse_leave:
            self.MouseLeave -= self._handle_mouse_leave
        self._mouse_leave = value
        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave


    def _handle_mouse_enter(self, sender, event):
        if self._mouse_enter:
            self._mouse_enter()



    def _handle_mouse_leave(self, sender, event):
        if self._mouse_leave:
            self._mouse_leave()
