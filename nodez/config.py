import asyncio
import aiohttp
import os

from toga import (
    App,
    Window,
    Box,
    Label,
    ProgressBar,
    Divider,
    Icon,
    ImageView
)
from toga.window import OnCloseHandler
from toga.constants import Direction
from toga.colors import RED

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.progressbar import ProgressStyle
from .styles.divider import DividerStyle


class MakeConfig(Window):
    def __init__(self, app:App, rpc_button, local_button):
        super().__init__(
            title="Making Config...",
            size=(400, 700),
            position=(500, 50),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.rpc_button = rpc_button
        self.local_button = local_button
        
    def close_window(self, widget):
        self.rpc_button.enabled = True
        self.local_button.enabled = True
        self.close()