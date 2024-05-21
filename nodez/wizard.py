import asyncio
import os
import subprocess

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

from .connect import WindowRPC
from .social import Social

class MainWizard(Box):
    def __init__(self, app:App, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.wizard_main_box
        super().__init__(id, style, children)
        self.app = app
        
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
            self.loading_options)
    
    async def loading_options(self, widget):
        await asyncio.sleep(1)
        self.loading_txt = Label(
            "Loading...",
            style=LabelStyle.default_txt_bold_style
        )
        self.row_center_box.add(
            self.loading_txt
        )
        await self.check_data_path()
        
    async def check_data_path(self):
        data_path = self.app.paths.data
        if os.path.exists(data_path):
            result = True
            await self.display_options(result)
        if not os.path.exists(data_path):
            result = False
            await self.display_options(result)
    
    
    async def display_options(self, result):
        if result is True:
            local_icone = Icon("icones/start_button")
            on_select = self.check_node_files
        if result is False:
            local_icone = Icon("icones/setup_button")
            on_select = self.setup_node_files
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
            icon=local_icone,
            style=ButtonStyle.local_button,
            on_press=on_select
        )
        self.row_center_box.add(
            self.rpc_button,
            self.local_button
        )
        
    async def check_node_files(self, button):
        data_path = self.app.paths.data
        required_files = ['bitcoinzd', 'bitcoinz-cli', 'bitcoinz-tx']
        missing_files = []

        for file_name in required_files:
            file_path = os.path.join(data_path, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)
        if missing_files:
            async def on_confirm(window, result):
                if result is False:
                    return
                if result is True:
                    await self.download_nodes_file()
            self.app.main_window.confirm_dialog(
                "Missing Files",
                f"The following required files are missing:\n- {', '.join(missing_files)}",
                on_result=on_confirm
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
            
    async def setup_node_files(self, button):
        data_path = self.app.paths.data
        print(data_path)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        await self.download_nodes_file()
        
    async def download_nodes_file(self):
        pass