import asyncio
import os
import json
from collections import Counter
from datetime import datetime
from typing import Iterable

from toga import (
    App,
    Box,
    Button,
    Label,
    Icon,
    ImageView,
    TextInput,
    Divider
)
from toga.widgets.base import Widget
from toga.constants import Direction
from toga.colors import RED, GREEN

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle
from .styles.image import ImageStyle

from ..client import RPCRequest
from ..command import ClientCommands
from ..system import SystemOp


class AddressIndex(Box):
    def __init__(
            self,
            app:App,
            address: str |None = None,
            result: str | None = None,
            on_scroll= None,
            id: str | None = None,
            style= None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.address_info
        super().__init__(id, style, children)
        self.app = app
        self.address = address
        self.result = result
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)
        self.on_scroll = on_scroll

        self.address_title = Label(
            self.address,
            style=LabelStyle.address_title
        )
        self.total_received_txt = Label(
            "Total Received :",
            style=LabelStyle.address_total_received_txt
        )
        self.total_received = Label(
            "",
            style=LabelStyle.address_total_received
        )
        self.total_received_box = Box(
            style=BoxStyle.address_lines_box
        )
        self.total_sent_txt = Label(
            "Total Sent :",
            style=LabelStyle.address_total_sent_txt
        )
        self.total_sent = Label(
            "",
            style=LabelStyle.address_total_sent
        )
        self.total_sent_box = Box(
            style=BoxStyle.address_lines_box
        )
        self.final_balance_txt = Label(
            "Final Balance :",
            style=LabelStyle.address_final_balance_txt
        )
        self.final_balance = Label(
            "",
            style=LabelStyle.address_final_balance
        )
        self.final_balance_box = Box(
            style=BoxStyle.address_lines_box
        )
        self.number_transactions_txt = Label(
            "No. Transactions :",
            style=LabelStyle.address_number_transactions_txt
        )
        self.number_transactions = Label(
            "",
            style=LabelStyle.address_number_transactions
        )
        self.number_transactions_box = Box(
            style=BoxStyle.address_lines_box
        )
        self.address_divider = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.address_divider
        )
        self.transactions_title = Label(
            "- Transactions -",
            style=LabelStyle.address_transactions_title
        )
        self.address_balances_list_box = Box(
            style=BoxStyle.address_balances_list_box
        )
        self.address_balances_box = Box(
            style=BoxStyle.address_balances_box
        )
        self.add(
            self.address_title,
            self.address_balances_box,
            self.address_divider,
            self.transactions_title
        )
        self.app.add_background_task(
            self.get_address_balance
        )


    async def get_address_balance(self, widget):
        qr_code = self.system.qr_generate(self.address)
        balance_satoshis = self.result.get('balance')
        received_satoshis = self.result.get('received')
        balance = balance_satoshis / 100000000
        received = received_satoshis / 100000000
        sent = (received_satoshis - balance_satoshis) / 100000000
        self.total_received.text = f"{received} BTCZ"
        self.total_sent.text = f"{sent} BTCZ"
        self.final_balance.text = f"{balance} BTCZ"
        self.qrcode_image = ImageView(
            qr_code,
            style=ImageStyle.qr_code_img
        )
        self.total_received_box.add(
            self.total_received_txt,
            self.total_received
        )
        self.total_sent_box.add(
            self.total_sent_txt,
            self.total_sent
        )
        self.final_balance_box.add(
            self.final_balance_txt,
            self.final_balance
        )
        self.address_balances_list_box.add(
            self.total_received_box,
            self.total_sent_box,
            self.final_balance_box
        )
        self.address_balances_box.add(
            self.address_balances_list_box,
            self.qrcode_image
        )

        await self.get_address_txids()


    async def get_address_txids(self):
        result = await self.command.getAddressDeltas(self.address)
        if result is not None:
            self.txids_result = json.loads(result)
            self.total_txids = len(self.txids_result)
            self.number_transactions.text = str(self.total_txids)
            self.number_transactions_box.add(
                self.number_transactions_txt,
                self.number_transactions
            )
            self.address_balances_list_box.add(
                self.number_transactions_box
            )
            start_index = max(self.total_txids - 10, 0)
            for item in reversed(self.txids_result[start_index:]):
                txid = item["txid"]
                self.transaction_id = Label(
                    txid,
                    style=LabelStyle.address_transaction_id
                )
                self.transaction_box = Box(
                    style=BoxStyle.address_transaction_box
                )
                self.transaction_box.add(
                    self.transaction_id
                )
                self.add(
                    self.transaction_box
                )
            
            self.loadmore_button = Button(
                "load more",
                enabled=True,
                on_press=self.load_more_txids
            )
            self.add(
                self.loadmore_button
            )

                
    async def load_more_txids(self, button):
        transaction_boxes = []
        self.remove(
            self.loadmore_button
        )
        start_index = max(self.total_txids - 20, 0)
        for item in reversed(self.txids_result[start_index:self.total_txids]):
            txid = item["txid"]
            transaction_id = Label(
                txid,
                style=LabelStyle.address_transaction_id
            )
            transaction_box = Box(
                style=BoxStyle.address_transaction_box
            )
            transaction_box.add(
                transaction_id
            )
            transaction_boxes.append(transaction_box)
            
        for box in transaction_boxes:
            self.add(box)

        self.total_txids -= 10
        if self.total_txids > 0:
            self.add(self.loadmore_button)        