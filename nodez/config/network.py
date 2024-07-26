import os

from toga import (
    App,
    Box,
    Label,
    TextInput,
    NumberInput,
    MultilineTextInput,
    Divider,
    Switch,
    Button
)
from toga.constants import Direction
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.switch import SwitchStyle
from .styles.input import InputStyle

from ..system import SystemOp

        

class NetConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style = BoxStyle.net_box
        super().__init__(id, style, children)
        self.app = app
        self.system = SystemOp(self.app)
        self.file_path = self.system.load_config_file()
        
        self.net_txt = Label(
            "Network settings",
            style=LabelStyle.title_txt
        )
        self.net_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.testnet_switch = Switch(
            "testnet",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "testnet"
            )
        )
        self.regtest_switch = Switch(
            "regtest",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "regtest"
            )
        )
        self.listen_switch = Switch(
            "listen",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "listen"
            )
        )
        self.server_switch = Switch(
            "server",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "server"
            )
        )
        self.proxy_txt = Label(
            "proxy :",
            style=LabelStyle.proxy_txt
        )
        self.bind_txt = Label(
            "bind :",
            style=LabelStyle.bind_txt
        )
        self.whitebind_txt = Label(
            "whitebind :",
            style=LabelStyle.whitebind_txt
        )
        self.maxconnections_txt = Label(
            "maxconnections :",
            style=LabelStyle.maxconnections_txt
        )
        self.addnode_txt = Label(
            "addnode :",
            style=LabelStyle.addnode_txt
        )
        self.connect_txt = Label(
            "connect :",
            style=LabelStyle.connect_txt
        )
        self.proxy_input = TextInput(
            placeholder="127.0.0.1:9050",
            style=InputStyle.proxy_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "proxy"
            )
        )
        self.bind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.bind_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "bind"
            )
        )
        self.whitebind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.whitebind_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "whitebind"
            )
        )
        self.maxconnections_input = NumberInput(
            min=0,
            style=InputStyle.maxconnections_input,
            on_change=lambda input: self.update_config_input(
                input, "maxconnections"
            )
        )
        self.addnode_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.addnode_input,
            on_change=lambda input: self.update_config_multiinput(
                input, "addnode"
            )
        )
        self.connect_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.connect_input,
            on_change=lambda input: self.update_config_multiinput(
                input, "connect"
            )
        )
        self.testnet_info = Button(
            "?",
            id="testnet",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.regtest_info = Button(
            "?",
            id="regtest",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.listen_info = Button(
            "?",
            id="listen",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.server_info = Button(
            "?",
            id="server",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.proxy_info = Button(
            "?",
            id="proxy",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.bind_info = Button(
            "?",
            id="bind",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.whitebind_info = Button(
            "?",
            id="whitebind",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.maxconnections_info = Button(
            "?",
            id="maxconnections",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.addnode_info = Button(
            "?",
            id="addnode",
            style=ButtonStyle.addnode_info,
            on_press=self.display_info
        )
        self.connect_info = Button(
            "?",
            id="connect",
            style=ButtonStyle.connect_info,
            on_press=self.display_info
        )
        self.net_switch_box = Box(
            style=BoxStyle.net_switch_box
        )
        self.net_button_box = Box(
            style=BoxStyle.net_button_box
        )
        self.net_button2_box = Box(
            style=BoxStyle.net_button2_box
        )
        self.net_txt_box = Box(
            style=BoxStyle.net_txt_box
        )
        self.net_input_box = Box(
            style=BoxStyle.net_input_box
        )
        self.net_row_box = Box(
            style=BoxStyle.net_row_box
        )
        self.net_row2_box = Box(
            style=BoxStyle.net_row2_box
        )
        self.net_switch_box.add(
            self.testnet_switch,
            self.regtest_switch,
            self.listen_switch,
            self.server_switch
        )
        self.net_txt_box.add(
            self.proxy_txt,
            self.bind_txt,
            self.whitebind_txt,
            self.maxconnections_txt,
            self.addnode_txt,
            self.connect_txt
        )
        self.net_button_box.add(
            self.testnet_info,
            self.regtest_info,
            self.listen_info,
            self.server_info
        )
        self.net_button2_box.add(
            self.proxy_info,
            self.bind_info,
            self.whitebind_info,
            self.maxconnections_info,
            self.addnode_info,
            self.connect_info
        )
        self.net_row_box.add(
            self.net_switch_box,
            self.net_button_box
        )
        self.net_row2_box.add(
            self.net_txt_box,
            self.net_input_box,
            self.net_button2_box
        )
        self.add(
            self.net_txt,
            self.net_divider,
            self.net_row_box,
            self.net_row2_box
        )
        self.app.add_background_task(
            self.read_file_lines
        )

                 
    async def read_file_lines(self, widget):
        testnet = regtest = listen = server = proxy = None
        bind = whitebind = maxconnections = None
        addnodes = []
        connections = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == "testnet":
                        testnet = value
                    elif key == "regtest":
                        regtest = value
                    elif key == "listen":
                        listen = value
                    elif key == "server":
                        server = value
                    elif key == "proxy":
                        proxy = value
                    elif key == "bind":
                        bind = value
                    elif key == "whitebind":
                        whitebind = value
                    elif key == "maxconnections":
                        maxconnections = value
                if line.startswith("addnode="):
                    addnodes.append(line.split("=", 1)[1].strip())
                if line.startswith("connect="):
                    connections.append(line.split("=", 1)[1].strip())
        await self.update_values(
                testnet, regtest, listen, server, proxy, bind,
                whitebind, maxconnections, addnodes, connections
            )
        
    async def update_values(
        self,
        testnet, regtest, listen, server, proxy,
        bind, whitebind, maxconnections, addnodes, connections
    ):
        self.testnet_switch.value = (testnet == "1")
        self.regtest_switch.value = (regtest == "1")
        self.listen_switch.value = (listen == "1")
        self.server_switch.value = (server == "1")
        self.proxy_input.value = proxy
        self.bind_input.value = bind
        self.whitebind_input.value = whitebind
        self.maxconnections_input.value = maxconnections
        self.addnode_input.value = "\n".join(addnodes) if addnodes else ""
        self.connect_input.value = "\n".join(connections) if connections else ""
        self.net_input_box.add(
            self.proxy_input,
            self.bind_input,
            self.whitebind_input,
            self.maxconnections_input,
            self.addnode_input,
            self.connect_input
        )
        
    def update_config_switch(self, switch, key):
        new_value = "1" if switch.value else "0"
        key_found = False
        updated_lines = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if "=" in stripped_line:
                current_key, value = map(str.strip, stripped_line.split('=', 1))
                if current_key == key:
                    updated_lines.append(f"{key}={new_value}\n")
                    key_found = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        if not key_found:
            updated_lines.append(f"{key}={new_value}\n")
        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)
            
            
    def update_config_input(self, input, key):
        current_value = input.value
        key_found = False
        updated_lines = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if "=" in stripped_line:
                current_key, value = map(str.strip, stripped_line.split('=', 1))
                if current_key == key:
                    if current_value is not None:
                        updated_lines.append(f"{key}={current_value}\n")
                    else:
                        updated_lines.append(f"{key}=\n")
                    key_found = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        if not key_found:
            if current_value is not None:
                updated_lines.append(f"{key}={current_value}\n")
            else:
                updated_lines.append(f"{key}=\n")
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
        if button.id == "testnet":
            info_message = "Use the test network"
        elif button.id == "regtest":
            info_message = "Run a regression test network"
        elif button.id == "listen":
            info_message = "Accept connections form outside (default : 1 if no -proxy or -connect)"
        elif button.id == "server":
            info_message = "Accept command line and JSON-RPC commands"
        elif button.id == "proxy":
            info_message = "Connect through SOCKS5 proxy"
        elif button.id == "bind":
            info_message = "Bind to given address and always listen on it. Use [host]:port notation for IPv6"
        elif button.id == "whitebind":
            info_message = "Bind to given address and whitelist peers connecting to it. Use [host]:port notation for IPv6"
        elif button.id == "maxconnections":
            info_message = "Maximum number of inbound+outbound connections"
        elif button.id == "addnode":
            info_message = "Use as many settings as you like to connect to specific peers"
        elif button.id == "connect":
            info_message = "Alternatively use as many settings as you like to connect ONLY to specific peers"
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )