
import os
import json
import asyncio
from datetime import datetime
import shutil

from toga import (
    App,
    Box,
    Label,
    ImageView,
    Selection,
    ScrollContainer
)
from toga.widgets.base import Widget
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.image import ImageStyle
from .styles.selection import SelectionStyle

from ..client import RPCRequest
from ..command import ClientCommands
from ..system import SystemOp


class PeersInfo(ScrollContainer):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style= None,
    ):
        super().__init__(id, style)

        self.app = app
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)
        self.file_path = self.system.load_config_file()


        self.peer_column = Label(
            "ID",
            style=LabelStyle.peer_column
        )
        self.addr_column = Label(
            "Node Address",
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
        self.pingtime_column = Label(
            "Ping Time",
            style=LabelStyle.default_column
        )
        self.option_column = Label(
            "Options",
            style=LabelStyle.option_column
        )
        self.peer_table_box = Box(
            style=BoxStyle.peer_table_box
        )
        self.peer_list_box = Box(
            style=BoxStyle.peer_main_box
        )
        self.peer_main_box = Box(
            style=BoxStyle.peer_main_box
        )
        self.content = self.peer_main_box

        self.peer_table_box.add(
            self.peer_column,
            self.addr_column,
            self.addrlocal_column,
            self.subver_column,
            self.syncedblocks_column,
            self.pingtime_column,
            self.option_column
        )
        self.peer_main_box.add(
            self.peer_table_box,
            self.peer_list_box
        )

        self.app.add_background_task(
            self.display_tab
        )


    async def display_tab(self, widget):
        result = await self.get_peers_info()
        for peer in result:
            peer_id = peer.get('id')
            addr = peer.get('addr')
            addrlocal = peer.get('addrlocal')
            subver = peer.get('subver')
            synced_blocks = peer.get('synced_blocks')
            pingtime = peer.get('pingtime') * 1000

            option_items = [
                {"option": ""},
                {"option": "Info"},
                {"option": "Add"},
                {"option": "Disconnect"},
                {"option": "Ban"}
            ]

            peer_image = ImageView(
                ("icones/nodes.gif"),
                style=ImageStyle.peer_image
            )    
            peer_id_txt = Label(
                peer_id,
                style=LabelStyle.peer_id_txt
            )
            addr_txt = Label(
                addr,
                style=LabelStyle.addr_txt
            )
            addrlocal_txt = Label(
                f"{addrlocal[:6]}XXX.XXXX",
                style=LabelStyle.addrlocal_txt
            )
            subver_txt = Label(
                subver,
                style=LabelStyle.subver_txt
            )
            syncedblocks_txt = Label(
                synced_blocks,
                style=LabelStyle.syncedblocks_txt
            )
            pingtime_txt = Label(
                f"{int(pingtime)} ms",
                style=LabelStyle.pingtime_txt
            )
            option_select = Selection(
                items=option_items,
                accessor="option",
                enabled=True,
                style=SelectionStyle.peer_option_select,
                on_change=lambda widget, peer=peer: asyncio.create_task(self.get_selected_action(widget, peer))
            )
            
            peer_info_box = Box(
                style=BoxStyle.peer_info_box
            )
            peer_info_box.add(
                peer_image,
                peer_id_txt,
                addr_txt,
                addrlocal_txt,
                subver_txt,
                syncedblocks_txt,
                pingtime_txt,
                option_select
            )
            self.peer_list_box.add(
                peer_info_box
            )

            peer_image.style.visibility = VISIBLE
            peer_id_txt.style.visibility = VISIBLE
            addr_txt.style.visibility = VISIBLE
            addrlocal_txt.style.visibility = VISIBLE
            subver_txt.style.visibility = VISIBLE
            syncedblocks_txt.style.visibility = VISIBLE
            pingtime_txt.style.visibility = VISIBLE
            option_select.style.visibility = VISIBLE



    async def get_peers_info(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.getPeerInfo()
        else:
            result = await self.command.getPeerInfo()
            result = json.loads(result)
        if result is not None:
            return result
        


    async def get_selected_action(self, selection, peer):
        selected_option = selection.value.option
        if selected_option == "Info":
            await self.display_peer_info(peer)
        elif selected_option == "Add":
            await self.verify_node_address(peer)
        elif selected_option == "Ban":
            await self.ban_node(peer)
            self.peer_list_box.clear()
            await self.display_tab(None)
        selection.value = selection.items.find("")


    async def display_peer_info(self, peer):
        peer_id = peer.get('id')
        addr = peer.get('addr')
        addrlocal = peer.get('addrlocal')
        services = peer.get('services')
        lastsend = datetime.fromtimestamp(peer.get('lastsend')).strftime("%Y-%m-%d %H:%M:%S")
        lastrecv = datetime.fromtimestamp(peer.get('lastrecv')).strftime("%Y-%m-%d %H:%M:%S")
        bytessent = peer.get('bytessent')
        bytesrecv = peer.get('bytesrecv')
        conntime = datetime.fromtimestamp(peer.get('conntime')).strftime("%Y-%m-%d %H:%M:%S")
        timeoffset = peer.get('timeoffset')
        pingtime = peer.get('pingtime') * 1000
        version = peer.get('version')
        subver = peer.get('subver')
        inbound = peer.get('inbound')
        startingheight = peer.get('startingheight')
        banscore = peer.get('banscore')
        synced_headers = peer.get('synced_headers')
        synced_blocks = peer.get('synced_blocks')
        whitelisted = peer.get('whitelisted')

        peer_info_str = [
            f"Peer ID : {peer_id}\n",
            f"Node Addr : {addr}\n",
            f"Addr Local : {addrlocal}\n",
            f"Services : {services}\n",
            f"LastSend : {lastsend}\n",
            f"LastReceive : {lastrecv}\n",
            f"BytesSent : {bytessent}\n",
            f"BytesReceive : {bytesrecv}\n",
            f"ConnTime : {conntime}\n",
            f"TimeOffset : {timeoffset}\n",
            f"PingTime : {int(pingtime)} ms\n",
            f"PeerVersion : {version}\n",
            f"NodeVersion : {subver}\n",
            f"Inbound : {inbound}\n",
            f"Starting Height : {startingheight}\n",
            f"BanScore : {banscore}\n",
            f"Sync Headres : {synced_headers}\n",
            f"Sync Blocks : {synced_blocks}\n",
            f"Whitelisted : {whitelisted}"
        ]
        peer_info = "".join(peer_info_str)

        self.app.main_window.info_dialog(
            "Peer info...",
            peer_info
        )



    async def verify_node_address(self, peer):
        node_address = peer.get('addr')
        addnodes = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("addnode="):
                    addnodes.append(line.split("=", 1)[1].strip())
        if node_address in addnodes:
            self.app.main_window.error_dialog(
                "Error...",
                f"{node_address} is in the addnodes list."
            )
        else:
            async def on_confirm(window, result):
                if result is False:
                    return
                if result is True:
                    await self.add_node(node_address)
            self.app.main_window.question_dialog(
                "Adding node...",
                f"You are about adding a new node address {node_address}, are you sure?",
                on_result=on_confirm
            )



    async def add_node(self, node):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            self.client.addNode(node, "add")
        else:
            await self.command.addNode(node, "add")
            await self.add_node_config_file(node)
        self.peer_list_box.clear()
        await self.display_tab(None)



    async def add_node_config_file(self, node):
        new_entry = f"addnode={node.strip()}\n"
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        entry_found = any(line.strip() == new_entry.strip() for line in lines)
        if not entry_found:
            lines.append(new_entry)
        with open(self.file_path, 'w') as file:
            file.writelines(lines)
        await self.copy_config_datadir()


    
    async def ban_node(self, peer):
        node_address = peer.get('addr')
        address = node_address.split(':')[0]
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            self.client.setBan(address, "add")
        else:
            await self.command.setBan(address, "add")



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
        
        