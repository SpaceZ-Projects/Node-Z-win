
import os
import asyncio

from toga import (
    App,
    Window,
    Box,
    Label,
    ImageView,
    ScrollContainer,
    Divider,
    DetailedList,
    MultilineTextInput,
    Button,
    TextInput,
    Icon
)
from toga.constants import VISIBLE, Direction

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle
from .styles.container import ContainerStyle
from .styles.output import OutputStyle
from .styles.input import InputStyle

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest




class MessageWindow(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Messenger",
            size=(1050, 850),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.command = ClientCommands(self.app)
        self.client = RPCRequest(self.app)

        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button
        

        self.banner_image = ImageView(
            ("icones/messenger_txt.png"),
            style=ImageStyle.banner_image
        )
        self.discussion_outputs = DetailedList(
            data=[
                {
                    "subtitle": "Hello, How are you?"
                }
            ],
            style=OutputStyle.discussion_outputs
        )
        self.discussion_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.chat_inputs = MultilineTextInput(
            placeholder="Say Hello",
            style=InputStyle.chat_inputs
        )
        self.memo_calculate = Label(
            "Memo size : 0 / 512 bytes",
            style=LabelStyle.memo_calculate
        )
        self.send_button = Button(
            "Send",
            enabled=True,
            style=ButtonStyle.send_button
        )
        self.amount_txt = Label(
            "Amount :",
            style=LabelStyle.amount_txt
        )
        self.fee_txt = Label(
            "TxFee :",
            style=LabelStyle.fee_txt
        )
        self.amount_txt_box = Box(
            style=BoxStyle.amount_box
        )
        self.amount_input = TextInput(
            value="0.0001",
            placeholder="1000",
            style=InputStyle.amount_input
        )
        self.fee_input = TextInput(
            value="0.0001",
            placeholder="0.0001",
            style=InputStyle.fee_input
        )
        self.amount_box = Box(
            style=BoxStyle.amount_box
        )
        self.send_box = Box(
            style=BoxStyle.send_box
        )
        self.chat_inputs_box = Box(
            style=BoxStyle.chat_inputs_box
        )
        self.discussion_box = Box(
            style=BoxStyle.discussion_box
        )
        self.contacts_divider = Divider(
            direction=Direction.VERTICAL
        )
        self.add_contact_button = Button(
            "Add Contact",
            enabled=True,
            style=ButtonStyle.add_contact_button
        )
        self.contacts_txt = Label(
            "--------------Contacts--------------",
            style=LabelStyle.contacts_txt
        )
        self.contacts_list = DetailedList(
            style=OutputStyle.contacts_list
        )
        self.contacts_box = Box(
            style=BoxStyle.contacts_box
        )
        self.contacts_container = ScrollContainer(
            horizontal=False,
            style=ContainerStyle.contacts_container,
            content=self.contacts_box
        )
        self.banner_box = Box(
            style=BoxStyle.banner_box
        )
        self.chat_main_box = Box(
            style=BoxStyle.chat_main_box
        )
        self.main_box = Box(
            style=BoxStyle.main_box
        )
        self.banner_box.add(
            self.banner_image
        )
        self.contacts_box.add(
            self.add_contact_button,
            self.contacts_txt,
            self.contacts_list
        )
        self.amount_txt_box.add(
            self.amount_txt,
            self.fee_txt
        )
        self.amount_box.add(
            self.amount_input,
            self.fee_input
        )
        self.send_box.add(
            self.amount_txt_box,
            self.amount_box,
            self.memo_calculate,
            self.send_button
        )
        self.chat_inputs_box.add(
            self.chat_inputs,
            self.send_box
        )
        self.discussion_box.add(
            self.discussion_outputs,
            self.discussion_divider,
            self.chat_inputs_box
        )
        self.chat_main_box.add(
            self.contacts_container,
            self.contacts_divider,
            self.discussion_box
        )
        self.main_box.add(
            self.banner_box,
            self.chat_main_box
        )

        self.content = self.main_box
        
        self.show()
        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('message_window', False)
        self.close()