
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
    ImageView
)
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle

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
        
        self.address_column = Label(
            "Address",
            style=LabelStyle.node_column
        )
        self.ban_until_column = Label(
            "Banned Until",
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
            self.clear_button
        )
        self.banlist_main_box.add(
            self.banned_table_box
        )
        self.address_column.style.visibility = VISIBLE
        self.ban_until_column.style.visibility = VISIBLE
        self.clear_button.style.visibility = VISIBLE
        result = await self.get_nodes_banlist()
        for banned in result:
            address = banned.get('address')
            banned_until = datetime.fromtimestamp(banned.get('banned_until')).strftime("%Y-%m-%d %H:%M:%S")

            address_txt = Label(
                address,
                style=LabelStyle.address_txt
            )
            banned_until_txt = Label(
                banned_until,
                style=LabelStyle.banned_until_txt
            )
            banned_box = Box(
                style=BoxStyle.peer_info_box
            )
            banned_box.add(
                address_txt,
                banned_until_txt
            )
            self.banlist_main_box.add(
                banned_box
            )

            address_txt.style.visibility = VISIBLE
            banned_until_txt.style.visibility = VISIBLE

    
    async def clear_banlist(self, button):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            self.client.clearBanned()
        else:
            await self.command.clearBanned()
        self.banlist_main_box.clear()
        await self.display_tab(None)

    

    async def get_nodes_banlist(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.listBanned()
        else:
            result = await self.command.listBanned()
            result = json.loads(result)
        if result is not None:
            return result