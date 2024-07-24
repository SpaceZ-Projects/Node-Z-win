
import os
import json

from toga import (
    App,
    Box,
    Label
)
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.label import LabelStyle

from ..client import RPCRequest
from ..command import ClientCommands


class PeersInfo(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style= None,
        children: list[Widget] | None = None,
    ):
        style = BoxStyle.peer_main_box
        super().__init__(id, style, children)

        self.app = app
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)


        self.peer_column = Label(
            "ID",
            style=LabelStyle.peer_column
        )
        self.addr_column = Label(
            "IP Address",
            style=LabelStyle.default_column
        )
        self.addrlocal_column = Label(
            "Local Address",
            style=LabelStyle.default_column
        )
        self.subver_column = Label(
            "Version",
            style=LabelStyle.default_column
        )
        self.syncedblocks_column = Label(
            "Last Block",
            style=LabelStyle.default_column
        )
        self.whitelisted_column = Label(
            "Whitelisted",
            style=LabelStyle.default_column
        )
        self.banscore_column = Label(
            "Ban Score",
            style=LabelStyle.banscore_column
        )
        self.peer_table_box = Box(
            style=BoxStyle.peer_table_box
        )
        self.peer_menu_box = Box(
            style=BoxStyle.peer_menu_box
        )

        self.peer_table_box.add(
            self.peer_column,
            self.addr_column,
            self.addrlocal_column,
            self.subver_column,
            self.syncedblocks_column,
            self.whitelisted_column,
            self.banscore_column
        )
        self.peer_menu_box.add(
            self.peer_table_box
        )
        self.add(
            self.peer_menu_box
        )

        self.app.add_background_task(
            self.get_peer_info
        )


    async def get_peer_info(self, widget):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.getPeerInfo()
        else:
            result = await self.command.getPeerInfo()
            result = json.loads(result)
        if result is not None:
            await self.display_window(result)



    async def display_window(self, result):
        for peer in result:
            peer_id = peer.get('id')
            addr = peer.get('addr')
            addrlocal = peer.get('addrlocal')
            subver = peer.get('subver')
            syncedblocks = peer.get('synced_blocks')
            whitelisted = peer.get('whitelisted')
            banscore = peer.get('banscore')
                
            peer_id_txt = Label(
                peer_id,
                style=LabelStyle.peer_id_txt
            )
            addr_txt = Label(
                addr,
                style=LabelStyle.peer_info_txt
            )
            addrlocal_txt = Label(
                addrlocal,
                style=LabelStyle.peer_info_txt
            )
            subver_txt = Label(
                subver,
                style=LabelStyle.peer_info_txt
            )
            syncedblocks_txt = Label(
                syncedblocks,
                style=LabelStyle.peer_info_txt
            )
            whitelisted_txt = Label(
                whitelisted,
                style=LabelStyle.peer_info_txt
            )
            banscore_txt = Label(
                banscore,
                style=LabelStyle.banscore_txt
            )
            peer_info_box = Box(
                style=BoxStyle.peer_info_box
            )
            peer_info_box.add(
                peer_id_txt,
                addr_txt,
                addrlocal_txt,
                subver_txt,
                syncedblocks_txt,
                whitelisted_txt,
                banscore_txt
            )
            self.add(
                peer_info_box
            )