import os
import asyncio
import json
import operator
from datetime import datetime

from toga import (
    App,
    Box,
    Button,
    Label,
    ImageView,
    Icon
)
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.image import ImageStyle

from ..client import RPCRequest
from ..commands import ClientCommands


class LastTransactions(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style= None,
        children: list[Widget] | None = None
    ):
        style = BoxStyle.cash_transaction_box
        super().__init__(id, style, children)
        self.app = app
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        
        self.app.add_background_task(
            self.get_last_transactions
        )
        
    async def get_last_transactions(self, widget):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            transactions_data = self.client.listTransactions()
        else:
            transactions_data = await self.command.listTransactions()
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
                amount = data["amount"]
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
                    f"{amount:.8f} BTCZ",
                    style=LabelStyle.transaction_amount
                )
                time_received = Label(
                    formatted_date_time,
                    style=LabelStyle.time_received
                )
                transaction_address_box = Box(
                    style=BoxStyle.transaction_address_box
                )
                transaction_box = Box(
                    style=BoxStyle.transaction_box
                )
                transaction_address_box.add(
                    transaction_address
                )
                transaction_box.add(
                    cash_icone,
                    transaction_address_box,
                    transaction_amount,
                    time_received
                )
                self.add(
                    transaction_box
                )