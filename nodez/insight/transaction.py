
import asyncio
from datetime import datetime
from typing import Iterable

from toga import (
    App,
    Box,
    Label,
    Divider
)
from toga.widgets.base import Widget
from toga.constants import Direction
from toga.colors import RED, GREEN

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..command import ClientCommands
from ..system import SystemOp


class Transaction(Box):
    def __init__(
            self,
            app:App,
            result: str | None = None,
            id: str | None = None,
            style= None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.transaction_info
        super().__init__(id, style, children)
        self.app = app
        self.result = result
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)

        self.transaction_title = Label(
            "- Transaction -",
            style=LabelStyle.transaction_title
        )
        self.transaction_id_txt = Label(
            "Transaction ID :",
            style=LabelStyle.transaction_id_txt
        )
        self.transaction_id = Label(
            "",
            style=LabelStyle.transaction_id
        )
        self.transaction_id_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.transaction_divider = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.transaction_divider
        )
        self.received_time_txt = Label(
            "Received :",
            style=LabelStyle.transaction_received_time_txt
        )
        self.received_time = Label(
            "",
            style=LabelStyle.transaction_received_time
        )
        self.received_time_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.mined_time_txt = Label(
            "Mined :",
            style=LabelStyle.transaction_mined_time_txt
        )
        self.mined_time = Label(
            "",
            style=LabelStyle.transaction_mined_time
        )
        self.mined_time_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.blockhash_txt = Label(
            "In Block :",
            style=LabelStyle.transaction_blockhash_txt
        )
        self.blockhash = Label(
            "",
            style=LabelStyle.transaction_blockhash
        )
        self.blockhash_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.version_txt = Label(
            "Version :",
            style=LabelStyle.transaction_version_txt
        )
        self.version = Label(
            "",
            style=LabelStyle.transaction_version
        )
        self.version_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.overwintered_txt = Label(
            "Overwintered :",
            style=LabelStyle.transaction_overwintered_txt
        )
        self.overwintered = Label(
            "",
            style=LabelStyle.transaction_overwintered
        )
        self.overwintered_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.versiongroupid_txt = Label(
            "VersionGroupId :",
            style=LabelStyle.transaction_versiongroupid_txt
        )
        self.versiongroupid = Label(
            "",
            style=LabelStyle.transaction_versiongroupid
        )
        self.versiongroupid_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.expiryheight_txt = Label(
            "Expiry Height :",
            style=LabelStyle.transaction_expiryheight_txt
        )
        self.expiryheight = Label(
            "",
            style=LabelStyle.transaction_expiryheight
        )
        self.expiryheight_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.coinbase_txt = Label(
            "Coinbase :",
            style=LabelStyle.transaction_coinbase_txt
        )
        self.coinbase = Label(
            "",
            style=LabelStyle.transaction_coinbase
        )
        self.coinbase_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.transaction_details_box = Box(
            style=BoxStyle.transaction_details_box
        )
        self.transaction_id_box.add(
            self.transaction_id_txt
        )
        self.received_time_box.add(
            self.received_time_txt
        )
        self.mined_time_box.add(
            self.mined_time_txt
        )
        self.blockhash_box.add(
            self.blockhash_txt
        )
        self.version_box.add(
            self.version_txt
        )
        self.overwintered_box.add(
            self.overwintered_txt
        )
        self.versiongroupid_box.add(
            self.versiongroupid_txt
        )
        self.expiryheight_box.add(
            self.expiryheight_txt
        )
        self.coinbase_box.add(
            self.coinbase_txt
        )

        self.add(
            self.transaction_title,
            self.transaction_id_box,
            self.received_time_box,
            self.mined_time_box,
            self.blockhash_box,
            self.version_box,
            self.overwintered_box,
            self.versiongroupid_box,
            self.expiryheight_box,
            self.coinbase_box,
            self.transaction_divider,
            self.transaction_details_box
        )

        self.app.add_background_task(
            self.get_txid_info
        )

    async def get_txid_info(self, widget):
        txid = self.result.get('txid')
        received = self.result.get('time')
        if received is not None:
            formatted_received = datetime.fromtimestamp(received).strftime("%Y-%m-%d %H:%M:%S")
            self.received_time.text = formatted_received
        blocktime = self.result.get('blocktime')
        if blocktime is not None:
            formatted_blocktime = datetime.fromtimestamp(blocktime).strftime("%Y-%m-%d %H:%M:%S")
            self.mined_time.text = formatted_blocktime
        blockhash = self.result.get('blockhash')
        version = self.result.get('version')
        overwintered = self.result.get('overwintered')
        versiongroupid = self.result.get('versiongroupid', None)
        if versiongroupid is not None:
            self.versiongroupid.text = f"0x{versiongroupid}"
        expiryheight = self.result.get('expiryheight')
        coinbase = self.result.get('vin', [])[0].get('coinbase', None)
        if coinbase is not None:
            self.coinbase.text = f"{coinbase[:60]}..."
        self.transaction_id.text = txid
        self.blockhash.text = blockhash
        self.version.text = version
        self.overwintered.text = overwintered
        self.expiryheight.text = expiryheight
        self.transaction_id_box.add(
            self.transaction_id
        )
        self.received_time_box.add(
            self.received_time
        )
        self.mined_time_box.add(
            self.mined_time
        )
        self.blockhash_box.add(
            self.blockhash
        )
        self.version_box.add(
            self.version
        )
        self.overwintered_box.add(
            self.overwintered
        )
        self.versiongroupid_box.add(
            self.versiongroupid
        )
        self.expiryheight_box.add(
            self.expiryheight
        )
        self.coinbase_box.add(
                self.coinbase
            )
        await self.get_txid_details()


    async def get_txid_details(self):
        await asyncio.sleep(1)
        self.transaction_deatils_txt = Label(
            "Transaction Details",
            style=LabelStyle.transaction_details_title
        )
        self.confirmations = Label(
            "",
            style=LabelStyle.transaction_confirmations
        )
        self.value = Label(
            "",
            style=LabelStyle.transaction_value
        )
        self.addresses_box = Box(
            style=BoxStyle.addresses_box
        )
        self.vin_address_box = Box(
            style=BoxStyle.transaction_address_box
        )
        self.vout_address_box = Box(
            style=BoxStyle.transaction_address_box
        )
        self.confirmations_box = Box(
            style=BoxStyle.confirmations_box
        )
        vin = self.result.get('vin', [])
        for data in vin:
            vin_value = data.get('value')
            vin_address = data.get('address')
            if vin_value and vin_address:
                self.vin_address = Label(
                    f"{vin_address}  {self.system.format_balance(vin_value)} BTCZ",
                    style=LabelStyle.transaction_vin_address
                )
            else:
                self.vin_address = Label(
                    "No Inputs (Newly Generated Coins)",
                    style=LabelStyle.transaction_vin_address
                )
            self.vin_address_box.add(
                self.vin_address
            )
        vout = self.result.get('vout', [])
        total_value = sum(vout_data.get('value', 0) for vout_data in vout)
        for data in vout:
            script_pubkey = data.get('scriptPubKey', {})
            vout_value = data.get('value')
            vout_addresses = script_pubkey.get('addresses', [])
            if isinstance(vout_addresses, list) and len(vout_addresses) == 1:
                vout_address = vout_addresses[0]
            else:
                vout_address = ', '.join(vout_addresses) if vout_addresses else 'Unknown'
            self.vout_address = Label(
                f"{vout_address}  {self.system.format_balance(vout_value)} BTCZ",
                style=LabelStyle.transaction_vout_address
            )
            self.vout_address_box.add(self.vout_address)
        confirmations = self.result.get('confirmations', '0')
        if confirmations == "0" or confirmations is None:
            background_color = RED
            self.confirmations.text = f"Unconfirmed Tx"
        else:
            background_color = GREEN
            self.confirmations.text = f"Confirmations : {confirmations}"
        self.value.text = f"{self.system.format_balance(total_value)} BTCZ"
        self.confirmations.style.background_color = background_color
        self.confirmations_box.add(
            self.confirmations,
            self.value
        )
        self.addresses_box.add(
            self.vin_address_box,
            self.vout_address_box
        )
        self.transaction_details_box.add(
            self.transaction_deatils_txt,
            self.addresses_box,
            self.confirmations_box
        )



