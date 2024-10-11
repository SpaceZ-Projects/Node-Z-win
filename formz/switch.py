import os
import clr
import System
import System.Windows.Forms as Forms
import System.Drawing as Drawing

from typing import Optional, Callable, Tuple
from .app import App

class Switch(Forms.PictureBox):
    def __init__(
        self, 
        location: Tuple[int, int] = (0, 0), 
        value: bool = False,
        enabled: bool = True,
        on_changed: Optional[Callable[[], None]] = None
    ):
        super().__init__()

        self.app_path = App().app_path

        self._value = value
        self._enabled = enabled
        self._location = location
        self._on_switch_changed = on_changed

        self._load_images()

        self.Image = self.switch_active_icon if self._value else self.switch_inactive_icon
        self.Location = Drawing.Point(*self._location)
        
        if self._enabled:
            self.Click += self._on_mouse_click



    @property
    def value(self) -> bool:
        return self._value
    

    
    @value.setter
    def value(self, new_value: bool):
        if self._value != new_value:
            self._value = new_value
            self.Image = self.switch_active_icon if self._value else self.switch_inactive_icon
            if self._on_switch_changed:
                self._on_switch_changed(self._value)



    @property
    def enabled(self) -> bool:
        return self._enabled
    


    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        if value:
            self.Click += self._on_mouse_click
        else:
            self.Click -= self._on_mouse_click



    def _load_images(self):
        switch_inactive = str(os.path.join(self.app_path, 'icons/switch_off.png'))
        switch_active = str(os.path.join(self.app_path, 'icons/switch_on.png'))

        self.switch_inactive_icon = Drawing.Bitmap(switch_inactive)
        self.switch_active_icon = Drawing.Bitmap(switch_active)



    def _on_mouse_click(self, sender, event):
        self.value = not self.value
