
import os
import json
import asyncio

from toga import (
    App,
    Box,
    ScrollContainer,
    Label,
    Selection,
    ImageView
)
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.selection import SelectionStyle
from .styles.image import ImageStyle

from ..command import ClientCommands
from ..client import RPCRequest


class NodesList(ScrollContainer):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style= None,
    ):
        super().__init__(id, style)

        self.app = app
        self.command = ClientCommands(self.app)
        self.client = RPCRequest(self.app)
        self.horizontal = False

        self.node_column = Label(
            "ID",
            style=LabelStyle.node_column
        )
        self.address_column = Label(
            "Node Address",
            style=LabelStyle.default_column
        )
        self.status_column = Label(
            "Status",
            style=LabelStyle.default_column
        )
        self.option_column = Label(
            "Options",
            style=LabelStyle.option_column
        )
        self.node_table_box = Box(
            style=BoxStyle.peer_table_box
        )
        self.nodes_main_box = Box(
            style=BoxStyle.peer_main_box
        )

        self.content = self.nodes_main_box
        
        self.app.add_background_task(
            self.display_tab
        )

    async def display_tab(self, widget):
        self.node_table_box.add(
            self.node_column,
            self.address_column,
            self.status_column,
            self.option_column
        )
        self.nodes_main_box.add(
            self.node_table_box
        )
        self.node_column.style.visibility = VISIBLE
        self.address_column.style.visibility = VISIBLE
        self.status_column.style.visibility = VISIBLE
        self.option_column.style.visibility = VISIBLE
        result = await self.get_nodes_list()
        for index, node in enumerate(result):
            addednode = node.get('addednode')
            connected = node.get('connected')
            if connected is True:
                status_icon = ImageView(
                    "icones/green_spot.gif",
                    style=ImageStyle.status_icon
                )
            else:
                status_icon = ImageView(
                    ("icones/red_spot.gif"),
                    style=ImageStyle.status_icon
                )

            option_items = [
                {"option": ""},
                {"option": "Remove"},
                {"option": "Ban"}
            ]

            node_id_txt = Label(
                index+1,
                style=LabelStyle.node_id_txt
            )
            addednode_txt = Label(
                addednode,
                style=LabelStyle.addednode_txt
            )
            option_select = Selection(
                items=option_items,
                accessor="option",
                enabled=True,
                style=SelectionStyle.node_option_select,
                on_change=lambda widget, node=node: asyncio.create_task(self.get_selected_action(widget, node))
            )
            node_box = Box(
                style=BoxStyle.peer_info_box
            )
            node_box.add(
                node_id_txt,
                addednode_txt,
                status_icon,
                option_select
            )
            self.nodes_main_box.add(
                node_box
            )
            node_id_txt.style.visibility = VISIBLE
            addednode_txt.style.visibility = VISIBLE
            status_icon.style.visibility = VISIBLE
            option_select.style.visibility = VISIBLE


    async def get_selected_action(self, selection, node):
        pass


    async def get_nodes_list(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.getAddedNodeInfo()
        else:
            result = await self.command.getAddedNodeInfo()
            result = json.loads(result)
        if result is not None:
            return result