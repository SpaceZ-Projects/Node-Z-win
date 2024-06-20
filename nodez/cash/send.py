
import os
import asyncio
import json

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

from toga.colors import CYAN, YELLOW
from toga.constants import VISIBLE, HIDDEN, Direction

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle
from .styles.selection import SelectionStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from .styles.container import ContainerStyle

from .txlist import LastTransactions
from ..system import SystemOp, NotificationWin
from ..client import RPCRequest
from ..commands import ClientCommands



class CashWindow(Window):
    def __init__(self, app:App, window_button):
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
            "icones/transparent.png",
            style=ImageStyle.transparent_icon
        )
        self.shielded_icon = ImageView(
            "icones/shield.png",
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
            on_lose_focus=self.verify_balances,
            on_gain_focus=self.verify_balances,
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
            on_gain_focus=self.check_comments
        )
        self.comment_memo_txt = Label(
            "Comment/Memo :",
            style=LabelStyle.comment_memo_txt
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
        self.commen_menmo_box = Box(
            style=BoxStyle.comment_memo_box
        )
        self.buttons_box = Box(
            style=BoxStyle.buttons_box
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
        self.commen_menmo_box.add(
            self.comment_memo_txt,
            self.comment_memo_input
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
            self.commen_menmo_box,
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
        self.last_transaction_list.content = LastTransactions(self.app)
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
            self.address_balance
        )
        self.txfee_box.add(
            self.fee_input,
            self.txfee_info_txt
        )
        self.show()
        
        
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
                    amount = balance - float(self.fee_input.value)
                    self.amount_input.value = f"{amount:.8f}"
                    
        
        
    async def switch_to_transparent(self, button):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.items.clear()
        self.select_address.style.color = YELLOW
        self.select_address.items = transparent_address
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
        self.select_address.items.clear()
        self.select_address.style.color = CYAN
        self.select_address.items = shielded_address
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
            addresses_data = self.client.listAddressgroupPings()
        else:
            addresses_data = await self.command.listAddressgroupPings()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            sorted_addresses = sorted(
                [address_info for address_info_list in addresses_data for address_info in address_info_list],
                key=lambda x: x[1],
                reverse=True
            )
            if len(sorted_addresses) == 1:
                address_items = [("Main Account", ""), (sorted_addresses[0][0], sorted_addresses[0][0])]
            else:
                address_items = [("Main Account", "")] + [(address_info[0], address_info[0]) for address_info in sorted_addresses]
        else:
            address_items = [("Main Account", "")]
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
                result = await self.command.z_validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        elif selected_address != "Main Account" and address.startswith("z"):
            if os.path.exists(db_path):
                result = self.client.validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.validateAddress(address)
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
        amount = float(amount)
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        try:
            if selected_address == "Main Account" and address.startswith("t"):
                if os.path.exists(db_path):
                    operation = self.client.sendToAddress(address, amount, comment)
                else:
                    operation = await self.command.sendToAddress(address, amount, comment)
                if operation is not None:
                    print(operation)
                    txid = operation
                    await self.clear_inputs()
                    await self.send_notification_system(amount, txid)
                    await self.update_last_transaction()
                else:
                    self.send_button.enabled = True
                    
                    
            elif selected_address != "Main Account":
                if os.path.exists(db_path):
                    operation = self.client.z_sendMany(selected_address, address, amount, comment, txfee)
                else:
                    operation = await self.command.z_sendMany(selected_address, address, amount, comment, txfee)
                if operation:
                    print(operation)
                    if os.path.exists(db_path):
                        transaction_status = self.client.z_getOperationStatus(operation)
                    else:
                        transaction_status = await self.command.z_getOperationStatus(operation)
                    if isinstance(transaction_status, list) and transaction_status:
                        print(transaction_status)
                        status = transaction_status[0].get('status')
                        if status == "executing":
                            await asyncio.sleep(1)
                            while True:
                                if os.path.exists(db_path):
                                    transaction_result = self.client.z_getOperationResult(operation)
                                else:
                                    transaction_result = await self.command.z_getOperationResult(operation)
                                if isinstance(transaction_result, list) and transaction_result:
                                    print(transaction_result)
                                    result = transaction_result[0].get('result', {})
                                    txid = result.get('txid')
                                    await self.clear_inputs()
                                    await self.send_notification_system(amount, txid)
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
        self.send_button.enabled = True
            
            
    async def send_notification_system(self, amount, txid):
        notify = NotificationWin(
            title=f"Sent : {amount} BTCZ",
            message=f"{txid}",
            icon=("resources/app_logo.ico"),
            duration=10,
            on_press=None
        )
        notify.popup()
        
    
        
    async def update_last_transaction(self):
        self.main_box.remove(
            self.last_transaction_list
        )
        self.last_transaction_list.content = LastTransactions(self.app)
        self.main_box.add(
            self.loading_box
        )
        await asyncio.sleep(4)
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
        try:
            amount = float(amount)
        except ValueError:
            self.amount_note.text = "Invalid amount"
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
                if amount < address_balance:
                    self.amount_note.text = ""
                elif amount > address_balance:
                    self.amount_note.text = "Insufficient balance"
                    self.amount_input.value = ""
                    await asyncio.sleep(2)
                    self.amount_note.text = ""
        elif selected_address == "Main Account":
            if os.path.exists(db_path):
                total_balance = self.client.z_getTotalBalance()
            else:
                total_balance = await self.command.z_getTotalBalance()
                total_balance = json.loads(total_balance)
            if total_balance is not None:
                transparent_balance = total_balance.get("transparent", 0)
                if amount < float(transparent_balance):
                    self.amount_note.text = ""
                elif amount > float(transparent_balance):
                    self.amount_note.text = "Insufficient balance"
                    self.amount_input.value = ""
                    await asyncio.sleep(2)
                    self.amount_note.text = ""
        else:
            self.amount_note.text = "No address selected"
                
            
    def is_digit(self, value):
        if not value.replace('.', '', 1).isdigit():
            self.amount_input.value = ""
                
        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('cash_window', False)
        self.close()