
import os
import json

from toga import (
    App,
    Window,
    Box,
    ImageView,
    Button,
    Label,
    Selection
)
from toga.colors import YELLOW, CYAN
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.image import ImageStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle
from .styles.selection import SelectionStyle

from .address_info import AddressInfo

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest



class WalletWindow(Window):
    def __init__(self, app:App, window_button, explorer_button):
        super().__init__(
            title="Wallet Manage",
            size=(800, 700),
            resizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button
        self.explorer_button = explorer_button

        self.loading_icon = ImageView(
            ("icones/loading_tx.gif"),
            style=ImageStyle.loading_icon
        )
        self.loading_box = Box(
            style=BoxStyle.loading_box
        )
        self.transparent_button = Button(
            "Transparent",
            enabled=True,
            style=ButtonStyle.transparent_button,
            on_press=self.switch_to_transparent
        )
        self.shielded_button = Button(
            "Shielded",
            enabled=True,
            style=ButtonStyle.shielded_button,
            on_press=self.switch_to_shielded
        )
        self.transparent_icon = ImageView(
            "icones/transparent_txt.png",
            style=ImageStyle.transparent_icon
        )
        self.shielded_icon = ImageView(
            "icones/shielded_txt.png",
            style=ImageStyle.shielded_icon
        )
        self.switch_button_box = Box(
            style=BoxStyle.switch_button_box
        )
        self.select_address_txt = Label(
            "Address :",
            style=LabelStyle.select_address_txt
        )
        self.select_address = Selection(
            accessor="select_address",
            enabled=True,
            style=SelectionStyle.select_address,
            on_change=self.display_address_info
        )
        self.new_address_button = Button(
            "New Address",
            enabled=True,
            style=ButtonStyle.new_address_button,
            on_press=self.generate_new_address
        )
        self.select_address_box = Box(
            style=BoxStyle.select_address_box
        )
        self.address_manage_box = Box(
            style=BoxStyle.address_manage_box
        )

        self.main_box = Box(
            style=BoxStyle.wallet_main_box
        )
        self.main_box.add(
            self.switch_button_box,
            self.select_address_box
        )

        self.content = self.main_box
        
        self.app.add_background_task(
            self.get_addresses_list
        )



    async def get_addresses_list(self, widget):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.items = transparent_address

        self.display_window()


    def display_window(self):
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        self.select_address_box.add(
            self.select_address_txt,
            self.select_address,
            self.new_address_button
        )
        self.show()
        

    async def switch_to_transparent(self, button):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.items.clear()
        self.select_address.style.color = YELLOW
        self.select_address.items = transparent_address
        self.switch_button_box.remove(
            self.transparent_button,
            self.shielded_icon
        )
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        
    async def switch_to_shielded(self, button):
        self.transaction_mode = "shielded"
        shielded_address = await self.get_shielded_addresses()
        self.select_address.items.clear()
        self.select_address.style.color = CYAN
        self.select_address.items = shielded_address
        self.switch_button_box.remove(
            self.transparent_icon,
            self.shielded_button
        )
        self.switch_button_box.add(
            self.transparent_button,
            self.shielded_icon
        )


    async def get_transparent_addresses(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            addresses_data = self.client.listAddressgroupPings()
        else:
            addresses_data = await self.command.listAddressgroupPings()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            sorted_addresses = sorted(
                [address_info for address_info_list in addresses_data for address_info in address_info_list],
                key=lambda x: x[1],
                reverse=True
            )
            if len(sorted_addresses) == 1:
                address_items = [("Main Account", ""), (sorted_addresses[0][0], sorted_addresses[0][0])]
            else:
                address_items = [("Main Account", "")] + [(address_info[0], address_info[0]) for address_info in sorted_addresses]
        else:
            address_items = [("Main Account", "")]
        return address_items
    

    async def get_shielded_addresses(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            addresses_data = self.client.z_listAddresses()
        else:
            addresses_data = await self.command.z_listAddresses()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            if len(addresses_data) == 1:
                address_items = [(addresses_data[0], addresses_data[0])]
            else:
                address_items = [(address, address) for address in addresses_data]
        else:
            address_items = []
        return address_items
    

    async def generate_new_address(self, button):
        self.new_address_button.enabled = False
        if self.transaction_mode == "transparent":
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                new_address = self.client.getNewAddress()
            else:
                new_address = await self.command.getNewAddress()
        
        elif self.transaction_mode == "shielded":
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                new_address = self.client.z_getNewAddress()
            else:
                new_address = await self.command.z_getNewAddress()

        if new_address is not None:
            self.info_dialog(
                "New Address",
                f"New address generated :\n{new_address}"
            )
            await self.update_addresses_list(new_address)
        self.new_address_button.enabled = True


    async def update_addresses_list(self, address):
        self.select_address.items.clear()

        if self.transaction_mode == "transparent":
            transparent_address = await self.get_transparent_addresses()
            self.select_address.style.color = YELLOW
            self.select_address.items = transparent_address

        elif self.transaction_mode == "shielded":
            shielded_address = await self.get_shielded_addresses()
            self.select_address.style.color = CYAN
            self.select_address.items = shielded_address
            
        self.select_address.value = self.select_address.items.find(address)

    

    async def display_address_info(self, selection):
        if not self.select_address.value:
            return
        
        if not self.select_address.value.select_address:
            return
        
        address = self.select_address.value.select_address
        if address == "Main Account":
            if len(self.address_manage_box.children) > 0:
                self.address_manage_box.remove(self.address_manage_box.children[0])
            return
        
        if len(self.address_manage_box.children) > 0:
            self.address_manage_box.remove(self.address_manage_box.children[0])

        self.address_manage_box.add(
            AddressInfo(
                self.app,
                address,
                self.transaction_mode
            )
        )
        self.main_box.add(
            self.address_manage_box
        )
        


    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('wallet_window', False)
        self.close()