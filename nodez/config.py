import asyncio
import aiohttp
import os

from toga import (
    App,
    Window,
    Box,
    ScrollContainer,
    Label,
    TextInput,
    PasswordInput,
    NumberInput,
    Divider,
    Icon,
    ImageView,
    Button
)
from toga.constants import Direction
from toga.colors import RED

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.progressbar import ProgressStyle
from .styles.divider import DividerStyle
from .styles.input import InputStyle
from .styles.button import ButtonStyle


class EditConfig(Window):
    def __init__(self, app:App, config_window):
        super().__init__(
            title="Edit Config",
            size=(400, 550),
            position=(500, 50),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.config_window = config_window
        
        self.rpc_txt = Label(
            "RPC server options",
            style=LabelStyle.config_rpc_txt
        )
        self.rpcuser_txt = Label(
            "rpcuser :",
            style=LabelStyle.config_rpcuser_txt
        )
        self.rpcpassword_txt = Label(
            "rpcpassword :",
            style=LabelStyle.config_rpcpassword_txt
        )
        self.rpcport_txt = Label(
            "rpcport :",
            style=LabelStyle.config_rpcport_txt
        )
        self.rpcuser_input = TextInput(
            style=InputStyle.config_rpcuser_input
        )
        self.rpcpassword_input = PasswordInput(
            style=InputStyle.config_rpcpassword_input
        )
        self.rpcport_input = NumberInput(
            style=InputStyle.config_rpcport_input
        )
        self.rpcuser_info = Button(
            "?",
            id="rpcuser",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.rpcpassword_info = Button(
            "?",
            id="rpcpassword",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.rpcport_info = Button(
            "?",
            id="rpcport",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.rpc_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.rpc_txt_box = Box(
            style=BoxStyle.config_rpc_txt_box
        )
        self.rpc_input_box = Box(
            style=BoxStyle.config_rpc_input_box
        )
        self.rpc_button_box = Box(
            style=BoxStyle.config_rpc_button_box
        )
        self.rpc_txt_box.add(
            self.rpcuser_txt,
            self.rpcpassword_txt,
            self.rpcport_txt
        )
        self.rpc_input_box.add(
            self.rpcuser_input,
            self.rpcpassword_input,
            self.rpcport_input
        )
        self.rpc_button_box.add(
            self.rpcuser_info,
            self.rpcpassword_info,
            self.rpcport_info
        )
        self.rpc_row_box = Box(
            style=BoxStyle.config_rpc_row_box
        )
        self.rpc_row_box.add(
            self.rpc_txt_box,
            self.rpc_input_box,
            self.rpc_button_box
        )
        self.rpc_box = Box(
            style=BoxStyle.config_rpc_box
        )
        self.rpc_box.add(
            self.rpc_txt,
            self.rpc_divider,
            self.rpc_row_box
        )
        self.main_box = Box(
            style=BoxStyle.config_main_box
        )
        self.main_box.add(
            self.rpc_box
        )
        self.main_scroll = ScrollContainer(
            horizontal=False,
            vertical=True,
            content=self.main_box
        )
        self.content = self.main_scroll
        
    def display_info(self, button):
        if button.id == "rpcuser":
            info_message = "Username for JSON-RPC connections"
        elif button.id == "rpcpassword":
            info_message = "Password for JSON-RPC connections"
        elif button.id == "rpcport":
            info_message = "Listen for JSON-RPC connections on <port>\n(default : 8232 or testnet : 18232)"
        self.info_dialog(
            "Info",
            info_message
        )
        
    def close_window(self, widget):
        self.config_window.enabled = True
        self.close()