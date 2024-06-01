import asyncio
import os
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
        self.row_center_box.add(
            self.rpc_button,
            self.local_button
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
        
    def insert_toolbar(self, widget):
        self.app.commands.clear()
        self.commands.config_cmd.action = self.display_config_window
        self.commands.start_config_cmd.action = self.start_with_config
        self.app.commands.add(
            self.commands.config_cmd,
            self.commands.start_config_cmd,
            self.commands.import_wallet_cmd
        )
        self.app.main_window.show()
        
        
    async def start_with_config(self, window):
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        async def on_confirm(window, result):
            print(result)
        self.app.main_window.open_file_dialog(
            "Select config file...",
            file_types=["conf"],
            initial_directory=config_path,
            on_result=on_confirm
        )
        
    
    def display_config_window(self, widget):
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        file_path = os.path.join(config_path, config_file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(
                    "experimentalfeatures=1\n"
                    "insightexplorer=1\n"
                    "txindex=1\n"
                )
        self.config_window = EditConfig(
            self.app,
            self.commands.config_cmd
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