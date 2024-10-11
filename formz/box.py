import clr
import time
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Optional, Union, List, Tuple, Callable
from .style import Color

class Box(Forms.Panel):
    def __init__(
        self,
        size: Tuple[int, int] = None,
        location: Tuple[int, int] = (0, 0),
        background_color: Optional[Color] = None,
        on_click: Optional[Callable[[], None]] = None,
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None,
        scrollbale: bool = False,
        scroll_direction :Optional[str] = "vertical"
    ):
        super().__init__()
        self._size = size
        self._location = location
        self._background_color = background_color
        self._on_click = on_click
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave
        self._scrollable = scrollbale
        self._scroll_direction = scroll_direction

        self._widgets = []
        
        if self._size is None:
            self.AutoSize = True
        else:
            self.AutoSize = False
            self.Size = Drawing.Size(*self._size)

        self.Location = Drawing.Point(*self._location)
        if self._background_color:
            self.BackColor = self._background_color

        self.AutoScroll = self._scrollable

        if self._scroll_direction == 'vertical':
            self.VerticalScroll.Enabled = self._scrollable
            self.HorizontalScroll.Enabled = False
        else:
            self.VerticalScroll.Enabled = False
            self.HorizontalScroll.Enabled = self._scrollable

        if self._on_click:
            self.Click += self._handle_click

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave


    @property
    def size(self) -> Tuple[int, int]:
        return self._size
    


    @size.setter
    def size(self, value: Tuple[int, int]):
        self._size = value
        self.Size = Drawing.Size(*value)



    @property
    def location(self) -> Tuple[int, int]:
        return self._location
    


    @location.setter
    def location(self, value: tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(*value)



    @property
    def background_color(self) -> Optional[Drawing.Color]:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Optional[Drawing.Color]):
        self._background_color = value
        if value:
            self.BackColor = value




    @property
    def on_click(self) -> Optional[Callable[[], None]]:
        return self._on_click
    
    

    @on_click.setter
    def on_click(self, value: Optional[Callable[[], None]]):
        if self._on_click:
            self.Click -= self._handle_click
        self._on_click = value
        if self._on_click:
            self.Click += self._handle_click
            


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


    @property
    def widgets(self) -> List[Forms.Control]:
        return self._widgets


    
    def insert(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Add(controls)
            self._widgets.append(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Add(control)
                    self._widgets.append(controls)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
        

    
    def remove(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Remove(controls)
            self._widgets.remove(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Remove(control)
                    self._widgets.remove(controls)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
        

    def _handle_click(self, sender, event):
        if self._on_click:
            self._on_click()


    def _handle_mouse_enter(self, sender, event):
        if self._mouse_enter:
            self._mouse_enter()



    def _handle_mouse_leave(self, sender, event):
        if self._mouse_leave:
            self._mouse_leave()


    def slide(self, target_location: Tuple[int, int], duration: float = 0.5, steps:int = 100):
        sleep_time = duration / steps
        
        delta_x = (target_location[0] - self.Location.X) / steps
        delta_y = (target_location[1] - self.Location.Y) / steps

        for _ in range(steps):
            self.Location = Drawing.Point(int(self.Location.X + delta_x), int(self.Location.Y + delta_y))
            Forms.Application.DoEvents()
            time.sleep(sleep_time)


    def gradient(self, end_rgb: Tuple[int, int, int], duration: float = 0.2, steps: int = 100):
        start_color = self.BackColor
        end_color = Drawing.Color.FromArgb(*end_rgb)

        delta_r = (end_color.R - start_color.R) / steps
        delta_g = (end_color.G - start_color.G) / steps
        delta_b = (end_color.B - start_color.B) / steps

        for i in range(steps):
            new_r = int(start_color.R + delta_r * i)
            new_g = int(start_color.G + delta_g * i)
            new_b = int(start_color.B + delta_b * i)

            self.BackColor = Drawing.Color.FromArgb(new_r, new_g, new_b)
            self.Invalidate()
            Forms.Application.DoEvents()
            time.sleep(duration / steps)


    def clear(self):
        self.Controls.Clear()
        self._widgets.clear()


    def refresh(self):
        self.Invalidate()
        self.Update()

