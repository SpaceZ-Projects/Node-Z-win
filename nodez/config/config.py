import os
from toga import (
    App,
    Window,
    Box,
    ScrollContainer,
    Label,
    Button
)

from .options.network import NetConfig
from .options.rpc import RPCConfig
from .options.txfee import FeeConfig
from .options.explorer import insightConfig
from .options.divers import DiversConfig

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.scroll import ScrollStyle


class EditConfig(Window):
    def __init__(self, app:App, config_window, config_button):
        super().__init__(
            title="Edit Config",
            size=(450, 620),
            position=(500, 50),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.config_window = config_window
        self.config_button = config_button
        
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
            "Done",
            style=ButtonStyle.done_button,
            on_press=self.close_window
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
        self.config_window.enabled = False
        self.show()
        
        
    def close_window(self, widget):
        self.config_window.enabled = True
        self.close()