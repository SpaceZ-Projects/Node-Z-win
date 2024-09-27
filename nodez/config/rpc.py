
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
from typing import Iterable
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle

from ..system import SystemOp
        
        
        
class RPCConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: Iterable[Widget] | None = None
    ):
        style = BoxStyle.rpc_box
        super().__init__(id, style, children)
        self.app = app
        self.system = SystemOp(self.app)
        self.file_path = self.system.load_config_file()
        
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
            style=InputStyle.rpcuser_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "rpcuser"
            )
        )
        self.rpcpassword_input = PasswordInput(
            placeholder="<password>",
            style=InputStyle.rpcpassword_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "rpcpassword"
            )
        )
        self.rpcport_input = NumberInput(
            min=0,
            style=InputStyle.rpcport_input,
            on_change=lambda input: self.update_config_input(
                input, "rpcport"
            )
        )
        self.rpcbind_input = MultilineTextInput(
            placeholder="<addr>",
            style=InputStyle.rpcbind_input,
            on_change=lambda input: self.update_config_multiinput(
                input, "rpcbind"
            )
        )
        self.rpcclienttimeout_input = NumberInput(
            min=0,
            style=InputStyle.rpcclienttimeout_input,
            on_change=lambda input: self.update_config_input(
                input, "rpcclienttimeout"
            )
        )
        self.rpcallowip_input = MultilineTextInput(
            placeholder="127.0.0.1/255.255.255.0"
                        "\n127.0.0.1/24"
                        "\n::1/128",
            style=InputStyle.rpcallowip_input,
            on_change=lambda input: self.update_config_multiinput(
                input, "rpcallowip"
            )
        )
        self.rpcconnect_input = TextInput(
            placeholder="127.0.0.1",
            style=InputStyle.rpcconnect_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "rpcconnect"
            )
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
        self.app.add_background_task(
            self.read_file_lines
        )
        
        
    async def read_file_lines(self, widget):
        rpcuser = rpcpassword = rpcconnect = None
        rpcport = ""
        rpcclienttimeout = ""
        rpcbinds = []
        rpcallowips = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == "rpcuser":
                        rpcuser = value
                    elif key == "rpcpassword":
                        rpcpassword = value
                    elif key == "rpcport":
                        rpcport = value
                    elif key == "rpcclienttimeout":
                        rpcclienttimeout = value
                    elif key == "rpcconnect":
                        rpcconnect = value
                if line.startswith("rpcbind="):
                    rpcbinds.append(line.split("=", 1)[1].strip())
                if line.startswith("rpcallowip="):
                    rpcallowips.append(line.split("=", 1)[1].strip())
        await self.update_values(
                rpcuser, rpcpassword, rpcport, rpcclienttimeout,
                rpcconnect, rpcbinds, rpcallowips
            )
        
    async def update_values(
        self,
        rpcuser, rpcpassword, rpcport, rpcclienttimeout,
        rpcconnect, rpcbinds, rpcallowips
    ):
        self.rpcuser_input.value = rpcuser
        self.rpcpassword_input.value = rpcpassword
        self.rpcport_input.value = rpcport
        self.rpcclienttimeout_input.value = rpcclienttimeout
        self.rpcconnect_input.value = rpcconnect
        self.rpcbind_input.value = "\n".join(rpcbinds) if rpcbinds else ""
        self.rpcallowip_input.value = "\n".join(rpcallowips) if rpcallowips else ""
        self.rpc_input_box.add(
            self.rpcuser_input,
            self.rpcpassword_input,
            self.rpcport_input,
            self.rpcbind_input,
            self.rpcclienttimeout_input,
            self.rpcallowip_input,
            self.rpcconnect_input
        )

        
        
    def update_config_input(self, input, key):
        current_value = input.value
        updated_lines = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        key_found = False
        for line in lines:
            stripped_line = line.strip()
            if "=" in stripped_line:
                current_key, _ = map(str.strip, stripped_line.split('=', 1))
                if current_key == key:
                    key_found = True
                    if current_value is not None and current_value != "":
                        updated_lines.append(f"{key}={current_value}\n")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        if not key_found and current_value is not None and current_value != "":
            updated_lines.append(f"{key}={current_value}\n")
        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)
            
    
    def update_config_multiinput(self, input, key):
        input_lines = input.value.strip().split('\n')
        updated_lines = []
        key_lines = [f"{key}={line.strip()}\n" for line in input_lines if line.strip()]
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        key_found = False
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith(f"{key}="):
                if not key_found:
                    updated_lines.extend(key_lines)
                    key_found = True
            else:
                updated_lines.append(line)
        if not key_found:
            updated_lines.extend(key_lines)

        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)
            
        
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