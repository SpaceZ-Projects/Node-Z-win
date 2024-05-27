import asyncio
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
    MultilineTextInput,
    Divider,
    Switch,
    Button
)
from toga.constants import Direction
from toga.colors import RED
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from .styles.button import ButtonStyle
from .styles.switch import SwitchStyle


class EditConfig(Window):
    def __init__(self, app:App, config_window):
        super().__init__(
            title="Edit Config",
            size=(450, 550),
            position=(500, 50),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.config_window = config_window
        
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
            style=LabelStyle.config_guide_txt
        )
        self.guide_box = Box(
            style=BoxStyle.config_guide_box
        )
        self.main_box = Box(
            style=BoxStyle.config_main_box
        )
        self.guide_box.add(
            self.guide_txt
        )
        self.main_box.add(
            self.guide_box,
            NetConfig(),
            RPCConfig(),
            FeeConfig(),
            OptionsConfig()
        )
        self.main_scroll = ScrollContainer(
            horizontal=False,
            vertical=True,
            content=self.main_box
        )
        self.content = self.main_scroll
        
        
    def close_window(self, widget):
        self.config_window.enabled = True
        self.close()
        

class NetConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.config_net_box
        super().__init__(id, style, children)
        
        self.net_txt = Label(
            "Network settings",
            style=LabelStyle.config_rpc_txt
        )
        self.net_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.testnet_switch = Switch(
            "testnet",
            style=SwitchStyle.config_net_switch
        )
        self.regtest_switch = Switch(
            "regtest",
            style=SwitchStyle.config_net_switch
        )
        self.listen_switch = Switch(
            "listen",
            style=SwitchStyle.config_net_switch
        )
        self.server_switch = Switch(
            "server",
            style=SwitchStyle.config_net_switch
        )
        self.proxy_txt = Label(
            "proxy :",
            style=LabelStyle.config_proxy_txt
        )
        self.bind_txt = Label(
            "bind :",
            style=LabelStyle.config_bind_txt
        )
        self.whitebind_txt = Label(
            "whitebind :",
            style=LabelStyle.config_whitebind_txt
        )
        self.maxconnections_txt = Label(
            "maxconnections :",
            style=LabelStyle.config_maxconnections_txt
        )
        self.addnode_txt = Label(
            "addnode :",
            style=LabelStyle.config_addnode_txt
        )
        self.connect_txt = Label(
            "connect :",
            style=LabelStyle.config_connect_txt
        )
        self.proxy_input = TextInput(
            placeholder="127.0.0.1:9050",
            style=InputStyle.config_proxy_input
        )
        self.bind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.config_bind_input
        )
        self.whitebind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.config_whitebind_input
        )
        self.maxconnections_input = NumberInput(
            max=8,
            min=2,
            style=InputStyle.config_maxconnections_input
        )
        self.addnode_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.config_addnode_input
        )
        self.connect_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.config_connect_input
        )
        self.testnet_info = Button(
            "?",
            id="testnet",
            style=ButtonStyle.config_net_info_button,
            on_press=self.display_info
        )
        self.regtest_info = Button(
            "?",
            id="regtest",
            style=ButtonStyle.config_net_info_button,
            on_press=self.display_info
        )
        self.listen_info = Button(
            "?",
            id="listen",
            style=ButtonStyle.config_net_info_button,
            on_press=self.display_info
        )
        self.server_info = Button(
            "?",
            id="server",
            style=ButtonStyle.config_net_info_button,
            on_press=self.display_info
        )
        self.proxy_info = Button(
            "?",
            id="proxy",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.bind_info = Button(
            "?",
            id="bind",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.whitebind_info = Button(
            "?",
            id="whitebind",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.maxconnections_info = Button(
            "?",
            id="maxconnections",
            style=ButtonStyle.config_info_button,
            on_press=self.display_info
        )
        self.addnode_info = Button(
            "?",
            id="addnode",
            style=ButtonStyle.config_addnode_info,
            on_press=self.display_info
        )
        self.connect_info = Button(
            "?",
            id="connect",
            style=ButtonStyle.config_connect_info,
            on_press=self.display_info
        )
        self.net_switch_box = Box(
            style=BoxStyle.config_net_switch_box
        )
        self.net_button_box = Box(
            style=BoxStyle.config_net_button_box
        )
        self.net_button2_box = Box(
            style=BoxStyle.config_net_button2_box
        )
        self.net_txt_box = Box(
            style=BoxStyle.config_net_txt_box
        )
        self.net_input_box = Box(
            style=BoxStyle.config_net_input_box
        )
        self.net_row_box = Box(
            style=BoxStyle.config_net_row_box
        )
        self.net_row2_box = Box(
            style=BoxStyle.config_net_row2_box
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
        self.net_input_box.add(
            self.proxy_input,
            self.bind_input,
            self.whitebind_input,
            self.maxconnections_input,
            self.addnode_input,
            self.connect_input
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
        
        
        
class RPCConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.config_rpc_box
        super().__init__(id, style, children)
        
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
        self.rpcbind_txt = Label(
            "rpcbind :",
            style=LabelStyle.config_rpcbind_txt
        )
        self.rpcclienttimeout_txt = Label(
            "rpcclienttimeout :",
            style=LabelStyle.config_rpcclienttimeout_txt
        )
        self.rpcallowip_txt = Label(
            "rpcallowip :",
            style=LabelStyle.config_rpcallowip_txt
        )
        self.rpcconnect_txt = Label(
            "rpcconnect :",
            style=LabelStyle.config_rpcconnect_txt
        )
        self.rpcuser_input = TextInput(
            placeholder="<username>",
            style=InputStyle.config_rpcuser_input
        )
        self.rpcpassword_input = PasswordInput(
            placeholder="<password>",
            style=InputStyle.config_rpcpassword_input
        )
        self.rpcport_input = NumberInput(
            style=InputStyle.config_rpcport_input
        )
        self.rpcbind_input = MultilineTextInput(
            placeholder="<addr>",
            style=InputStyle.config_rpcbind_input
        )
        self.rpcclienttimeout_input = NumberInput(
            style=InputStyle.config_rpcclienttimeout_input
        )
        self.rpcallowip_input = MultilineTextInput(
            placeholder="127.0.0.1/255.255.255.0"
                        "\n127.0.0.1/24"
                        "\n::1/128",
            style=InputStyle.config_rpcallowip_input
        )
        self.rpcconnect_input = TextInput(
            placeholder="127.0.0.1",
            style=InputStyle.config_rpcconnect_input
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
        self.rpcbind_info = Button(
            "?",
            id="rpcbind",
            style=ButtonStyle.config_rpcbind_info,
            on_press=self.display_info
        )
        self.rpcclienttimeout_info = Button(
            "?",
            id="rpcclienttimeout",
            style=ButtonStyle.config_rpcclienttimeout_info,
            on_press=self.display_info
        )
        self.rpcallowip_info = Button(
            "?",
            id="rpcallowip",
            style=ButtonStyle.config_rpcallowip_info,
            on_press=self.display_info
        )
        self.rpcconnect_info = Button(
            "?",
            id="rpcconnect",
            style=ButtonStyle.config_rpcconnect_info,
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
            style=BoxStyle.config_rpc_row_box
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
        
        
class FeeConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.config_fee_box
        super().__init__(id, style, children)
        
        self.fee_txt = Label(
            "Transaction fee",
            style=LabelStyle.config_rpc_txt
        )
        
        self.add(
            self.fee_txt
        )
        
        
class OptionsConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.config_option_box
        super().__init__(id, style, children)
        
        self.option_txt = Label(
            "Features",
            style=LabelStyle.config_rpc_txt
        )
        
        self.add(
            self.option_txt
        )