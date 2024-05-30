import asyncio
import os
from decimal import Decimal

from toga import (
    App,
    Box,
    Label,
    TextInput,
    PasswordInput,
    NumberInput,
    MultilineTextInput,
    Divider,
    Button
)
from toga.constants import Direction
from toga.colors import RED
from toga.widgets.base import Widget

from ..styles.box import BoxStyle
from ..styles.button import ButtonStyle
from ..styles.label import LabelStyle
from ..styles.switch import SwitchStyle
from ..styles.input import InputStyle
        
        
        
class RPCConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style = BoxStyle.rpc_box
        super().__init__(id, style, children)
        self.app = app
        
        self.rpc_txt = Label(
            "RPC server options",
            style=LabelStyle.title_txt
        )
        self.rpcuser_txt = Label(
            "rpcuser :",
            style=LabelStyle.rpcuser_txt
        )
        self.rpcpassword_txt = Label(
            "rpcpassword :",
            style=LabelStyle.rpcpassword_txt
        )
        self.rpcport_txt = Label(
            "rpcport :",
            style=LabelStyle.rpcport_txt
        )
        self.rpcbind_txt = Label(
            "rpcbind :",
            style=LabelStyle.rpcbind_txt
        )
        self.rpcclienttimeout_txt = Label(
            "rpcclienttimeout :",
            style=LabelStyle.rpcclienttimeout_txt
        )
        self.rpcallowip_txt = Label(
            "rpcallowip :",
            style=LabelStyle.rpcallowip_txt
        )
        self.rpcconnect_txt = Label(
            "rpcconnect :",
            style=LabelStyle.rpcconnect_txt
        )
        self.rpcuser_input = TextInput(
            placeholder="<username>",
            style=InputStyle.rpcuser_input
        )
        self.rpcpassword_input = PasswordInput(
            placeholder="<password>",
            style=InputStyle.rpcpassword_input
        )
        self.rpcport_input = NumberInput(
            style=InputStyle.rpcport_input
        )
        self.rpcbind_input = MultilineTextInput(
            placeholder="<addr>",
            style=InputStyle.rpcbind_input
        )
        self.rpcclienttimeout_input = NumberInput(
            style=InputStyle.rpcclienttimeout_input
        )
        self.rpcallowip_input = MultilineTextInput(
            placeholder="127.0.0.1/255.255.255.0"
                        "\n127.0.0.1/24"
                        "\n::1/128",
            style=InputStyle.rpcallowip_input
        )
        self.rpcconnect_input = TextInput(
            placeholder="127.0.0.1",
            style=InputStyle.rpcconnect_input
        )
        self.rpcuser_info = Button(
            "?",
            id="rpcuser",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.rpcpassword_info = Button(
            "?",
            id="rpcpassword",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.rpcport_info = Button(
            "?",
            id="rpcport",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.rpcbind_info = Button(
            "?",
            id="rpcbind",
            style=ButtonStyle.rpcbind_info,
            on_press=self.display_info
        )
        self.rpcclienttimeout_info = Button(
            "?",
            id="rpcclienttimeout",
            style=ButtonStyle.rpcclienttimeout_info,
            on_press=self.display_info
        )
        self.rpcallowip_info = Button(
            "?",
            id="rpcallowip",
            style=ButtonStyle.rpcallowip_info,
            on_press=self.display_info
        )
        self.rpcconnect_info = Button(
            "?",
            id="rpcconnect",
            style=ButtonStyle.rpcconnect_info,
            on_press=self.display_info
        )
        self.rpc_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.rpc_txt_box = Box(
            style=BoxStyle.rpc_txt_box
        )
        self.rpc_input_box = Box(
            style=BoxStyle.rpc_input_box
        )
        self.rpc_button_box = Box(
            style=BoxStyle.rpc_button_box
        )
        self.rpc_txt_box.add(
            self.rpcuser_txt,
            self.rpcpassword_txt,
            self.rpcport_txt,
            self.rpcbind_txt,
            self.rpcclienttimeout_txt,
            self.rpcallowip_txt,
            self.rpcconnect_txt
        )
        self.rpc_input_box.add(
            self.rpcuser_input,
            self.rpcpassword_input,
            self.rpcport_input,
            self.rpcbind_input,
            self.rpcclienttimeout_input,
            self.rpcallowip_input,
            self.rpcconnect_input
        )
        self.rpc_button_box.add(
            self.rpcuser_info,
            self.rpcpassword_info,
            self.rpcport_info,
            self.rpcbind_info,
            self.rpcclienttimeout_info,
            self.rpcallowip_info,
            self.rpcconnect_info
        )
        self.rpc_row_box = Box(
            style=BoxStyle.rpc_row_box
        )
        self.rpc_row_box.add(
            self.rpc_txt_box,
            self.rpc_input_box,
            self.rpc_button_box
        )
        self.add(
            self.rpc_txt,
            self.rpc_divider,
            self.rpc_row_box
        )
        
    def display_info(self, button):
        if button.id == "rpcuser":
            info_message = "Username for JSON-RPC connections"
        elif button.id == "rpcpassword":
            info_message = "Password for JSON-RPC connections"
        elif button.id == "rpcport":
            info_message = "Listen for JSON-RPC connections on <port>\n(default : 8232 or testnet : 18232)"
        elif button.id == "rpcbind":
            info_message_str = [
                "Bind to given address to listen for JSON-RPC connections. ",
                "Use [host]:port notation for IPv6. ",
                "This option can be specified multiple times (default: bind to all interfaces)"
            ]
            info_message = "".join(info_message_str)
        elif button.id == "rpcclienttimeout":
            info_message_str = [
                "How many seconds BitcoinZ will wait for a complete RPC HTTP request. ",
                "after the HTTP connection is established"
            ]
            info_message = "".join(info_message_str)
        elif button.id == "rpcallowip":
            info_message_str = [
                "By default, only RPC connections from localhost are allowed. ",
                "Specify as many settings as you require to allow ",
                "insecure connections from other hosts, either as a single IPv4/IPv6 ",
                "or with a subnet specification. Without further security controls, ",
                "an attacker who can see your network traffic will be able to take ",
                "over your node"
            ]
            info_message = "".join(info_message_str)
        elif button.id == "rpcconnect":
            info_message = "You can use bitcoinzd to send commands to bitcoinzd running on another host using this option"
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )