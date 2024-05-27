import asyncio
import os
import json
from toga import (
    App,
    Box,
    Label,
    Button,
    Divider,
    ImageView,
    Icon
)
from toga.widgets.base import Widget
from toga.constants import Direction

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.divider import DividerStyle
from .styles.label import LabelStyle

from .request import RPCRequest, get_btcz_price
from .client import ClientCommands
from .command import Toolbar


class MainMenu(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style=BoxStyle.home_main_box
        super().__init__(id, style, children)
        self.app = app
        self.request = RPCRequest(self.app)
        self.client = ClientCommands(self.app)
        self.commands = Toolbar(self.app)
        
        self.cash_button = Button(
            icon=Icon("icones/cash"),
            style=ButtonStyle.menu_button
        )
        self.wallet_buuton = Button(
            icon=Icon("icones/wallet"),
            style=ButtonStyle.menu_button
        )
        self.explorer_button = Button(
            icon=Icon("icones/explorer"),
            style=ButtonStyle.menu_button
        )
        self.message_button = Button(
            icon=Icon("icones/message"),
            style=ButtonStyle.menu_button
        )
        self.tools_button = Button(
            icon=Icon("icones/tools"),
            style=ButtonStyle.menu_button
        )
        self.buttons_box = Box(
            style=BoxStyle.home_buttons_box
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.home_divider_top
        )
        self.divider_bottom = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.home_divider_bottom
        )
        self.total_balances_txt = Label(
            "Total Balance :",
            style=LabelStyle.home_total_balances_txt
        )
        self.total_balances = Label(
            "_._",
            style=LabelStyle.home_total_balances
        )
        self.transparent_balance_txt = Label(
            "T :",
            style=LabelStyle.home_transparent_balance_txt
        )
        self.transparent_balance = Label(
            "_._",
            style=LabelStyle.home_transparent_balance
        )
        self.private_balance_txt = Label(
            "Z :",
            style=LabelStyle.home_private_balance_txt
        )
        self.private_balance = Label(
            "_._",
            style=LabelStyle.home_private_balance
        )
        self.btcz_coin = ImageView(
            "resources/btcz_coin.gif"
        )
        self.price_txt = Label(
            "BTCZ Price :",
            style=LabelStyle.home_price_txt
        )
        self.price_value = Label(
            "$ _._"
        )
        self.chain_txt = Label(
            "Chain :",
            style=LabelStyle.home_chain_txt
        )
        self.chain_value = Label(
            "NaN",
            style=LabelStyle.home_chain_value
        )
        self.blocks_txt = Label(
            "Blocks :",
            style=LabelStyle.home_blocks_txt
        )
        self.blocks_value = Label(
            "NaN",
            style=LabelStyle.home_blocks_value
        )
        self.sync_txt = Label(
            "Sync :",
            style=LabelStyle.home_sync_txt
        )
        self.sync_value = Label(
            "NaN",
            style=LabelStyle.home_sync_value
        )
        self.dep_text = Label(
            "Dep :",
            style=LabelStyle.home_dep_txt
        )
        self.dep_value = Label(
            "NaN",
            style=LabelStyle.home_dep_value
        )
        self.total_balances_box = Box(
            style=BoxStyle.home_total_balances_box
        )
        self.balances_box = Box(
            style=BoxStyle.home_balances_box
        )
        self.price_box = Box(
            style=BoxStyle.home_price_box
        )
        self.blockchain_info_box = Box(
            style=BoxStyle.home_blockchain_info_box
        )
        self.buttons_box.add(
            self.cash_button,
            self.wallet_buuton,
            self.explorer_button,
            self.message_button,
            self.tools_button
        )
        self.total_balances_box.add(
            self.total_balances_txt,
            self.total_balances,
            self.btcz_coin
        )
        self.balances_box.add(
            self.transparent_balance_txt,
            self.transparent_balance,
            self.private_balance_txt,
            self.private_balance
        )
        self.price_box.add(
            self.price_txt,
            self.price_value
        )
        self.blockchain_info_box.add(
            self.chain_txt,
            self.chain_value,
            self.blocks_txt,
            self.blocks_value,
            self.sync_txt,
            self.sync_value,
            self.dep_text,
            self.dep_value
        )
        self.add(
            self.buttons_box,
            self.divider_top,
            self.total_balances_box,
            self.balances_box,
            self.divider_bottom,
            self.price_box,
            self.blockchain_info_box
        )
        self.app.add_background_task(
            self.update_total_balances
        )
        self.app.add_background_task(
            self.update_price
        )
        self.app.add_background_task(
            self.update_blockchain_info
        )

        
    async def update_total_balances(self, widget):
        while True:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                balances = self.request.z_getTotalBalance()
                if balances is not None:
                    total = self.format_balance(
                        float(balances["total"])
                    )
                    transparent = self.format_balance(
                        float(balances["transparent"])
                    )
                    private = self.format_balance(
                        float(balances["private"])
                    )
            if not os.path.exists(db_path):
                balances = await self.client.z_getTotalBalance()
                if balances is not None:
                    if isinstance(balances, str):
                        balances = json.loads(balances)
                    total = self.format_balance(
                        float(balances.get('total'))
                    )
                    transparent = self.format_balance(
                        float(balances.get('transparent'))
                    )
                    private = self.format_balance(
                        float(balances.get('private'))
                    )
            self.total_balances.text = f"{total}"
            self.transparent_balance.text = f"{transparent}"
            self.private_balance.text = f"{private}"
            await asyncio.sleep(5)
                
            
    async def update_price(self, widget):
        while True:
            price = await get_btcz_price()
            if price is not None:
                price_format = self.format_price(price)
                self.price_value.text = f"$ {price_format}"
            else:
                self.price_value.text = "$ NaN"
            await asyncio.sleep(600)
            
    
    async def update_blockchain_info(self, widget):
        while True:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                info = self.request.getBlockchainInfo()
                if info is not None:
                    chain = info["chain"]
                    blocks = info["blocks"]
                    sync = info["verificationprogress"]
                deprecation = self.request.getDeprecationInfo()
                if deprecation is not None:
                    dep = deprecation["deprecationheight"]
            if not os.path.exists(db_path):
                info = await self.client.getBlockchainInfo()
                if isinstance(info, str):
                    info = json.loads(info)
                    if info is not None:
                        chain = info.get('chain')
                        blocks = info.get('blocks')
                        sync = info.get('verificationprogress')
                deprecation = await self.client.getDeprecationInfo()
                if isinstance(deprecation, str):
                    deprecation = json.loads(deprecation)
                    if deprecation is not None:
                        dep = deprecation.get('deprecationheight')
            sync_percentage = sync * 100
            self.chain_value.text = f"{chain}"
            self.blocks_value.text = f"{blocks}"
            self.sync_value.text = f"%{float(sync_percentage):.2f}"
            self.dep_value.text = f"{dep}"
            await asyncio.sleep(5)
            
    
    def format_balance(self, total):
        formatted_total = '{:.8f}'.format(total)  
        parts = formatted_total.split('.')  
        integer_part = parts[0]
        decimal_part = parts[1] 

        if len(integer_part) > 4:
            digits_to_remove = len(integer_part) - 4
            formatted_decimal = decimal_part[:-digits_to_remove]
        else:
            formatted_decimal = decimal_part

        formatted_balance = integer_part + '.' + formatted_decimal
        return formatted_balance
    
    def format_price(self, price):
        if price > 0.00000001 and price < 0.0000001:
            return f"{price:.10f}"
        elif price > 0.0000001 and price < 0.000001:
            return f"{price:.9f}"
        elif price > 0.000001 and price < 0.00001:
            return f"{price:.8f}"
        elif price > 0.00001 and price < 0.0001:
            return f"{price:.7f}"
        elif price > 0.0001 and price < 0.001:
            return f"{price:.6f}"
        elif price > 0.001 and price < 0.01:
            return f"{price:.5f}"
        elif price > 0.01 and price < 0.1:
            return f"{price:.4f}"
        elif price > 0.1 and price < 1:
            return f"{price:.3f}"
        elif price > 1 and price < 10:
            return f"{price:.2f}"
        elif price > 10 and price < 100:
            return f"{price:.1f}"
        else:
            return f"{price:.0f}"