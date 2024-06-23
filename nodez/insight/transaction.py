import json
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

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..command import ClientCommands


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

        self.transaction_title = Label(
            "Transaction",
            style=LabelStyle.transaction_title
        )
        self.transaction_id_txt = Label(
            "Transaction ID :",
            style=LabelStyle.transcation_id_txt
        )
        self.transaction_id = Label(
            "",
            style=LabelStyle.transcation_id
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
            style=LabelStyle.received_time_txt
        )
        self.received_time = Label(
            "",
            style=LabelStyle.received_time
        )
        self.received_time_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.mined_time_txt = Label(
            "Mined :",
            style=LabelStyle.mined_time_txt
        )
        self.mined_time = Label(
            "",
            style=LabelStyle.mined_time
        )
        self.mined_time_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.blockhash_txt = Label(
            "In Block :",
            style=LabelStyle.blockhash_txt
        )
        self.blockhash = Label(
            "",
            style=LabelStyle.blockhash
        )
        self.blockhash_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.version_txt = Label(
            "Version :",
            style=LabelStyle.version_txt
        )
        self.version = Label(
            "",
            style=LabelStyle.version
        )
        self.version_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.overwintered_txt = Label(
            "Overwintered :",
            style=LabelStyle.overwintered_txt
        )
        self.overwintered = Label(
            "",
            style=LabelStyle.overwintered
        )
        self.overwintered_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.versiongroupid_txt = Label(
            "VersionGroupId :",
            style=LabelStyle.versiongroupid_txt
        )
        self.versiongroupid = Label(
            "",
            style=LabelStyle.versiongroupid
        )
        self.versiongroupid_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.expiryheight_txt = Label(
            "Expiry Height :",
            style=LabelStyle.expiryheight_txt
        )
        self.expiryheight = Label(
            "",
            style=LabelStyle.expiryheight
        )
        self.expiryheight_box = Box(
            style=BoxStyle.transaction_info_box
        )
        self.coinbase_txt = Label(
            "Coinbase :",
            style=LabelStyle.coinbase_txt
        )
        self.coinbase = Label(
            "",
            style=LabelStyle.coinbase
        )
        self.coinbase_box = Box(
            style=BoxStyle.transaction_info_box
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
        )

        self.app.add_background_task(
            self.get_txid_info
        )

    async def get_txid_info(self, widget):
        txid = self.result.get('txid')
        received = self.result.get('time')
        blocktime = self.result.get('blocktime')
        formatted_received = datetime.fromtimestamp(received).strftime("%Y-%m-%d %H:%M:%S")
        formatted_blocktime = datetime.fromtimestamp(blocktime).strftime("%Y-%m-%d %H:%M:%S")
        blockhash = self.result.get('blockhash')
        version = self.result.get('version')
        overwintered = self.result.get('overwintered')
        versiongroupid = self.result.get('versiongroupid')
        expiryheight = self.result.get('expiryheight')
        coinbase = self.result.get('vin', [])[0].get('coinbase')
        self.transaction_id.text = txid
        self.received_time.text = formatted_received
        self.mined_time.text = formatted_blocktime
        self.blockhash.text = blockhash
        self.version.text = version
        self.overwintered.text = overwintered
        self.versiongroupid.text = f"0x{versiongroupid}"
        self.expiryheight.text = expiryheight
        self.coinbase.text = f"{coinbase[:60]}..."
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



