
import os
import time
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms


from typing import Callable, Optional, Type, Tuple, Union, List
from pathlib import Path
from .style import Color


class App:
    _icon = None
    _app_path = None
    _app_data = None

    @classmethod
    def set_icon(cls, icon_path: Optional[Path]):
        if icon_path:
            try:
                cls._icon = Drawing.Icon(str(icon_path))
            except Exception as e:
                print(f"Error setting icon: {e}")
        else:
            cls._icon = None

    @classmethod
    def get_icon(cls) -> Optional[Path]:
        return cls._icon
    
    @classmethod
    def _initialize_app_path(cls):
        if cls._app_path is None:
            try:
                script_path = os.path.join(os.path.dirname(__file__))
                cls._app_path = os.path.dirname(script_path)
            except Exception as e:
                print(f"Error initializing app path: {e}")
                

    @property
    def app_path(cls) -> Optional[str]:
        if cls._app_path is None:
            cls._initialize_app_path()
        return cls._app_path
    
    
    @property
    def app_data(cls) -> Path:
        if cls._app_data is None:
            cls._app_data = Path.home() / 'AppData' / 'Local' / 'BTCZCommunity' / 'NodeZ-Remake'
        return cls._app_data
    

    @property
    def screens(cls) -> List[Tuple[int, int]]:
        screens = []
        for screen in Forms.Screen.AllScreens:
            screens.append((screen.Bounds.Width, screen.Bounds.Height))
        return screens
    

    @property
    def screen_size(cls) -> Tuple[int, int]:
        primary_screen = Forms.Screen.PrimaryScreen
        return (primary_screen.Bounds.Width, primary_screen.Bounds.Height)
    

    @classmethod
    def __getattr__(cls, item):
        if item == 'app_path':
            if cls._app_path is None:
                cls._initialize_app_path()
            return cls._app_path
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{item}'")



class MainWindow(Forms.Form):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            print("Warning: An instance of MainWindow already exists")
            return cls._instance
        cls._instance = super(MainWindow, cls).__new__(cls)
        return cls._instance
    

    def __init__(
        self,
        title: str = "Node-Z",
        size: Tuple[int, int] = (800, 600),
        location: Tuple[int, int] = (100, 100),
        center_screen: bool = False,
        background_color: Optional[Color] = None,
        background_image: Optional[Path] = None,
        resizable: bool = True,
        minimizable: bool = True,
        maxmizable: bool = True,
        closable: bool = True,
        borderless: bool = True,
        icon: Optional[Path] = None,
        opacity: float = 1.0,
        on_exit: Optional[Callable[[Type], bool]] = None,
        on_minimize: Optional[Callable[[Type], None]] = None,
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None,
        draggable: bool = False
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        super().__init__()
        self._title = title
        self._size = Drawing.Size(size[0], size[1])
        self._location = location
        self._center_screen = center_screen
        self._background_color = background_color
        self._background_image = background_image
        self._resizable = resizable
        self._minimizable = minimizable
        self._maxmizable = maxmizable
        self._closable = closable
        self._borderless = borderless
        self._icon = icon
        self._opacity = opacity
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave
        self._icon = icon

        self.SetStyle(
            Forms.ControlStyles.AllPaintingInWmPaint | 
            Forms.ControlStyles.UserPaint | 
            Forms.ControlStyles.DoubleBuffer, True
        )

        self._on_exit = on_exit
        self._on_minimize = on_minimize
        self._draggable = draggable

        self._dragging = False
        self._drag_start = Drawing.Point(0, 0)

        self.Opacity = self._opacity
        self.Text = self._title
        self.Size = self._size

        if self._icon:
            App.set_icon(self._icon)
            self.Icon = Drawing.Icon(os.path.join(App().app_path, str(self._icon)))

        if background_color:
            self.BackColor = self._background_color

        if background_image:
            self.BackgroundImage = Drawing.Image.FromFile(str(self._background_image))
            self.BackgroundImageLayout = Forms.ImageLayout.Stretch

        self.MinimizeBox = self._minimizable
        self.MaximizeBox = self._maxmizable
        self.ControlBox = self._closable

        self.center_screen = self._center_screen

        if not self._borderless:
            self.FormBorderStyle = Forms.FormBorderStyle(0)
        elif not self._resizable:
            self.FormBorderStyle = Forms.FormBorderStyle.FixedDialog

        if draggable:
            self._update_draggable()

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave

        self.FormClosing += self._handle_form_closing
        self.Resize += self._handle_minimize_window

        self._initialized = True

    
    @property
    def title(self):
        return self._title
    

    @title.setter
    def title(self, new_title: str):
        self._title = new_title
        self.Text = new_title


    @property
    def icon(self) -> Optional[Path]:
        return self._icon
    


    @icon.setter
    def icon(self, value: Optional[Drawing.Icon]):
        self._icon = value
        App.set_icon(value)
        self.Icon = App.get_icon()


    @property
    def opacity(self) -> float:
        return self._opacity
    


    @opacity.setter
    def opacity(self, value: float):
        if 0.0 <= value <= 1.0:
            self.opacity_slide(value)
        else:
            raise ValueError("Opacity must be between 0.0 and 1.0")


    @property
    def size(self):
        return (self.Size.Width, self.Size.Height)
    

    @size.setter
    def size(self, new_size: tuple[int, int]):
        self._size = Drawing.Size(new_size[0], new_size[1])
        self.Size = self._size

    
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
    def resizable(self):
        return self.FormBorderStyle == Forms.FormBorderStyle.Sizable

    @resizable.setter
    def resizable(self, value: bool):
        if value:
            self.FormBorderStyle = Forms.FormBorderStyle.Sizable
        else:
            self.FormBorderStyle = Forms.FormBorderStyle.FixedDialog
        self._resizable = value


    @property
    def minimizable(self) -> bool:
        return self.MinimizeBox

    @minimizable.setter
    def minimizable(self, value: bool):
        self.MinimizeBox = value
        self._minimizable = value


    @property
    def maxmizable(self) -> bool:
        return self.MaximizeBox

    @maxmizable.setter
    def maxmizable(self, value: bool):
        self.MaximizeBox = value
        self._maxmizable = value


    @property
    def closable(self) -> bool:
        return self.ControlBox

    @closable.setter
    def closable(self, value: bool):
        self.ControlBox = value
        self._closable = value


    
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
    def on_exit(self) -> Optional[Callable[[], bool]]:
        return self._on_exit

    @on_exit.setter
    def on_exit(self, handler: Optional[Callable[[], bool]]):
        self._on_exit = handler

    
    @property
    def on_minimize(self) -> Optional[Callable[[], None]]:
        return self._on_minimize
    

    @on_minimize.setter
    def on_minimize(self, handler: Optional[Callable[[], None]]):
        self._on_minimize = handler


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



    def _handle_form_closing(self, sender, e: Forms.FormClosingEventArgs):
        if self._on_exit:
            result = self._on_exit()
            if result is False:
                e.Cancel = True 


    def _handle_minimize_window(self, sender, e: System.EventArgs):
        if self.WindowState == Forms.FormWindowState.Minimized:
            if callable(self._on_minimize):
                self._on_minimize()



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
        
        

    def opacity_slide(self, target_opacity: float, duration: float = 0.1, steps: int = 100):
        sleep_time = duration / steps
        
        delta_opacity = (target_opacity - self.Opacity) / steps

        for _ in range(steps):
            self.Opacity = min(max(self.Opacity + delta_opacity, 0.0), 1.0)
            Forms.Application.DoEvents()
            time.sleep(sleep_time)

        self.Opacity = target_opacity
        
        

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


    def run(self):
        Forms.Application.Run(self)


    def exit(self):
        Forms.Application.Exit()