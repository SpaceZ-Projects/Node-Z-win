import asyncio
import os
import json
from datetime import datetime
from typing import Iterable

from toga import (
    App,
    Box,
    Button,
    Label,
    ImageView,
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
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.getAddressDeltas(self.address)
        else:
            result = await self.command.getAddressDeltas(self.address)
            result = json.loads(result)
        if result is not None:
            self.txids_result = result
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
            print(start_index)
            for item in reversed(self.txids_result[start_index:self.total_txids]):
                txid = item["txid"]
                transaction_id_label = Label(
                    txid,
                    style=LabelStyle.address_transaction_id
                )
                vin_address_box = Box(
                    style=BoxStyle.transaction_address_box
                )
                vout_address_box = Box(
                    style=BoxStyle.transaction_address_box
                )
                addresses_box = Box(
                    style=BoxStyle.addresses_box
                )
                confirmations = Label(
                    "",
                    style=LabelStyle.transaction_confirmations
                )
                value = Label(
                    "",
                    style=LabelStyle.transaction_value
                )
                confirmations_box = Box(
                    style=BoxStyle.confirmations_box
                )
                transaction_box = Box(
                    style=BoxStyle.address_transaction_box
                )
                transaction_box.add(transaction_id_label)
                if os.path.exists(db_path):
                    txid_details = self.client.getRawTransaction(txid)
                else:
                    txid_details = await self.command.getRawTransaction(txid)
                    txid_details = json.loads(txid_details)
                if txid_details:
                    vin = txid_details.get('vin', [])
                    for data in vin:
                        vin_value = data.get('value')
                        vin_address = data.get('address')
                        if vin_value and vin_address:
                            vin_address_label = Label(
                                f"{vin_address}  {self.system.format_balance(vin_value)} BTCZ",
                                style=LabelStyle.transaction_vin_address
                            )
                        else:
                            vin_address_label = Label(
                                "No Inputs (Newly Generated Coins)",
                                style=LabelStyle.transaction_vin_address
                            )
                        vin_address_box.add(
                            vin_address_label
                        )
                    vout = txid_details.get('vout', [])
                    total_value = sum(vout_data.get('value', 0) for vout_data in vout)
                    for data in vout:
                        script_pubkey = data.get('scriptPubKey', {})
                        vout_value = data.get('value')
                        vout_addresses = script_pubkey.get('addresses', [])
                        if isinstance(vout_addresses, list) and len(vout_addresses) == 1:
                            vout_address = vout_addresses[0]
                        else:
                            vout_address = ', '.join(vout_addresses) if vout_addresses else 'Unknown'
                        vout_address_label = Label(
                            f"{vout_address}  {self.system.format_balance(vout_value)} BTCZ",
                            style=LabelStyle.transaction_vout_address
                        )
                        vout_address_box.add(
                            vout_address_label
                        )
                    confirmations_result = txid_details.get('confirmations', '0')
                    confirmations.text = f"Confirmations : {confirmations_result}"
                    confirmations.style.background_color = GREEN
                    value.text = f"{self.system.format_balance(total_value)} BTCZ"
                    addresses_box.add(
                        vin_address_box,
                        vout_address_box
                    )
                    confirmations_box.add(
                        confirmations,
                        value
                    )
                    transaction_box.add(
                        addresses_box,
                        confirmations_box
                    )
                self.add(transaction_box)
            self.loadmore_button = Button(
                "load more",
                enabled=True,
                on_press=self.load_more_txids
            )
            self.add(self.loadmore_button)
        self.total_txids -= 10

                
    async def load_more_txids(self, button):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        self.remove(self.loadmore_button)
        start_index = max(self.total_txids - 20, 0)
        for item in reversed(self.txids_result[start_index:self.total_txids]):
            txid = item["txid"]
            if os.path.exists(db_path):
                txid_details = self.client.getRawTransaction(txid)
            else:
                txid_details = await self.command.getRawTransaction(txid)
                txid_details = json.loads(txid_details)
            if txid_details:
                vin_address_box = Box(
                    style=BoxStyle.transaction_address_box
                )
                vout_address_box = Box(
                    style=BoxStyle.transaction_address_box
                )
                addresses_box = Box(
                    style=BoxStyle.addresses_box
                )
                confirmations = Label(
                    "",
                    style=LabelStyle.transaction_confirmations
                )
                value = Label(
                    "",
                    style=LabelStyle.transaction_value
                )
                confirmations_box = Box(
                    style=BoxStyle.confirmations_box
                )
                
                vin = txid_details.get('vin', [])
                for data in vin:
                    vin_value = data.get('value')
                    vin_address = data.get('address')
                    if vin_value and vin_address:
                        vin_address_label = Label(
                            f"{vin_address}  {self.system.format_balance(vin_value)} BTCZ",
                            style=LabelStyle.transaction_vin_address
                        )
                    else:
                        vin_address_label = Label(
                            "No Inputs (Newly Generated Coins)",
                            style=LabelStyle.transaction_vin_address
                        )
                    vin_address_box.add(vin_address_label)
                
                vout = txid_details.get('vout', [])
                total_value = sum(vout_data.get('value', 0) for vout_data in vout)
                for data in vout:
                    script_pubkey = data.get('scriptPubKey', {})
                    vout_value = data.get('value')
                    vout_addresses = script_pubkey.get('addresses', [])
                    if isinstance(vout_addresses, list) and len(vout_addresses) == 1:
                        vout_address = vout_addresses[0]
                    else:
                        vout_address = ', '.join(vout_addresses) if vout_addresses else 'Unknown'
                    vout_address_label = Label(
                        f"{vout_address}  {self.system.format_balance(vout_value)} BTCZ",
                        style=LabelStyle.transaction_vout_address
                    )
                    vout_address_box.add(
                        vout_address_label
                    )
                confirmations_result = txid_details.get('confirmations', '0')
                confirmations.text = f"Confirmations : {confirmations_result}"
                confirmations.style.background_color = GREEN
                value.text = f"{self.system.format_balance(total_value)} BTCZ"
                addresses_box.add(
                    vin_address_box,
                    vout_address_box
                )
                confirmations_box.add(
                    confirmations,
                    value
                )
                transaction_id_label = Label(
                    txid,
                    style=LabelStyle.address_transaction_id
                )
                transaction_box = Box(
                    style=BoxStyle.address_transaction_box
                )
                transaction_box.add(
                    transaction_id_label,
                    addresses_box,
                    confirmations_box)
                self.add(transaction_box)
            
            await asyncio.sleep(0.1)
        
        self.total_txids -= 10
        if self.total_txids > 10:
            self.add(self.loadmore_button)        