
import os
import asyncio
import shutil

from toga import (
    App,
    Box,
    Label,
    Button,
    ImageView,
    Icon
)
from typing import Iterable
from toga.widgets.base import Widget
from toga.colors import YELLOW, CYAN

from .styles.box import BoxStyle
from .styles.image import ImageStyle
from .styles.button import ButtonStyle
from .styles.label import LabelStyle

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
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)

        self.config_path = self.app.paths.config

        self.qr_code = self.system.qr_generate(self.address)

        self.balance_txt = Label(
            "- Balance -",
            style=LabelStyle.balance_txt
        )
        self.balance_value = Label(
            "_._",
            style=LabelStyle.balance_value
        )
        self.address_balance_box = Box(
            style=BoxStyle.address_balance_box
        )
        self.copy_button = Button(
            icon=Icon("icones/copy"),
            enabled=True,
            style=ButtonStyle.address_buttons,
            on_press=self.copy_address_clipboard
        )
        self.save_button = Button(
            icon=Icon("icones/save"),
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

        self.address_balance_box.add(
            self.balance_txt,
            self.balance_value
        )
        self.address_buttons_box.add(
            self.copy_button,
            self.save_button
        )
        self.add(
            self.address_balance_box,
            self.qrcode_image,
            self.address_buttons_box
        )
        await self.get_address_balance()

    
    async def get_address_balance(self):
        db_path = os.path.join(self.config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.z_getBalance(self.address)
        else:
            result = await self.command.z_getBalance(self.address)
        if result is not None:
            if self.transaction_mode == "transparent":
                self.balance_value.style.color = YELLOW
            elif self.transaction_mode == "shielded":
                self.balance_value.style.color = CYAN
            self.balance_value.text = f"{self.system.format_balance(float(result))}  BTCZ"


    
    async def copy_address_clipboard(self, button):
        import clr
        clr.AddReference('System.Windows.Forms')
        from System.Windows.Forms import Clipboard
        Clipboard.SetText(self.address)

        self.copy_button.enabled = False

        await asyncio.sleep(1)

        self.copy_button.enabled = True



    async def save_qr_image(self, button):
        self.save_button.enabled = False
        async def on_confirm(window, path):
            if path:
                new_path = str(path) + '.png'
                try:
                    shutil.copy(self.qr_code, new_path)
                    self.save_button.enabled = True
                except Exception as e:
                    print(e)
                    self.save_button.enabled = True
            else:
                self.save_button.enabled = True
                    
        self.app.main_window.save_file_dialog(
            title="Save QR...",
            suggested_filename=self.qr_code,
            file_types=["png"],
            on_result=on_confirm
        )