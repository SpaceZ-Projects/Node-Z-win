
import json
import asyncio

from toga import (
    App,
    Window,
    Box,
    Label,
    TextInput,
    Button
)
from toga.constants import VISIBLE

from .styles.box import BoxStyle
from .styles.input import InputStyle
from .styles.label import LabelStyle

from .transaction import Transaction

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest

class ExplorerWindow(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Insight Explorer",
            size=(800, 650),
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

        self.explorer_input = TextInput(
            placeholder="Enter an address, transaction hash, block hash or block number",
            style=InputStyle.explorer_input,
            on_confirm=self.verify_input
        )
        self.not_found = Label(
            "Not Found !",
            style=LabelStyle.not_found
        )
        self.main_box = Box(
            style=BoxStyle.explorer_main_box
        )
        self.main_box.add(
            self.explorer_input
        )

        self.content = self.main_box
        
        self.show()


    async def verify_input(self, input):
        if len(self.main_box.children) > 1:
            self.main_box.remove(self.main_box.children[1])
        inputs = self.explorer_input.value
        inputs = inputs.replace(" ", "")
        if inputs.isdigit() or inputs.startswith("0000"):
            await self.get_block_height(inputs)
        elif inputs.startswith("t"):
            await self.get_address_info(inputs)
        else:
            await self.get_txid_info(inputs)


    async def get_block_height(self, blockheight):
        result = await self.command.getBlock(blockheight)
        result = json.loads(result)
        if result:
            print("ok")

    async def get_address_txids(self, address):
        pass

    
    async def get_txid_info(self, txid):
        result = await self.command.getRawTransaction(txid)
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
            result = json.loads(result)
            self.transaction_box = Transaction(
                self.app,
                result
            )
            self.explorer_input.value = ""
            self.main_box.add(
                self.transaction_box
            )


        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('explorer_window', False)
        self.close()