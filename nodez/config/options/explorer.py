import asyncio
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
        
        self.explorer_txt = Label(
            "Insight explorer",
            style=LabelStyle.title_txt
        )
        self.explorer_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.txindex_switch = Switch(
            "txindex",
            style=SwitchStyle.switch
        )
        self.experimentalfeatures_switch = Switch(
            "experimentalfeatures",
            style=SwitchStyle.switch
        )
        self.insightexplorer_switch = Switch(
            "insightexplorer",
            style=SwitchStyle.switch
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
            self.insightexplorer_switch
        )
        self.explorer_button_box.add(
            self.txindex_info,
            self.experimentalfeatures_info,
            self.insightexplorer_info
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
            self.check_config_file
        )
    
    async def check_config_file(self, widget):
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        if not os.path.exists(config_path):
            return
        file_path = os.path.join(config_path, config_file)
        if not os.path.exists(file_path):
            return
        else:
            await self.read_file_lines(file_path)
                
    
    async def read_file_lines(self, file_path):
        txindex = None
        experimentalfeatures = None
        insightexplorer = None
        with open(file_path, 'r') as file:
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
                        
        await self.update_values(
                    txindex, experimentalfeatures,
                    insightexplorer
                )
        
    async def update_values(
        self,
        txindex, experimentalfeatures, insightexplorer
    ):
        self.txindex_switch.value = (txindex == "1")
        self.experimentalfeatures_switch.value = (experimentalfeatures == "1")
        self.insightexplorer_switch.value = (insightexplorer == "1")
                    
                    
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
            info_message = "the insightexplorer option enables the Insight API, allowing applications to query detailed blockchain data, including blocks, transactions, and addresses"
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )