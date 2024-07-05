
import os
import asyncio
import pyperclip
import shutil

from toga import (
    App,
    Box,
    Label,
    Button,
    ImageView
)
from typing import Iterable
from toga.widgets.base import Widget
from toga.colors import YELLOW, CYAN

from .styles.box import BoxStyle
from .styles.image import ImageStyle
from .styles.button import ButtonStyle

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest


class AddressInfo(Box):
    def __init__(
            self,
            app:App,
            address: str |None = None,
            transaction_mode:str |None = None,
            id: str | None = None,
            style= None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.address_info_box
        super().__init__(id, style, children)
        self.app = app
        self.address = address
        self.transaction_mode = transaction_mode
        self.system = SystemOp(self.app)

        self.qr_code = self.system.qr_generate(self.address)

        self.copy_button = Button(
            "Copy",
            enabled=True,
            style=ButtonStyle.address_buttons,
            on_press=self.copy_address_clipboard
        )
        self.save_button = Button(
            "Save QR",
            enabled=True,
            style=ButtonStyle.address_buttons,
            on_press=self.save_qr_image
        )
        self.address_buttons_box = Box(
            style=BoxStyle.address_buttons_box
        )

        self.app.add_background_task(
            self.get_address_info
        )


    async def get_address_info(self, widget):

        self.qrcode_image = ImageView(
            self.qr_code,
            style=ImageStyle.qr_code_img
        )
        if self.transaction_mode == "transparent":
            self.copy_button.style.background_color = YELLOW
            self.save_button.style.background_color = YELLOW
        elif self.transaction_mode == "shielded":
            self.copy_button.style.background_color = CYAN
            self.save_button.style.background_color = CYAN
        self.address_buttons_box.add(
            self.copy_button,
            self.save_button
        )
        self.add(
            self.qrcode_image,
            self.address_buttons_box
        )

    
    async def copy_address_clipboard(self, button):
        pyperclip.copy(self.address)
        self.copy_button.enabled = False
        self.copy_button.text = "Copied !"
        await asyncio.sleep(1)
        self.copy_button.text = "Copy"
        self.copy_button.enabled = True



    async def save_qr_image(self, button):
        self.save_button.enabled = False
        self.save_button.text = "Saving..."
        async def on_confirm(window, path):
            if path:
                new_path = str(path) + '.png'
                try:
                    shutil.copy(self.qr_code, new_path)
                    self.save_button.enabled = True
                    self.save_button.text = "Save QR"
                except Exception as e:
                    print(e)
                    self.save_button.enabled = True
                    self.save_button.text = "Save QR"
            else:
                self.save_button.enabled = True
                self.save_button.text = "Save QR"
                    
        self.app.main_window.save_file_dialog(
            title="Save QR...",
            suggested_filename=self.qr_code,
            file_types=["png"],
            on_result=on_confirm
        )