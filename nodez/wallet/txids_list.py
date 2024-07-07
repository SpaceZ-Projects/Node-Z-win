
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

        self.config_path = self.app.paths.config

        self.app.add_background_task(
            self.get_transactions_list
        )

    
    async def get_transactions_list(self, widget):
        db_path = os.path.join(self.config_path, 'config.db')
        if os.path.exists(db_path):
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
        if transactions_data is not None:
            sorted_transactions = sorted(
                transactions_data,
                key=operator.itemgetter('timereceived'),
                reverse=True
            )
            for data in sorted_transactions:
                address = data.get("address", "Shielded")
                category = data["category"]
                amount = self.system.format_balance(data["amount"])
                timereceived = data["timereceived"]
                formatted_date_time = datetime.fromtimestamp(timereceived).strftime("%Y-%m-%d %H:%M:%S")
                txid = data["txid"]
                if category == "send":
                    cash_icone = ImageView(
                        "icones/cashout.png",
                        style=ImageStyle.cash_icon
                    )
                else:
                    cash_icone = ImageView(
                        "icones/cashin.png",
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
                    icon=Icon("icones/explorer_txid"),
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
                self.add(
                    transaction_box
                )

            await asyncio.sleep(1)
            await self.add_navigation_buttons()

    
    async def add_navigation_buttons(self):
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
        self.transactions_from = self.transactions_from + self.transactions_count
        self.clear()
        await self.get_transactions_list(None)


    async def previous_page(self, button):
        if self.transactions_from <= 0:
            return
        self.transactions_from = self.transactions_from - self.transactions_count
        self.clear()
        await self.get_transactions_list(None)


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
                