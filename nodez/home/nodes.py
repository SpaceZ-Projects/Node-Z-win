
import os
import json
import asyncio
import shutil

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
from ..system import SystemOp


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
        self.system = SystemOp(self.app)
        self.horizontal = False

        self.file_path = self.system.load_config_file()

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')

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

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        addnode_lines = []
        for line in lines:
            if line.startswith('addnode='):
                _, value = line.split('=', 1)
                value = value.strip()
                addnode_lines.append(value)

        for index, node in enumerate(result):
            addednode = node.get('addednode')
            connected = node.get('connected')
            if addednode in addnode_lines:
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
                    {"option": "Connect"},
                    {"option": "Remove"}
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
        selected_option = selection.value.option
        if selected_option == "Remove":
            await self.remove_node(node)
        elif selected_option == "Connect":
            #edit config and add selected node to connect= list
            await self.connect_node(node)
        selection.value = selection.items.find("")



    async def remove_node(self, node):
        node_address = node.get("addednode")
        
        if os.path.exists(self.db_path):
            self.client.addNode(node, "remove")
        else:
            await self.command.addNode(node_address, "remove")
            await self.remove_node_config_file(node_address)
            
        self.nodes_main_box.clear()
        await self.display_tab(None)



    async def connect_node(self, node):
        node_address = node.get("addednode")
        new_entry = f"connect={node_address.strip()}\n"
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        entry_found = any(line.strip() == new_entry.strip() for line in lines)
        if not entry_found:
            lines.append(new_entry)
        with open(self.file_path, 'w') as file:
            file.writelines(lines)
        await self.copy_config_datadir()
        self.nodes_main_box.clear()
        await self.display_tab(None)
        



    async def remove_node_config_file(self, node):
        node_address = node.get('addednode')

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        update_lines = []
        for line in lines:
            if line.startswith('addnode='):
                _, value = line.split('=', 1)
                value = value.strip()
                if value != node_address:
                    update_lines.append(line)
            else:
                update_lines.append(line)

        with open(self.file_path, 'w') as file:
            file.writelines(update_lines)

        await self.copy_config_datadir()
        

    
    async def copy_config_datadir(self):
        settings_path = os.path.join(self.app.paths.config, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                blockchain_path = settings_data.get('blockchainpath')
                
                if not blockchain_path:
                    return
                else:
                    config_file = "bitcoinz.conf"
                    config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
                    file_path = os.path.join(config_path, config_file)
                    target_file_path = os.path.join(blockchain_path, config_file)
                    
                    shutil.copyfile(file_path, target_file_path)
            



    async def get_nodes_list(self):
        if os.path.exists(self.db_path):
            result = self.client.getAddedNodeInfo()
        else:
            result = await self.command.getAddedNodeInfo()
            result = json.loads(result)
        if result is not None:
            return result