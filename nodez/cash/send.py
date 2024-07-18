
import os
import asyncio
import json
import threading
from datetime import datetime
import operator
import sys

from toga import (
    App,
    Window,
    Switch,
    ScrollContainer,
    Selection,
    Divider,
    Box,
    Label,
    TextInput,
    Button,
    Icon,
    ImageView
)

from toga.colors import CYAN, YELLOW, RED, WHITE
from toga.constants import VISIBLE, HIDDEN, Direction

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle
from .styles.selection import SelectionStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from .styles.container import ContainerStyle

from ..insight.explorer import ExplorerWindow
from ..system import SystemOp
from ..client import RPCRequest
from ..command import ClientCommands



class CashWindow(Window):
    def __init__(self, app:App, window_button, explorer_button):
        super().__init__(
            title="Cash Out",
            size=(800, 650),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button
        self.explorer_button = explorer_button
        
        self.loading_icon = ImageView(
            ("icones/loading_tx.gif"),
            style=ImageStyle.loading_icon
        )
        self.loading_box = Box(
            style=BoxStyle.loading_box
        )
        self.transparent_button = Button(
            "Transparent",
            enabled=True,
            style=ButtonStyle.transparent_button,
            on_press=self.switch_to_transparent
        )
        self.shielded_button = Button(
            "Shielded",
            enabled=True,
            style=ButtonStyle.shielded_button,
            on_press=self.switch_to_shielded
        )
        self.transparent_icon = ImageView(
            "icones/transparent_txt.png",
            style=ImageStyle.transparent_icon
        )
        self.shielded_icon = ImageView(
            "icones/shielded_txt.png",
            style=ImageStyle.shielded_icon
        )
        self.select_address_txt = Label(
            "From :",
            style=LabelStyle.select_address_txt
        )
        self.select_address = Selection(
            accessor="select_address",
            enabled=True,
            style=SelectionStyle.select_address,
            on_change=self.display_address_balance
        )
        self.address_balance = Label(
            "",
            style=LabelStyle.address_balance
        )
        self.listunspent_button = Button(
            "Unspent",
            enabled=True,
            style=ButtonStyle.lisunspent_button,
            on_press=self.display_listunspent
        )
        self.to_address_txt = Label(
            "To :",
            style=LabelStyle.to_address_txt
        )
        self.to_address_input = TextInput(
            style=InputStyle.to_address_input,
            on_change=self.verify_address
        )
        self.verified_icon = ImageView(
            "icones/verified.png",
            style=ImageStyle.verified_icon
        )
        self.invalid_icon = ImageView(
            "icones/invalid.png",
            style=ImageStyle.invalid_icon
        )
        self.amount_txt = Label(
            "Amount :",
            style=LabelStyle.amount_txt
        )
        self.amount_input = TextInput(
            placeholder="0.00000000",
            style=InputStyle.amount_input,
            on_change=self.verify_balances,
            validators=[
                self.is_digit
            ]
        )
        self.max_button = Button(
            "Max",
            enabled=True,
            style=ButtonStyle.max_button,
            on_press=self.set_max_amount
        )
        self.amount_note = Label(
            "",
            style=LabelStyle.amount_note
        )
        self.fee_txt = Label(
            "TxFee :",
            style=LabelStyle.fee_txt
        )
        self.fee_input = TextInput(
            placeholder="0.00000000",
            style=InputStyle.fee_input,
            on_gain_focus=self.check_txfee,
            validators=[
                self.is_digit
            ]
        )
        self.txfee_info_txt = Label(
            "The transaction fee in BTCZ/kB",
            style=LabelStyle.txfee_info_txt
        )
        self.comment_memo_input = TextInput(
            style=InputStyle.comment_memo_input,
            on_gain_focus=self.check_comments,
            on_change=self.calculate_bytes
        )
        self.comment_memo_txt = Label(
            "Comment/Memo :",
            style=LabelStyle.comment_memo_txt
        )
        self.comment_calculate = Label(
            "0 / 512 bytes",
            style=LabelStyle.comment_calculate
        )
        self.send_button = Button(
            "Send",
            enabled=True,
            style=ButtonStyle.send_button,
            on_press=self.check_inputs_value
        )
        self.divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.send_box = Box(
            style=BoxStyle.cash_send_box
        )
        self.switch_button_box = Box(
            style=BoxStyle.switch_button_box
        )
        self.select_address_box = Box(
            style=BoxStyle.select_address_box
        )
        self.to_address_box = Box(
            style=BoxStyle.to_address_box
        )
        self.amount_box = Box(
            style=BoxStyle.amount_box
        )
        self.txfee_box = Box(
            style=BoxStyle.txfee_box
        )
        self.comment_menmo_box = Box(
            style=BoxStyle.comment_memo_box
        )
        self.buttons_box = Box(
            style=BoxStyle.buttons_box
        )
        self.last_transaction_box = Box(
            style=BoxStyle.cash_transaction_box
        )
        self.last_transaction_list = ScrollContainer(
            style=ContainerStyle.last_taransactions_list
        )
        self.main_box = Box(
            style=BoxStyle.cash_main_box
        )
        self.loading_box.add(
            self.loading_icon
        )
        self.select_address_box.add(
            self.select_address_txt
        )
        self.to_address_box.add(
            self.to_address_txt,
            self.to_address_input,
            self.invalid_icon
        )
        self.amount_box.add(
            self.amount_txt,
            self.amount_input,
            self.max_button,
            self.amount_note
        )
        self.txfee_box.add(
            self.fee_txt
        )
        self.comment_menmo_box.add(
            self.comment_memo_txt,
            self.comment_memo_input,
            self.comment_calculate
        )
        self.buttons_box.add(
            self.send_button
        )
        self.send_box.add(
            self.switch_button_box,
            self.select_address_box,
            self.to_address_box,
            self.amount_box,
            self.txfee_box,
            self.comment_menmo_box,
            self.buttons_box
        )
        self.main_box.add(
            self.send_box,
            self.divider
        )
        
        self.content = self.main_box
        self.app.add_background_task(
            self.get_addresses_list
        )
        
        
    async def get_addresses_list(self, widget):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.items = transparent_address
        
        await self.get_transactions_list()


    async def get_transactions_list(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        transactions_count = 10
        transactions_from = 0
        if os.path.exists(db_path):
            transactions_data = self.client.listTransactions(transactions_count, transactions_from)
        else:
            transactions_data = await self.command.listTransactions(transactions_count, transactions_from)
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
                self.last_transaction_box.add(
                    transaction_box
                )
        self.last_transaction_list.content = self.last_transaction_box
        self.main_box.add(
            self.last_transaction_list
        )
        await asyncio.sleep(1)
        self.display_window()
        
        
    def display_window(self):
        self.fee_input.readonly = True
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        self.select_address_box.add(
            self.select_address,
            self.address_balance,
            self.listunspent_button
        )
        self.txfee_box.add(
            self.fee_input,
            self.txfee_info_txt
        )
        self.show()


    async def display_listunspent(self, button):
        if not self.select_address.value.select_address:
            return
        address = self.select_address.value.select_address
        if address.startswith("z"):
            await self.get_listunspent_zaddr(address)
        elif address.startswith("t"):
            await self.get_listunspent_taddr(address)


    async def get_listunspent_zaddr(self, address):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.z_listUnspent(address)
        else:
            result = await self.command.z_listUnspent(address)
            result = json.loads(result)
        if result is not None:
            formatted_result = ""
            for data in result:
                txid = data['txid']
                outindex = data['outindex']
                confirmations = data['confirmations']
                spendable = data['spendable']
                address = data['address']
                amount = data['amount']
                change = data['change']

                formatted_result += (
                    f"Txid: {txid}\n"
                    f"Outindex: {outindex}\n"
                    f"Confirmations: {confirmations}\n"
                    f"Spendable: {spendable}\n"
                    f"Address: {address}\n"
                    f"Amount: {amount}\n"
                    f"Change: {change}\n\n"
                )
            
            self.info_dialog("List unspent", formatted_result)
        else:
            self.info_dialog("List unspent", "No unspent outputs found.")


    async def get_listunspent_taddr(self, address):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            result = self.client.listUnspent(address)
        else:
            result = await self.command.listUnspent(address)
            result = json.loads(result)
        if result is not None:
            formatted_result = ""
            for data in result:
                txid = data['txid']
                vout = data['vout']
                generated = data['generated']
                address = data['address']
                scriptpubkey = data['scriptPubKey']
                amount = data['amount']
                confirmations = data['confirmations']
                spendable = data['spendable']


                formatted_result += (
                    f"Txid: {txid}\n"
                    f"Vout: {vout}\n"
                    f"Confirmations: {confirmations}\n"
                    f"Spendable: {spendable}\n"
                    f"Address: {address}\n"
                    f"Amount: {amount}\n"
                    f"Generated: {generated}\n\n"
                    f"scriptPubKey: {scriptpubkey}\n\n"
                )
            
            self.info_dialog("List unspent", formatted_result)
        else:
            self.info_dialog("List unspent", "No unspent outputs found.")

        

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
        
        
    async def set_max_amount(self, button):
        if self.select_address.value.select_address:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            selected_address = self.select_address.value.select_address
            if selected_address == "Main Account":
                if os.path.exists(db_path):
                    balances = self.client.z_getTotalBalance()
                    transparent = balances["transparent"]
                else:
                    balances = await self.command.z_getTotalBalance()   
                    balances = json.loads(balances)
                    transparent = balances.get("transparent")  
                if transparent is not None:
                    amount = float(transparent) - 0.0001
                    self.amount_input.value = f"{amount:.8f}"
            else:
                if os.path.exists(db_path):
                    balance = self.client.z_getBalance(selected_address)
                else:
                    balance = await self.command.z_getBalance(selected_address)
                if balance is not None:
                    amount = float(balance) - float(self.fee_input.value)
                    self.amount_input.value = f"{amount:.8f}"
                    
        
        
    async def switch_to_transparent(self, button):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.style.color = YELLOW
        self.select_address.items = transparent_address
        self.send_button.style.background_color = YELLOW
        self.switch_button_box.remove(
            self.transparent_button,
            self.shielded_icon
        )
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        
    async def switch_to_shielded(self, button):
        self.transaction_mode = "shielded"
        shielded_address = await self.get_shielded_addresses()
        self.select_address.style.color = CYAN
        self.select_address.items = shielded_address
        self.send_button.style.background_color = CYAN
        self.switch_button_box.remove(
            self.transparent_icon,
            self.shielded_button
        )
        self.switch_button_box.add(
            self.transparent_button,
            self.shielded_icon
        )
        
        
    async def get_transparent_addresses(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            addresses_data = self.client.getAddressesByAccount()
        else:
            addresses_data = await self.command.getAddressesByAccount()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            address_items = [("Main Account")] + [(address_info, address_info) for address_info in addresses_data]
        else:
            address_items = [("Main Account")]
        return address_items
    
    
    async def get_shielded_addresses(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            addresses_data = self.client.z_listAddresses()
        else:
            addresses_data = await self.command.z_listAddresses()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            if len(addresses_data) == 1:
                address_items = [(addresses_data[0], addresses_data[0])]
            else:
                address_items = [(address, address) for address in addresses_data]
        else:
            address_items = []
        return address_items
    
    
    async def display_address_balance(self, selection):
        if selection.value is None:
            self.address_balance.style.visibility = HIDDEN
            return
        if self.to_address_input.value is not None:
            self.to_address_input.value = ""
        selected_address = selection.value.select_address
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if selected_address != "Main Account":
            self.to_address_input.placeholder = "paste T or Z address"
            self.comment_memo_input.placeholder = "memo"
            if os.path.exists(db_path):
                balance = self.client.z_getBalance(selected_address)
            else:
                balance = await self.command.z_getBalance(selected_address)
            if balance is not None:
                self.address_balance.text = f"{float(balance):.8f} BTCZ"
                self.address_balance.style.visibility = VISIBLE
            else:
                self.address_balance.style.visibility = HIDDEN
            if not self.fee_input.value:
                await self.check_txfee(selection)        
        elif selected_address == "Main Account":
            if self.fee_input.value is not None:
                self.fee_input.value = ""
            self.comment_memo_input.placeholder = "comment"
            self.to_address_input.placeholder = "paste T address"
            if os.path.exists(db_path):
                balances = self.client.z_getTotalBalance()
                transparent = balances["transparent"]
            else:
                balances = await self.command.z_getTotalBalance()
                balances = json.loads(balances)
                transparent = balances.get('transparent')
            if transparent:
                self.address_balance.text = f"{float(transparent):.8f} BTCZ"
                self.address_balance.style.visibility = VISIBLE
            else:
                self.address_balance.style.visibility = HIDDEN
        else:
            self.address_balance.style.visibility = HIDDEN
            
    
    async def verify_address(self, input):
        selected_address = self.select_address.value.select_address
        address = self.to_address_input.value
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        if not address:
            self.verified_icon.style.visibility = HIDDEN
            self.invalid_icon.style.visibility = HIDDEN
            return
        if selected_address == "Main Account" and address.startswith("t"):
            if os.path.exists(db_path):
                result = self.client.validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        elif selected_address != "Main Account" and address.startswith("t"):
            if os.path.exists(db_path):
                result = self.client.validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        elif selected_address != "Main Account" and address.startswith("z"):
            if os.path.exists(db_path):
                result = self.client.z_validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.z_validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        else:
            self.verified_icon.style.visibility = HIDDEN
            self.to_address_box.remove(
                self.verified_icon
            )
            self.invalid_icon.style.visibility = VISIBLE
            self.to_address_box.add(
                self.invalid_icon
            )
            await asyncio.sleep(1)
            self.to_address_input.value = ""
            return
        if result is not None:
            if is_valid is True:
                self.invalid_icon.style.visibility = HIDDEN
                self.to_address_box.remove(
                    self.invalid_icon
                )
                self.verified_icon.style.visibility = VISIBLE
                self.to_address_box.add(
                    self.verified_icon
                )
            elif is_valid is False:
                self.verified_icon.style.visibility = HIDDEN
                self.to_address_box.remove(
                    self.verified_icon
                )
                self.invalid_icon.style.visibility = VISIBLE
                self.to_address_box.add(
                    self.invalid_icon
                )
                await asyncio.sleep(1)
                self.to_address_input.value = ""
            
    
    async def check_txfee(self, input):
        selected_address = self.select_address.value.select_address
        if selected_address == "Main Account":
            self.fee_input.value = ""
            self.fee_input.readonly = True
        else:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                data = self.client.getInfo()
            else:
                data = await self.command.getInfo()
                data = json.loads(data)
            if data is not None:
                paytxfee = data.get('paytxfee')
                relayfee = data.get('relayfee')
            if paytxfee == 0.0:
                self.fee_input.value = f"{relayfee:.8f}"
            else:
                self.fee_input.value = f"{paytxfee:.8f}"
            self.fee_input.readonly = False
            
            
    def check_comments(self, input):
        selected_address = self.select_address.value.select_address
        address = self.to_address_input.value
        if selected_address == "Main Account":
            self.comment_memo_input.readonly = False
            self.comment_memo_input.placeholder = "comment"
        elif selected_address != "Main Account" and address.startswith("z"):
            self.comment_memo_input.readonly = False
            self.comment_memo_input.placeholder = "memo"
        else:
            self.comment_memo_input.value = ""
            self.comment_memo_input.readonly = True
               
            
            
    async def check_inputs_value(self, button):
        selected_address = self.select_address.value.select_address if self.select_address.value else None
        address = self.to_address_input.value
        amount = self.amount_input.value
        txfee = self.fee_input.value
        comment = self.comment_memo_input.value
        byte_size = sys.getsizeof(comment)
        if selected_address is None:
            async def on_confirm(result, window):
                if result:
                    self.select_address.focus()
            self.error_dialog(
                "No address selected",
                "Select address you are sending from",
                on_result=on_confirm
            )
            return
        elif address == "":
            async def on_confirm(result, window):
                if result:
                    self.to_address_input.focus()
            self.error_dialog(
                "No distination",
                "The distination address was not entred",
                on_result=on_confirm
            )
            return
        elif amount == "":
            async def on_confirm(result, window):
                if result:
                    self.amount_input.focus()
            self.error_dialog(
                "No amount",
                "The amount was not entred",
                on_result=on_confirm
            )
            return
        elif byte_size > 512:
            async def on_confirm(result, window):
                if result:
                    self.comment_memo_input.focus()
            self.error_dialog(
                "Size limit",
                "The size of comment/memo higher than 512 bytes",
                on_result=on_confirm
            )
            return
        elif txfee == "" or float(txfee) == 0:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                data = self.client.getInfo()
            else:
                data = await self.command.getInfo()
                data = json.loads(data)
            if data is not None:
                relayfee = data["relayfee"]
            txfee = relayfee
        await self.get_sending_method(
            selected_address,
            address,
            amount,
            comment,
            txfee
        )
        
        
    async def get_sending_method(self, selected_address, address, amount, comment, txfee):
        self.send_button.enabled = False
        txid = None
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        try:
            if selected_address == "Main Account" and address.startswith("t"):
                if os.path.exists(db_path):
                    operation = self.client.sendToAddress(address, amount, comment)
                else:
                    operation = await self.command.sendToAddress(address, amount, comment)
                if operation is not None:
                    txid = operation
                    await self.clear_inputs()
                    await self.send_notification_system(amount, txid)
                    await asyncio.sleep(1)
                    await self.update_last_transaction()
                else:
                    self.send_button.enabled = True
                    
                    
            elif selected_address != "Main Account":
                if os.path.exists(db_path):
                    operation = self.client.z_sendMany(selected_address, address, amount, comment, txfee)
                else:
                    operation = await self.command.z_sendMany(selected_address, address, amount, comment, txfee)
                if operation:
                    if os.path.exists(db_path):
                        transaction_status = self.client.z_getOperationStatus(operation)
                    else:
                        transaction_status = await self.command.z_getOperationStatus(operation)
                        transaction_status = json.loads(transaction_status)
                    if isinstance(transaction_status, list) and transaction_status:
                        status = transaction_status[0].get('status')
                        if status == "executing" or status =="success":
                            await asyncio.sleep(1)
                            while True:
                                if os.path.exists(db_path):
                                    transaction_result = self.client.z_getOperationResult(operation)
                                else:
                                    transaction_result = await self.command.z_getOperationResult(operation)
                                    transaction_result = json.loads(transaction_result)
                                if isinstance(transaction_result, list) and transaction_result:
                                    result = transaction_result[0].get('result', {})
                                    txid = result.get('txid')
                                    await self.clear_inputs()
                                    await self.send_notification_system(amount, txid)
                                    await asyncio.sleep(1)
                                    await self.update_last_transaction()
                                    return
                                await asyncio.sleep(3)
                        else:
                            self.send_button.enabled = True
                else:
                    self.send_button.enabled = True
                    
        except Exception as e:
            self.send_button.enabled = True
            print(f"An error occurred: {e}")
            
    
    async def clear_inputs(self):
        if self.transaction_mode == "transparent":
            address_list = await self.get_transparent_addresses()
        else:
            address_list = await self.get_shielded_addresses()
        self.verified_icon.style.visibility = HIDDEN
        self.invalid_icon.style.visibility = HIDDEN
        self.select_address.items.clear()
        self.select_address.items = address_list
        self.to_address_input.value = ""
        self.amount_input.value = ""
        self.comment_memo_input.value = ""
        self.comment_calculate.style.color = WHITE
        self.send_button.enabled = True
            
            
    async def send_notification_system(self, amount, txid):
        import clr
        clr.AddReference("System.Drawing")
        clr.AddReference("System.Windows.Forms")
        from System.Drawing import Icon
        from System.Windows.Forms import NotifyIcon
        icon_path = os.path.join(self.app.paths.app, "resources/app_logo.ico")
        icon = Icon(icon_path)
        self.notify_icon = NotifyIcon()
        self.notify_icon.Visible = True
        self.notify_icon.BalloonTipClicked += lambda sender, event: asyncio.create_task(self.on_notification_click(txid))
        self.notify_icon.Icon = icon
        self.notify_icon.BalloonTipTitle = f"Sent {amount} BTCZ"
        self.notify_icon.BalloonTipText = txid
        self.notify_icon.ShowBalloonTip(10)
        threading.Timer(10, self.hide_toast).start()


    async def on_notification_click(self, txid):
        await self.transaction_window(txid)


    def hide_toast(self):
        self.notify_icon.Visible = False
    
        
    async def update_last_transaction(self):
        self.last_transaction_list.content.clear()
        self.main_box.remove(
            self.last_transaction_list
        )
        self.main_box.add(
            self.loading_box
        )
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        transactions_count = 10
        transactions_from = 0
        if os.path.exists(db_path):
            transactions_data = self.client.listTransactions(
                transactions_count,
                transactions_from
            )
        else:
            transactions_data = await self.command.listTransactions(
                transactions_count,
                transactions_from
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
                self.last_transaction_box.add(
                    transaction_box
                )
        self.last_transaction_list.content = self.last_transaction_box
        await asyncio.sleep(1.5)
        self.main_box.remove(
            self.loading_box
        )
        self.main_box.add(
            self.last_transaction_list
        )
            
    
    async def verify_balances(self, input):
        amount = self.amount_input.value
        if not amount:
            self.amount_note.text = ""
            return
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        selected_address = self.select_address.value.select_address if self.select_address.value else None
        if selected_address != "Main Account":
            if os.path.exists(db_path):
                address_balance = self.client.z_getBalance(selected_address)
            else:
                address_balance = await self.command.z_getBalance(selected_address)
            if address_balance is not None:
                if float(amount) < float(address_balance):
                    self.amount_note.text = ""
                elif float(amount) > float(address_balance):
                    self.amount_note.text = "Insufficient balance"
                    await asyncio.sleep(1)
                    self.amount_input.value = ""
        elif selected_address == "Main Account":
            if os.path.exists(db_path):
                total_balance = self.client.z_getTotalBalance()
            else:
                total_balance = await self.command.z_getTotalBalance()
                total_balance = json.loads(total_balance)
            if total_balance is not None:
                transparent_balance = total_balance.get("transparent", 0)
                if float(amount) < float(transparent_balance):
                    self.amount_note.text = ""
                elif float(amount) > float(transparent_balance):
                    self.amount_note.text = "Insufficient balance"
                    await asyncio.sleep(1)
                    self.amount_input.value = ""
        else:
            self.amount_note.text = "No address selected"
                
            
    def is_digit(self, value):
        if not value.replace('.', '', 1).isdigit():
            self.amount_input.value = ""


    def calculate_bytes(self, input):
        value =  self.comment_memo_input.value
        if not value:
            self.comment_calculate.text = "0 / 512 bytes"
        else:
            byte_size = sys.getsizeof(value)
            self.comment_calculate.text = f"{byte_size} / 512 bytes"
            if byte_size > 512:
                self.comment_memo_input.style.color = RED
                self.comment_calculate.style.color = RED
            elif byte_size <= 512:
                self.comment_memo_input.style.color = YELLOW
                self.comment_calculate.style.color = WHITE
                
        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('cash_window', False)
        self.close()