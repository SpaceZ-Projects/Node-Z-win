import os

from toga import (
    App,
    Box,
    Label,
    TextInput,
    Divider,
    Switch,
    Button
)
from toga.constants import Direction
from toga.colors import RED, WHITE
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle
from .styles.switch import SwitchStyle
from .styles.input import InputStyle

        
        
class FeeConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style = BoxStyle.fee_box
        super().__init__(id, style, children)
        self.app = app
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        self.file_path = os.path.join(config_path, config_file)
        
        self.fee_txt = Label(
            "Transaction fee",
            style=LabelStyle.title_txt
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
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "sendfreetransactions"
            )
        )
        self.txconfirmtarget_switch = Switch(
            "txconfirmtarget",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "txconfirmtarget"
            )
        )
        self.paytxfee_input = TextInput(
            style=InputStyle.paytxfee_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "paytxfee"
            ),
            validators=[
                self.must_be_decimal
            ]
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
        self.app.add_background_task(
            self.read_file_lines
        )
        
    
    async def read_file_lines(self, widget):
        sendfreetransactions = txconfirmtarget = paytxfee = None
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == "sendfreetransactions":
                        sendfreetransactions = value
                    elif key == "txconfirmtarget":
                        txconfirmtarget = value
                    elif key == "paytxfee":
                        paytxfee = value
        await self.update_values(
                sendfreetransactions, txconfirmtarget, paytxfee
            )
        
    async def update_values(
        self,
        sendfreetransactions, txconfirmtarget, paytxfee
    ):
        self.sendfreetransactions_switch.value = (sendfreetransactions == "1")
        self.txconfirmtarget_switch.value =(txconfirmtarget == "1")
        self.paytxfee_input.value = paytxfee
        self.fee_input_box.add(
            self.paytxfee_input
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
            
    
    def must_be_decimal(self, value):
        if not value.replace('.', '', 1).isdigit():
            self.paytxfee_input.style.color = RED
        else:
            self.paytxfee_input.style.color = WHITE
        
        
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