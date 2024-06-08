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
from .styles.divider import DividerStyle

from .connect import WindowRPC
from .start import StartNode
from .social import Social
from .download import DownloadNode, DownloadParams

from ..config.config import EditConfig
from ..system import SystemOp

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
        self.system = SystemOp(self.app)
        self.config_status = None
        self.node_status = None
        self.params_status = None
        
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
            on_press=self.start_node
        )
        self.download_node_button = Button(
            icon=Icon("icones/download"),
            style=ButtonStyle.download_button,
            on_press=self.download_node_files
        )
        self.download_params_button = Button(
            icon=Icon("icones/download"),
            style=ButtonStyle.download_button,
            on_press=self.download_params_files
        )
        self.config_button = Button(
            icon=Icon("icones/config"),
            style=ButtonStyle.download_button,
            on_press=self.display_config_window
        )
        self.version_txt = Label(
            f"version {self.app._version}",
            style=LabelStyle.version_text_style
        )
        self.node_files_txt = Label(
            "Node\nfiles",
            style=LabelStyle.node_files_txt
        )
        self.params_txt = Label(
            "Params\nfiles",
            style=LabelStyle.params_txt
        )
        self.config_txt = Label(
            "Config\nfile",
            style=LabelStyle.config_txt
        )
        self.rpc_description_txt = Label(
            "connection to a node via remote procedure calls",
            style=LabelStyle.rpc_description_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.wizard_divider_top
        )
        self.divider_center = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.wizard_divider_center
        )
        self.divider_bottom = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.wizard_divider_bottom
        )
        self.local_divider_1 = Divider(
            direction=Direction.VERTICAL,
            style=DividerStyle.local_divider
        )
        self.local_divider_2 = Divider(
            direction=Direction.VERTICAL,
            style=DividerStyle.local_divider
        )
        self.local_row_box = Box(
            style=BoxStyle.wizard_local_row
        )
        self.rpc_row_box = Box(
            style=BoxStyle.wizard_rpc_row
        )
        self.center_box = Box(
            style=BoxStyle.wizard_center
        )
        self.row_bottom_box = Box(
            style=BoxStyle.wizard_row_bottom
        )
        self.local_row_box.add(
            self.local_button,
            self.node_files_txt,
            self.download_node_button,
            self.local_divider_1,
            self.params_txt,
            self.download_params_button,
            self.local_divider_2,
            self.config_txt,
            self.config_button
        )
        self.rpc_row_box.add(
            self.rpc_button,
            self.rpc_description_txt
        )
        self.center_box.add(
            self.local_row_box,
            self.divider_center,
            self.rpc_row_box
        )
        self.row_bottom_box.add(
            self.version_txt
        )
        self.add(
            self.nodez_banner,
            self.divider_top,
            self.center_box,
            self.row_bottom_box,
            self.divider_bottom,
            Social(self.app)
        )
        self.app.add_background_task(
            self.check_config
        )
        
    async def check_config(self, widget):
        config_file = self.system.load_config_file()
        if config_file is None:
            self.config_status = False
        else:
            self.config_status = True
            
        await self.check_node_files()
        
    
    async def check_node_files(self):
        node_files = self.system.load_node_files()
        if node_files is not None:
            self.node_status = False
            self.download_node_button.enabled = True
        else:
            self.node_status = True
            self.download_node_button.enabled = False
        
        await self.check_params_files()
        
        
    async def check_params_files(self):
        params_files = self.system.load_params_files()
        if params_files is not None:
            self.params_status = False
            self.download_params_button.enabled = True
        else:
            self.params_status = True
            self.download_params_button.enabled = False
            
        await self.insert_toolbar()
        
        
    async def insert_toolbar(self):
        self.app.commands.clear()
        await self.display_main_window()
        
        
    async def display_main_window(self):
        if self.config_status is True and self.node_status is True and self.params_status is True:
            self.local_button.enabled = True
        else:
            self.local_button.enabled = False   
        self.app.main_window.show()
        
        
    def download_node_files(self, button):
        self.download_node_window = DownloadNode(
            self.app,
            self.download_node_button,
            self.local_button,
            self.rpc_button
        )
        
    def download_params_files(self, button):
        self.download_params_window = DownloadParams(
            self.app,
            self.download_params_button,
            self.local_button,
            self.rpc_button
        )
        
    def display_config_window(self, button):
        self.app.main_window.hide()
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        file_path = os.path.join(config_path, config_file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write('')
        self.config_window = EditConfig(
            self.app,
            self.local_button
        )
        
    
    def start_node(self, button):
        self.local_window = StartNode(
            self.app
        )
        
    def open_rpc_window(self, button):
        self.rpc_window = WindowRPC(
            self.app
        )