
import os
import json
import asyncio

from toga import (
    App,
    Window,
    Box,
    Label,
    TextInput,
    ScrollContainer
)
from toga.constants import VISIBLE, HIDDEN

from .styles.box import BoxStyle
from .styles.input import InputStyle
from .styles.label import LabelStyle
from .styles.container import ContainerStyle

from .transaction import Transaction
from .block import BlockIndex
from .address import AddressIndex

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest

class ExplorerWindow(Window):
    def __init__(self, app:App, window_button, txid):
        super().__init__(
            title="Insight Explorer",
            size=(800, 500),
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
        self.txid = txid

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')

        self.explorer_input = TextInput(
            placeholder="Enter an address, transaction hash, block hash or block number",
            style=InputStyle.explorer_input,
            on_confirm=self.verify_input
        )
        self.not_found = Label(
            "Not Found !",
            style=LabelStyle.not_found
        )
        self.explorer_input_box = Box(
            style=BoxStyle.explorer_menu
        )
        self.main_box = Box(
            style=BoxStyle.explorer_main_box
        )
        self.details_container = ScrollContainer(
            style=ContainerStyle.transaction_container
        )
        self.explorer_input_box.add(
            self.explorer_input
        )
        self.main_box.add(
            self.explorer_input_box
        )

        self.content = self.main_box


    async def verify_input(self, input):
        if len(self.main_box.children) > 1:
            self.main_box.remove(self.main_box.children[1])
        inputs = self.explorer_input.value
        inputs = inputs.replace(" ", "")
        if inputs.isdigit() or inputs.startswith("000"):
            await self.get_block_height(inputs)
        elif inputs.startswith("t"):
            await self.get_address_txids(inputs)
        else:
            await self.get_txid_info(inputs)


    async def get_block_height(self, blockheight):
        if os.path.exists(self.db_path):
            result = self.client.getBlock(blockheight)
        else:
            result = await self.command.getBlock(blockheight)
            if result is not None:
                result = json.loads(result)
        if result is None:
            self.explorer_input.value = ""
            self.main_box.add(
                self.not_found
            )
            await asyncio.sleep(2)
            self.main_box.remove(
                self.not_found
            )
        else:
            self.explorer_input.value = ""
            self.explorer_input.readonly = True
            self.details_container.content = BlockIndex(
                self.app,
                result
            )
            self.details_container.style.visibility = HIDDEN
            self.main_box.add(
                self.details_container
            )
            await asyncio.sleep(1)
            self.explorer_input.readonly = False
            self.details_container.style.visibility = VISIBLE


    async def get_address_txids(self, address):
        if os.path.exists(self.db_path):
            result = self.client.getAddressBalance(address)
        else:
            result = await self.command.getAddressBalance(address)
            if result is not None:
                result = json.loads(result)
        if result is None:
            self.explorer_input.value = ""
            self.main_box.add(
                self.not_found
            )
            await asyncio.sleep(2)
            self.main_box.remove(
                self.not_found
            )
        else:
            self.explorer_input.value = ""
            self.explorer_input.readonly = True
            self.details_container.content = AddressIndex(
                self.app,
                address,
                result,
                self.details_container
            )
            self.details_container.style.visibility = HIDDEN
            self.main_box.add(
                self.details_container
            )
            await asyncio.sleep(5)
            self.explorer_input.readonly = False
            self.details_container.style.visibility = VISIBLE

    
    async def get_txid_info(self, txid):
        if os.path.exists(self.db_path):
            result = self.client.getRawTransaction(txid)
        else:
            result = await self.command.getRawTransaction(txid)
            if result is not None:
                result = json.loads(result)
        if result is None:
            self.explorer_input.value = ""
            self.main_box.add(
                self.not_found
            )
            await asyncio.sleep(2)
            self.main_box.remove(
                self.not_found
            )
        else:
            self.explorer_input.value = ""
            self.explorer_input.readonly = True
            self.details_container.content = Transaction(
                self.app,
                result
            )
            self.details_container.style.visibility = HIDDEN
            self.main_box.add(
                self.details_container
            )
            await asyncio.sleep(1)
            self.explorer_input.readonly = False
            self.details_container.style.visibility = VISIBLE


        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('explorer_window', False)
        self.close()