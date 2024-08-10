
import os
import asyncio
import json
import shutil

from toga import (
    App,
    Window,
    Box,
    ScrollContainer,
    Label,
    Button
)

from .network import NetConfig
from .rpc import RPCConfig
from .txfee import FeeConfig
from .index import insightConfig
from .divers import DiversConfig

from ..system import SystemOp

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.scroll import ScrollStyle


class EditConfig(Window):
    def __init__(self, app:App, local_button):
        super().__init__(
            title="Edit Config",
            size=(700, 800),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.local_button = local_button
        
        guid_message_str = [
            "Below contains information for additional configuration"
            "\nof the bitcoinz.conf file",
            "\n\nNotes:",
            "\nA blank bitcoinz.conf file will run bitcoinzd on mainnet.",
            "\n\nThe most important setting to set is which network, mainnet, testnet,",
            "\nand regtest, bitcoinzd to run.",
            "\nThe other settings allow optimization of bitcoinzd and how it interacts",
            "\nwith other components it services.",
            "\nYou can have multiple configuration files, and run bitcoinzd with a flag",
            "\n-conf=<file> to run with a specific config file.",
            "\nWe suggest keeping various configuration files to suit different needs,"
            "\nrather than editing your configuration file as needed.",
            "\nBy default, the config file bitcoinzd tries is"
            "\n$APPDATA/Roaming/BitcoinZ/bitcoinz.conf on Windows",
        ]
        guid_message = "".join(guid_message_str)
        self.guide_txt = Label(
            guid_message,
            style=LabelStyle.guide_txt
        )
        self.done_button = Button(
            "Save / Close",
            style=ButtonStyle.done_button,
            on_press=self.copy_config_datadir
        )
        self.guide_box = Box(
            style=BoxStyle.guide_box
        )
        self.scroll_box = Box(
            style=BoxStyle.scroll_box
        )
        self.button_box = Box(
            style=BoxStyle.button_box
        )
        self.main_box = Box(
            style=BoxStyle.main_box
        )
        self.guide_box.add(
            self.guide_txt
        )
        self.scroll_box.add(
            self.guide_box,
            NetConfig(self.app),
            RPCConfig(self.app),
            FeeConfig(self.app),
            insightConfig(self.app),
            DiversConfig(self.app)
        )
        self.main_scroll = ScrollContainer(
            horizontal=False,
            vertical=True,
            content=self.scroll_box,
            style=ScrollStyle.main_scroll
        )
        self.button_box.add(
            self.done_button
        )
        self.main_box.add(
            self.main_scroll,
            self.button_box
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.show_window
        )
        
        
    async def show_window(self, window):
        self.show()
        
        
        
    def check_requirements_files(self):
        config_file = self.system.load_config_file()
        if config_file is None:
            config_status = False
        else:
            config_status = True
        node_files = self.system.load_node_files()
        if node_files is not None:
            node_status = False
        else:
            node_status = True
        params_files = self.system.load_params_files()
        if params_files is not None:
            params_status = False
        else:
            params_status = True
        if config_status is True and node_status is True and params_status is True:
            self.local_button.enabled = True
    

    async def copy_config_datadir(self, button):
        settings_path = os.path.join(self.app.paths.config, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                blockchain_path = settings_data.get('blockchainpath')
                
                if blockchain_path in (None, "default"):
                    await self.close_window(None)
                else:
                    config_file = "bitcoinz.conf"
                    config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
                    file_path = os.path.join(config_path, config_file)
                    target_file_path = os.path.join(blockchain_path, config_file)
                    
                    shutil.copyfile(file_path, target_file_path)
                    
                    await self.close_window(None)
        else:
            await self.close_window(None)



    async def close_window(self, widget):
        self.check_requirements_files()
        self.close()
        await asyncio.sleep(1)
        self.app.main_window.show()