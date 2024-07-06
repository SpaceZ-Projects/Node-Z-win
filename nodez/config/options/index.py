import os

from toga import (
    App,
    Box,
    Label,
    Button,
    Divider,
    Switch
)
from toga.constants import Direction
from toga.colors import RED
from toga.widgets.base import Widget

from ..styles.box import BoxStyle
from ..styles.label import LabelStyle
from ..styles.switch import SwitchStyle
from ..styles.button import ButtonStyle
        
              
        
class insightConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None,
    ):
        style = BoxStyle.option_box
        super().__init__(id, style, children)
        self.app = app
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        self.file_path = os.path.join(config_path, config_file)
        
        self.explorer_txt = Label(
            "Insight explorer",
            style=LabelStyle.title_txt
        )
        self.explorer_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.txindex_switch = Switch(
            "txindex",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "txindex"
            )
        )
        self.experimentalfeatures_switch = Switch(
            "experimentalfeatures",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "experimentalfeatures"
            )
        )
        self.insightexplorer_switch = Switch(
            "insightexplorer",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "insightexplorer"
            )
        )
        self.addressindex_switch = Switch(
            "addressindex",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "addressindex"
            )
        )
        self.timestampindex_switch = Switch(
            "timestampindex",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "timestampindex"
            )
        )
        self.spentindex_switch = Switch(
            "spentindex",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "spentindex"
            )
        )
        self.txindex_info = Button(
            "?",
            id="txindex",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.experimentalfeatures_info = Button(
            "?",
            id="experimentalfeatures",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.insightexplorer_info = Button(
            "?",
            id="insightexplorer",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.addressindex_info = Button(
            "?",
            id="addressindex",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.timestampindex_info = Button(
            "?",
            id="timestampindex",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.spentindex_info = Button(
            "?",
            id="spentindex",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.explorer_switch_box = Box(
            style=BoxStyle.explorer_switch_box
        )
        self.explorer_button_box = Box(
            style=BoxStyle.explorer_button_box
        )
        self.explorer_row_box = Box(
            style=BoxStyle.explorer_row_box
        )
        self.explorer_switch_box.add(
            self.txindex_switch,
            self.experimentalfeatures_switch,
            self.insightexplorer_switch,
            self.addressindex_switch,
            self.timestampindex_switch,
            self.spentindex_switch
        )
        self.explorer_button_box.add(
            self.txindex_info,
            self.experimentalfeatures_info,
            self.insightexplorer_info,
            self.addressindex_info,
            self.timestampindex_info,
            self.spentindex_info
        )
        self.explorer_row_box.add(
            self.explorer_switch_box,
            self.explorer_button_box
        )
        self.add(
            self.explorer_txt,
            self.explorer_divider,
            self.explorer_row_box
        )
        self.app.add_background_task(
            self.read_file_lines
        )
                
    
    async def read_file_lines(self, widget):
        txindex = None
        experimentalfeatures = None
        insightexplorer = None
        addressindex = None
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == "txindex":
                        txindex = value
                    elif key == "experimentalfeatures":
                        experimentalfeatures = value
                    elif key == "insightexplorer":
                        insightexplorer = value
                    elif key == "addressindex":
                        addressindex = value
                    elif key == "timestampindex":
                        timestampindex = value
                    elif key == "spentindex":
                        spentindex = value
                        
        await self.update_values(
                    txindex, experimentalfeatures,
                    insightexplorer, addressindex,
                    timestampindex, spentindex
                )
        
    async def update_values(
        self,
        txindex, experimentalfeatures, insightexplorer, addressindex, timestampindex, spentindex
    ):
        self.txindex_switch.value = (txindex == "1")
        self.experimentalfeatures_switch.value = (experimentalfeatures == "1")
        self.insightexplorer_switch.value = (insightexplorer == "1")
        self.addressindex_switch.value = (addressindex == "1")
        self.timestampindex_switch.value = (timestampindex == "1")
        self.spentindex_switch.value = (spentindex == "1")
        
        
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
                    
                    
    def display_info(self, button):
        if button.id == "txindex":
            info_message = "maintains a full index of all transactions in the blockchain. This feature allows for quick lookup of any transaction by its transaction ID (txid)"
        elif button.id == "experimentalfeatures":
            info_message_str = [
                "the experimentalfeatures option enables access to new, in-development features for testing purposes. ",
                "These features are not yet part of the stable release and may include new protocol changes, privacy enhancements, and scalability improvements. ",
                "Enabling this option helps gather feedback and identify issues before official release."
            ]
            info_message = "".join(info_message_str)
        elif button.id == "insightexplorer":
            info_message = "the insightexplorer option enables the Insight API, allowing applications to query detailed blockchain data, including blocks, transactions, and addresses."
        elif button.id == "addressindex":
            info_message = "Enables the node to maintain a searchable index of addresses and their associated transactions, allowing for efficient querying and retrieval of transaction histories for specific addresses."
        elif button.id == "timestampindex":
            info_message = "Enables the node to maintain an index of block timestamps, facilitating efficient retrieval and querying of blocks and transactions based on their timestamps."
        elif button.id == "spentindex":
            info_message = "Maintains an index of spent transaction outputs. This index facilitates efficient verification of spent outputs, enhancing performance when querying transaction status and history."
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )