import asyncio
import os
from decimal import Decimal

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
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.switch import SwitchStyle
from .styles.input import InputStyle
from .styles.scroll import ScrollStyle


class EditConfig(Window):
    def __init__(self, app:App, config_window):
        super().__init__(
            title="Edit Config",
            size=(450, 620),
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
            style=LabelStyle.guide_txt
        )
        self.save_button = Button(
            "Save",
            style=ButtonStyle.save,
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
            NetConfig(),
            RPCConfig(),
            FeeConfig(),
            OptionsConfig()
        )
        self.main_scroll = ScrollContainer(
            horizontal=False,
            vertical=True,
            content=self.scroll_box,
            style=ScrollStyle.main_scroll
        )
        self.button_box.add(
            self.save_button
        )
        self.main_box.add(
            self.main_scroll,
            self.button_box
        )
        self.content = self.main_box
        
        
    def close_window(self, widget):
        self.config_window.enabled = True
        self.close()
        

class NetConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.net_box
        super().__init__(id, style, children)
        
        self.net_txt = Label(
            "Network settings",
            style=LabelStyle.rpc_txt
        )
        self.net_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.testnet_switch = Switch(
            "testnet",
            style=SwitchStyle.switch
        )
        self.regtest_switch = Switch(
            "regtest",
            style=SwitchStyle.switch
        )
        self.listen_switch = Switch(
            "listen",
            style=SwitchStyle.switch
        )
        self.server_switch = Switch(
            "server",
            style=SwitchStyle.switch
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
            style=InputStyle.proxy_input
        )
        self.bind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.bind_input
        )
        self.whitebind_input = TextInput(
            placeholder="<addr>",
            style=InputStyle.whitebind_input
        )
        self.maxconnections_input = NumberInput(
            min=0,
            style=InputStyle.maxconnections_input
        )
        self.addnode_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.addnode_input
        )
        self.connect_input = MultilineTextInput(
            placeholder="149.28.202.159:1989"
                        "\n85.237.189.122:1989"
                        "\n68.195.18.155:1989"
                        "\nseed.btcz.app"
                        "\nbtzseed.blockhub.info"
                        "\nbtzseed2.blockhub.info",
            style=InputStyle.connect_input
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
        style = BoxStyle.rpc_box
        super().__init__(id, style, children)
        
        self.rpc_txt = Label(
            "RPC server options",
            style=LabelStyle.rpc_txt
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
        
        
class FeeConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.fee_box
        super().__init__(id, style, children)
        
        self.fee_txt = Label(
            "Transaction fee",
            style=LabelStyle.rpc_txt
        )
        self.paytxfee_txt = Label(
            "paytxfee :",
            style=LabelStyle.paytxfee_txt
        )
        self.fee_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.sendfreetransactions_switch = Switch(
            "sendfreetransactions",
            style=SwitchStyle.switch
        )
        self.txconfirmtarget_switch = Switch(
            "txconfirmtarget",
            style=SwitchStyle.switch
        )
        self.paytxfee_input = NumberInput(
            step=Decimal('0.00000001'),
            min=Decimal('0.00000001'),
            style=InputStyle.paytxfee_input
        )
        self.sendfreetransactions_info = Button(
            "?",
            id="sendfreetransactions",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.txconfirmtarget_info = Button(
            "?",
            id="txconfirmtarget",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.paytxfee_info = Button(
            "?",
            id="paytxfee",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.fee_switch_box = Box(
            style=BoxStyle.fee_switch_box
        )
        self.fee_button_box = Box(
            style=BoxStyle.fee_button_box
        )
        self.fee_txt_box = Box(
            style=BoxStyle.fee_txt_box
        )
        self.fee_input_box = Box(
            style=BoxStyle.fee_input_box
        )
        self.fee_button2_box = Box(
            style=BoxStyle.fee_button2_box
        )
        self.fee_row_box = Box(
            style=BoxStyle.fee_row_box
        )
        self.fee_row2_box = Box(
            style=BoxStyle.fee_row2_box
        )
        self.fee_switch_box.add(
            self.sendfreetransactions_switch,
            self.txconfirmtarget_switch
        )
        self.fee_button_box.add(
            self.sendfreetransactions_info,
            self.txconfirmtarget_info
        )
        self.fee_txt_box.add(
            self.paytxfee_txt
        )
        self.fee_input_box.add(
            self.paytxfee_input
        )
        self.fee_button2_box.add(
            self.paytxfee_info
        )
        self.fee_row_box.add(
            self.fee_switch_box,
            self.fee_button_box
        )
        self.fee_row2_box.add(
            self.fee_txt_box,
            self.fee_input_box,
            self.fee_button2_box
        )
        self.add(
            self.fee_txt,
            self.fee_divider,
            self.fee_row_box,
            self.fee_row2_box
        )
        
    def display_info(self, button):
        if button.id == "sendfreetransactions":
            info_message = "Send transactions as zero-fee transactions if possible (default: 0)"
        elif button.id == "txconfirmtarget":
            info_message_str = [
                "Create transactions that have enough fees (or priority) so they are ",
                "likely to # begin confirmation within n blocks (default: 1). ",
                "This setting is overridden by the -paytxfee option"
            ]
            info_message = "".join(info_message_str)
        elif button.id == "paytxfee":
            info_message_str = [
                "Pay an optional transaction fee every time you send BitcoinZ. Transactions with fees ",
                "are more likely than free transactions to be included in generated blocks, so may ",
                "be validated sooner. This setting does not affect private transactions created with ",
                "z_sendmany"
            ]
            info_message = "".join(info_message_str)
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )
        
        
class OptionsConfig(Box):
    def __init__(self, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.option_box
        super().__init__(id, style, children)
        
        self.option_txt = Label(
            "Features",
            style=LabelStyle.rpc_txt
        )
        
        self.add(
            self.option_txt
        )