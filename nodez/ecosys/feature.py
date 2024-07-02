import os
import threading

from toga import (
    App,
    Window,
    Box,
    Label,
    ImageView
)
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.image import ImageStyle
from .styles.label import LabelStyle

from ..system import SystemOp




class EcosysWindow(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Ecosys Features",
            size=(800, 700),
            resizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button

        self.under_dev = ImageView(
            ("icones/under_dev.gif"),
            style=ImageStyle.under_dev
        )
        self.under_dev_txt = Label(
            "Under DEv...",
            style=LabelStyle.under_dev
        )
        self.main_box = Box(
            style=BoxStyle.ecosys_main_box
        )
        self.main_box.add(
            self.under_dev,
            self.under_dev_txt
        )

        self.content = self.main_box
        
        self.show()
        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('ecosys_window', False)
        self.close()