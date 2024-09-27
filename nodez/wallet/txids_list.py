
import os
import json
from datetime import datetime
import operator
import asyncio

from toga import (
    App,
    Box,
    Label,
    Button,
    ImageView,
    Icon
)
from toga.widgets.base import Widget
from typing import Iterable
from toga.constants import HIDDEN

from ..client import RPCRequest
from ..command import ClientCommands
from ..system import SystemOp

from ..insight.explorer import ExplorerWindow

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle
from .styles.label import LabelStyle


class AllTransactions(Box):
    def __init__(
            self,
            app:App,
            explorer_button,
            id: str | None = None,
            style = None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.wallet_main_box
        super().__init__(id, style, children)
        self.app = app
        self.explorer_button = explorer_button
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)

        self.transactions_count = 18
        self.transactions_from = 0

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')

        self.loading_icon = ImageView(
            ("icons/loading_tx.gif"),
            style=ImageStyle.loading_icon
        )
        self.loading_box = Box(
            style=BoxStyle.loading_box
        )
        self.txids_list_box = Box(
            style=BoxStyle.txids_list_box
        )
        self.loading_box.add(
            self.loading_icon
        )
        self.no_transactions_txt = Label(
            "No Transactions !",
            style=LabelStyle.no_transactions_txt
        )

        self.app.add_background_task(
            self.get_transactions_list
        )
        self.app.add_background_task(
            self.add_navigation_buttons
        )

    
    async def get_transactions_list(self, widget):
        if os.path.exists(self.db_path):
            transactions_data = self.client.listTransactions(
                self.transactions_count,
                self.transactions_from
            )
        else:
            transactions_data = await self.command.listTransactions(
                self.transactions_count,
                self.transactions_from
            )
            if isinstance(transactions_data, str):
                transactions_data = json.loads(transactions_data)
        if transactions_data:
            sorted_transactions = sorted(
                transactions_data,
                key=operator.itemgetter('timereceived'),
                reverse=True
            )
            await self.add_transactions_list(sorted_transactions)
        else:
            self.txids_list_box.add(
                self.no_transactions_txt
            )
            self.add(
                self.txids_list_box
            )



    async def add_transactions_list(self, sorted_transactions):
        for data in sorted_transactions:
            address = data.get("address", "Shielded")
            category = data["category"]
            amount = self.system.format_balance(data["amount"])
            timereceived = data["timereceived"]
            formatted_date_time = datetime.fromtimestamp(timereceived).strftime("%Y-%m-%d %H:%M:%S")
            txid = data["txid"]
            if category == "send":
                cash_icone = ImageView(
                    "icons/cashout.png",
                    style=ImageStyle.cash_icon
                )
            else:
                cash_icone = ImageView(
                    "icons/cashin.png",
                    style=ImageStyle.cash_icon
                )
            transaction_address = Label(
                address,
                style=LabelStyle.transaction_address
            )
            transaction_amount = Label(
                f"{amount} BTCZ",
                style=LabelStyle.transaction_amount
            )
            time_received = Label(
                formatted_date_time,
                style=LabelStyle.time_received
            )
            explorer_button = Button(
                icon=Icon("icons/explorer_txid"),
                style=ButtonStyle.explorer_button,
                enabled=True,
                on_press=lambda widget, txid=txid: asyncio.create_task(self.transaction_window(txid))
            )
            transaction_address_box = Box(
                style=BoxStyle.transaction_address_box
            )
            transaction_box = Box(
                style=BoxStyle.transaction_box
            )
            amount_box = Box(
                style=BoxStyle.transaction_amount_box
            )
            timereceived_box = Box(
                style=BoxStyle.transaction_time_box
            )
            transaction_address_box.add(
                transaction_address
            )
            amount_box.add(
                transaction_amount
            )
            timereceived_box.add(
                time_received
            )
            transaction_box.add(
                cash_icone,
                transaction_address_box,
                amount_box,
                timereceived_box,
                explorer_button
            )
            self.txids_list_box.add(
                transaction_box
            )
            self.add(
                self.txids_list_box
            )


    
    async def add_navigation_buttons(self, widget):
        await asyncio.sleep(1)
        self.previous_button = Button(
            "<",
            style=ButtonStyle.previous_button,
            on_press=self.previous_page
        )
        self.next_button = Button(
            ">",
            style=ButtonStyle.next_button,
            on_press=self.next_page
        )
        self.navigation_buttons_box = Box(
            style=BoxStyle.navigation_buttons_box
        )
        self.navigation_box = Box(
            style=BoxStyle.navigation_box
        )
        self.navigation_buttons_box.add(
            self.previous_button,
            self.next_button
        )
        self.navigation_box.add(
            self.navigation_buttons_box
        )
        self.add(
            self.navigation_box
        )


    async def next_page(self, button):
        self.previous_button.enabled = False
        self.next_button.enabled = False
        self.transactions_from = self.transactions_from + self.transactions_count
        self.txids_list_box.clear()
        self.txids_list_box.add(
            self.loading_box
        )
        await asyncio.sleep(1.5)
        self.txids_list_box.clear()
        await self.get_transactions_list(None)
        if self.transactions_from >= 0:
            self.previous_button.enabled = True
        self.next_button.enabled = True


    async def previous_page(self, button):
        self.previous_button.enabled = False
        self.next_button.enabled = False
        if self.transactions_from <= 0:
            self.previous_button.enabled = False
            self.next_button.enabled = True
            return
        self.transactions_from = self.transactions_from - self.transactions_count
        self.txids_list_box.clear()
        self.txids_list_box.add(
            self.loading_box
        )
        await asyncio.sleep(1.5)
        self.txids_list_box.clear()
        await self.get_transactions_list(None)
        self.previous_button.enabled = True
        self.next_button.enabled = True


    async def transaction_window(self, txid):
        active_windows = list(self.app.windows)
        for explorer_window in active_windows:
            if explorer_window.title == "Insight Explorer":
                explorer_window.close()
        self.explorer_button.style.visibility = HIDDEN
        self.explorer_window = ExplorerWindow(
            self.app,
            self.explorer_button,
            txid
        )
        self.explorer_window.explorer_input.value = txid
        await self.explorer_window.verify_input(txid)
        self.explorer_window.show()
                