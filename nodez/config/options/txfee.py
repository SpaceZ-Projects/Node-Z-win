import asyncio
import os

from toga import (
    App,
    Box,
    Label,
    NumberInput,
    Divider,
    Switch,
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
            style=SwitchStyle.switch
        )
        self.txconfirmtarget_switch = Switch(
            "txconfirmtarget",
            style=SwitchStyle.switch
        )
        self.paytxfee_input = NumberInput(
            step=0.00000001,
            min=0.00000001,
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