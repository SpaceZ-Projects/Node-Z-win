
import clr
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Callable, Optional, Type, Tuple, Union, List
from pathlib import Path
from .style import Color



class Window(Forms.Form):
    def __init__(
        self,
        size: Tuple[int, int] = (800, 600),
        content: Optional[Type] = None,
        location: Tuple[int, int] = (100, 100),
        center_screen: bool = False,
        background_color: Optional[Color] = None,
        background_image: Optional[Path] = None,
        borderless: bool = True,
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None,
        draggable: bool = False
    ):
        super().__init__()
        self._size = Drawing.Size(size[0], size[1])
        self._content = content
        self._location = location
        self._center_screen = center_screen
        self._background_color = background_color
        self._borderless = borderless
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave

        self._draggable = draggable

        self._dragging = False
        self._drag_start = Drawing.Point(0, 0)

        self.Size = self._size

        if background_color:
            self.BackColor = self._background_color

        if background_image:
            self.BackgroundImage = Drawing.Image.FromFile(str(self._background_image))
            self.BackgroundImageLayout = Forms.ImageLayout.Stretch

        if content:
            self.Controls.Add(self._content)

        self.center_screen = self._center_screen

        if not self._borderless:
            self.FormBorderStyle = Forms.FormBorderStyle(0)

        if draggable:
            self._update_draggable()

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave

        self._initialized = True


    @property
    def size(self):
        return (self.Size.Width, self.Size.Height)
    

    @size.setter
    def size(self, new_size: tuple[int, int]):
        self._size = Drawing.Size(new_size[0], new_size[1])
        self.Size = self._size


    @property
    def content(self) -> Optional[Type]:
        return self._content
    

    @content.setter
    def content(self, new_content: Optional[Type]):
        if self._content and self._content in self.Controls:
            self.Controls.Remove(self._content)
        self._content = new_content
        if new_content:
            self.Controls.Add(new_content)

    
    @property
    def location(self) -> tuple[int, int]:
        return (self.Location.X, self.Location.Y)

    @location.setter
    def location(self, new_location: tuple[int, int]):
        self._set_location(new_location)

    def _set_location(self, location: Tuple[int, int]):
        self._location = location
        if not self._center_screen:
            self.Location = Drawing.Point(location[0], location[1])



    @property
    def center_screen(self) -> bool:
        return self.StartPosition == Forms.FormStartPosition.CenterScreen
    


    @center_screen.setter
    def center_screen(self, value: bool):
        if value:
            self.StartPosition = Forms.FormStartPosition.CenterScreen
        else:
            self.StartPosition = Forms.FormStartPosition.Manual
            self.Location = Drawing.Point(self._location[0], self._location[1])
            


    @property
    def background_color(self) -> Optional[Color]:
        return self._background_color

    @background_color.setter
    def background_color(self, color: Optional[Color]):
        self._background_color = color
        if color is not None:
            self.BackColor = color
        else:
            self.BackColor = None


    
    @property
    def borderless(self) -> bool:
        return self._borderless

    @borderless.setter
    def borderless(self, value: bool):
        if value:
            self.FormBorderStyle = Forms.FormBorderStyle(1)
            self._borderless = True
        else:
            self.FormBorderStyle = Forms.FormBorderStyle(0)
            self._borderless = False


    @property
    def draggable(self) -> bool:
        return self._draggable
    

    @draggable.setter
    def draggable(self, value: bool):
        if self._draggable != value:
            self._draggable = value
            self._update_draggable()


    def _update_draggable(self):
        if self._draggable:
            self.MouseDown += self._on_mouse_down
            self.MouseMove += self._on_mouse_move
            self.MouseUp += self._on_mouse_up
        else:
            self.MouseDown -= self._on_mouse_down
            self.MouseMove -= self._on_mouse_move
            self.MouseUp -= self._on_mouse_up


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



    def _on_mouse_down(self, sender: object, e: Forms.MouseEventArgs):
        if e.Button == Forms.MouseButtons.Left:
            self._dragging = True
            self._drag_start = e.Location



    def _on_mouse_move(self, sender: object, e: Forms.MouseEventArgs):
        if self._dragging:
            self.Location = Drawing.Point(self.Location.X + e.X - self._drag_start.X,
                                          self.Location.Y + e.Y - self._drag_start.Y)
            
            

    def _on_mouse_up(self, sender: object, e: Forms.MouseEventArgs):
        if e.Button == Forms.MouseButtons.Left:
            self._dragging = False



    def insert(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Add(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Add(control)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
        

    
    def remove(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Remove(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Remove(control)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
        

    def _handle_mouse_enter(self, sender, event):
        if self._mouse_enter:
            self._mouse_enter()



    def _handle_mouse_leave(self, sender, event):
        if self._mouse_leave:
            self._mouse_leave()



    def minimize(self):
        self.WindowState = Forms.FormWindowState.Minimized

    
    def activate(self):
        self.Activate()


    def hide(self):
        self.Hide()

    def show(self):
        self.Show()

    def close(self):
        self.Close()


    def showdialog(self):
        self.ShowDialog()