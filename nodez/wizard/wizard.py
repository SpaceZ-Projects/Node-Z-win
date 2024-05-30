import asyncio

from toga import (
    App,
    Box,
    Label,
    ImageView,
    Button,
    Icon,
    Divider
)
from toga.widgets.base import Widget
from toga.constants import Direction
from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle

from ..connect.connect import WindowRPC
from ..startup.startup import NodeSetup
from .social import Social

from ..command import Toolbar
from ..config.config import EditConfig

class MainWizard(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style = BoxStyle.wizard_main_box
        super().__init__(id, style, children)
        self.app = app
        self.commands = Toolbar(self.app)
        
        self.nodez_banner = ImageView(
            "resources/nodez_banner.png"
        )
        self.version_txt = Label(
            f"version {self.app._version}",
            style=LabelStyle.version_text_style
        )
        self.row_top_box = Box(
            style=BoxStyle.wizard_row_top
        )
        self.row_center_box = Box(
            style=BoxStyle.wizard_row_center
        )
        self.row_bottom_box = Box(
            style=BoxStyle.wizard_row_bottom
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL
        )
        self.divider_bottom = Divider(
            direction=Direction.HORIZONTAL
        )
        self.row_bottom_box.add(
            self.version_txt
        )
        self.add(
            self.nodez_banner,
            self.divider_top,
            self.row_center_box,
            self.row_bottom_box,
            self.divider_bottom,
            Social(self.app)
        )
        self.app.add_background_task(
            self.insert_toolbar
        )
        self.app.add_background_task(
            self.loading_options
        )
        
    def insert_toolbar(self, widget):
        self.app.commands.clear()
        self.commands.config_cmd.action = self.display_config_window
        self.app.commands.add(
            self.commands.config_cmd,
            self.commands.import_wallet_cmd
        )
    
    def display_config_window(self, widget):
        self.config_window = EditConfig(
            self.app,
            self.commands.config_cmd
        )

    
    async def loading_options(self, widget):
        await asyncio.sleep(1)
        self.loading_txt = Label(
            "Loading...",
            style=LabelStyle.loading_txt
        )
        self.row_center_box.add(
            self.loading_txt
        )
        await self.display_options()
    
    
    async def display_options(self):
        await asyncio.sleep(1)
        self.row_center_box.remove(
            self.loading_txt
        )
        self.rpc_button = Button(
            icon=Icon("icones/rpc_button"),
            style=ButtonStyle.rpc_button,
            on_press=self.open_rpc_window
        )
        self.local_button = Button(
            icon=Icon("icones/start_button"),
            style=ButtonStyle.local_button,
            on_press=self.check_files
        )
        self.row_center_box.add(
            self.rpc_button,
            self.local_button
        )
        
    async def open_rpc_window(self, button):
        self.rpc_button.enabled = False
        self.local_button.enabled = False
        rpc_window = WindowRPC(
            self.app,
            self.rpc_button,
            self.local_button
        )
        rpc_window.show()
        
    async def check_files(self, button):
        self.rpc_button.enabled = False
        self.local_button.enabled = False
        download_window = NodeSetup(
            self.app,
            self.rpc_button,
            self.local_button
        )
        download_window.show()