
import os
import json
import asyncio
from datetime import datetime

from toga import (
    App,
    Box,
    ScrollContainer,
    Label,
    Button,
    Selection
)
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle
from .styles.selection import SelectionStyle

from ..command import ClientCommands
from ..client import RPCRequest
from ..system import SystemOp


class BannedList(ScrollContainer):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style= None,
    ):
        super().__init__(id, style)
        self.horizontal = False

        self.app = app
        self.command = ClientCommands(self.app)
        self.client = RPCRequest(self.app)
        self.system = SystemOp(self.app)

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')
        
        self.address_column = Label(
            "Address",
            style=LabelStyle.node_column
        )
        self.ban_until_column = Label(
            "Banned Until",
            style=LabelStyle.default_column
        )
        self.options_column = Label(
            "Options",
            style=LabelStyle.option_column
        )
        self.clear_button = Button(
            "Clear Banlist",
            style=ButtonStyle.clear_button,
            enabled=True,
            on_press=self.clear_banlist
        )
        self.banned_table_box = Box(
            style=BoxStyle.banned_table_box
        )
        self.banlist_main_box = Box(
            style=BoxStyle.peer_main_box
        )

        self.content = self.banlist_main_box

        self.app.add_background_task(
            self.display_tab
        )

    
    async def display_tab(self, widget):
        self.banned_table_box.add(
            self.address_column,
            self.ban_until_column,
            self.options_column,
            self.clear_button
        )
        self.banlist_main_box.add(
            self.banned_table_box
        )
        self.address_column.style.visibility = VISIBLE
        self.ban_until_column.style.visibility = VISIBLE
        self.options_column.style.visibility = VISIBLE
        self.clear_button.style.visibility = VISIBLE
        result = await self.get_nodes_banlist()
        for banned in result:
            address = banned.get('address')
            banned_until = datetime.fromtimestamp(banned.get('banned_until')).strftime("%Y-%m-%d %H:%M:%S")

            option_items = [
                {"option": ""},
                {"option": "Unban"}
            ]

            address_txt = Label(
                address,
                style=LabelStyle.address_txt
            )
            banned_until_txt = Label(
                banned_until,
                style=LabelStyle.banned_until_txt
            )
            option_select = Selection(
                items=option_items,
                accessor="option",
                enabled=True,
                style=SelectionStyle.ban_option_select,
                on_change=lambda widget, address=address: asyncio.create_task(self.get_selected_action(widget, address))
            )

            banned_box = Box(
                style=BoxStyle.peer_info_box
            )
            banned_box.add(
                address_txt,
                banned_until_txt,
                option_select
            )
            self.banlist_main_box.add(
                banned_box
            )

            address_txt.style.visibility = VISIBLE
            banned_until_txt.style.visibility = VISIBLE
            option_select.style.visibility = VISIBLE

    
    async def clear_banlist(self, button):
        if os.path.exists(self.db_path):
            self.client.clearBanned()
        else:
            await self.command.clearBanned()
        self.banlist_main_box.clear()
        await self.display_tab(None)



    async def get_selected_action(self, selection, address):
        selected_option = selection.value.option
        if selected_option == "Unban":
            await self.unban_selected_address(address)
        selection.value = selection.items.find("")


    async def unban_selected_address(self, address):
        if os.path.exists(self.db_path):
            self.client.setBan(address, "remove")
        else:
            await self.command.setBan(address, "remove")
        self.banlist_main_box.clear()
        await self.display_tab(None)    

    

    async def get_nodes_banlist(self):
        if os.path.exists(self.db_path):
            result = self.client.listBanned()
        else:
            result = await self.command.listBanned()
            result = json.loads(result)
        if result is not None:
            return result