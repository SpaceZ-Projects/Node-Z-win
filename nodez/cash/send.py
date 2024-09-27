
import os
import asyncio
import json
import threading
from datetime import datetime
import operator
import sys
import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from toga import (
    App,
    Window,
    ScrollContainer,
    Selection,
    Divider,
    Box,
    Label,
    TextInput,
    Button,
    Icon,
    ImageView,
    Switch,
    MultilineTextInput
)

from toga.colors import CYAN, YELLOW, RED, WHITE, GREENYELLOW
from toga.constants import VISIBLE, HIDDEN, Direction

from .styles.box import BoxStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle
from .styles.selection import SelectionStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from .styles.container import ContainerStyle
from .styles.switch import SwitchStyle

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

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')

        self.input_lines = None
        
        self.loading_icon = ImageView(
            ("icons/loading_tx.gif"),
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
            "icons/transparent_txt.png",
            style=ImageStyle.transparent_icon
        )
        self.shielded_icon = ImageView(
            "icons/shielded_txt.png",
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
        self.many_switch = Switch(
            "Send to many addresses",
            style=SwitchStyle.many_switch,
            on_change=self.switch_to_many
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
            "icons/verified.png",
            style=ImageStyle.verified_icon
        )
        self.invalid_icon = ImageView(
            "icons/invalid.png",
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
        self.many_switch_box = Box(
            style=BoxStyle.many_switch_box
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
        self.many_switch_box.add(
            self.many_switch
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
            self.many_switch_box,
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
        self.display_window()


    async def get_transactions_list(self):
        if self.last_transaction_list.content:
            self.last_transaction_list.content.clear()
        self.main_box.remove(
            self.last_transaction_list
        )
        self.main_box.add(
            self.loading_box
        )
        transactions_count = 10
        transactions_from = 0
        if os.path.exists(self.db_path):
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
            selected_address = self.select_address.value.select_address
            if selected_address == "Main Account":
                if os.path.exists(self.db_path):
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
                if os.path.exists(self.db_path):
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


    def switch_to_many(self, switch):
        self.add_addresses_button = Button(
            "+ Add Addresses",
            enabled=True,
            style=ButtonStyle.add_addresses_button,
            on_press=self.display_addresses_input
        )
        self.split_switch = Switch(
            "Split",
            style=SwitchStyle.split_switch,
            on_change=self.split_option,
            value=True
        )
        self.each_switch = Switch(
            "Each",
            style=SwitchStyle.each_switch,
            on_change=self.each_option
        ) 
        if switch.value is True:
            self.to_address_box.clear()
            self.to_address_box.add(
                self.to_address_txt,
                self.add_addresses_button
            )
            self.amount_box.clear()
            self.comment_menmo_box.clear()
            self.amount_box.add(
                self.amount_txt,
                self.amount_input,
                self.max_button,
                self.split_switch,
                self.each_switch,
                self.amount_note
            )
            self.fee_input.value = 0.0001
            self.fee_input.on_gain_focus = None
            self.fee_input.readonly = True
            self.send_button.on_press = self.check_inputs_many_value
        else:
            self.to_address_box.clear()
            self.to_address_box.add(
                self.to_address_txt,
                self.to_address_input,
                self.invalid_icon
            )
            self.amount_box.clear()
            self.amount_box.add(
                self.amount_txt,
                self.amount_input,
                self.max_button,
                self.amount_note
            )
            self.comment_menmo_box.add(
                self.comment_memo_txt,
                self.comment_memo_input,
                self.comment_calculate
            )
            self.fee_input.on_gain_focus = self.check_txfee
            self.fee_input.readonly = False
            self.send_button.on_press = self.check_inputs_value
            

    def split_option(self, switch):
        if switch.value is True:
            self.each_switch.value = False
        else:
            self.each_switch.value = True

    
    def each_option(self, switch):
        if switch.value is True:
            self.split_switch.value = False
        else:
            self.split_switch.value = True


    def display_addresses_input(self, button):
        info_txt = Label(
            "Paste addresses, each address on a line",
            style=LabelStyle.info_txt
        )
        self.many_addresses_input = MultilineTextInput(
            placeholder="Paste addresses",
            style=InputStyle.many_addresses_input,
            on_change=self.update_verify_button
        )
        self.verify_address_txt = Label(
            "",
            style=LabelStyle.verify_address_txt
        )
        self.verify_button = Button(
            "Verify Addresses",
            style=ButtonStyle.verify_button,
            on_press=self.verify_addresses
        )
        main_box = Box(
            style=BoxStyle.cash_main_box
        )
        main_box.add(
            info_txt,
            self.many_addresses_input,
            self.verify_address_txt,
            self.verify_button
        )
        self.add_addresses_window = Window(
            title="Add addresses...",
            size=(500, 400),
            resizable=False,
            minimizable=False,
            on_close=self.display_cashout_window
        )
        self.add_addresses_window.position = self.system.windows_screen_center(self.add_addresses_window.size)
        self.hide()
        self.add_addresses_window.content = main_box
        self.add_addresses_window.show()


    async def verify_addresses(self, button):
        if not self.many_addresses_input.value:
            def on_confirm(result, window):
                if result:
                    self.many_addresses_input.focus()
            self.error_dialog(
                "No distination",
                "The distination address was not entred",
                on_result=on_confirm
            )
            return
        await self.is_addresses_valid()



    async def is_addresses_valid(self):
        self.add_addresses_window.on_close = self.disable_close_window
        self.many_addresses_input.readonly = True
        self.verify_button.enabled = False
        self.verify_address_txt.style.color = GREENYELLOW
        self.verify_address_txt.style.visibility = VISIBLE
        input_lines = self.many_addresses_input.value.strip().split('\n')
        if len(input_lines) < 2:
            self.error_dialog(
                "Error...",
                "Minimum 2 addresses"
            )
            self.many_addresses_input.readonly = False
            self.add_addresses_window.on_close = self.display_cashout_window
            self.verify_button.enabled = True
            return
        address_set = set()
        for line_num, address in enumerate(input_lines, start=1):
            result = None
            if not address.strip():
                continue
            if address in address_set:
                self.verify_address_txt.text = address
                self.verify_address_txt.style.color = RED
                self.add_addresses_window.on_close = self.display_cashout_window
                self.many_addresses_input.readonly = False
                self.verify_button.enabled = True
                self.error_dialog(
                    "Duplicate address...",
                    f"[Line {line_num}]: {address}"
                )
                return
            address_set.add(address)
            if address.startswith("t"):
                if os.path.exists(self.db_path):
                    result = self.client.validateAddress(address)
                    is_valid = result["isvalid"]
                else:
                    result = await self.command.validateAddress(address)
                    result = json.loads(result)
                    is_valid = result.get('isvalid')
            elif address.startswith("z"):
                if os.path.exists(self.db_path):
                    result = self.client.z_validateAddress(address)
                    is_valid = result["isvalid"]
                else:
                    result = await self.command.z_validateAddress(address)
                    result = json.loads(result)
                    is_valid = result.get('isvalid')
            if result is not None:
                if is_valid is True:
                    self.verify_address_txt.text = address
                elif is_valid is False:
                    self.verify_address_txt.text = address
                    self.verify_address_txt.style.color = RED
                    self.add_addresses_window.on_close = self.display_cashout_window
                    self.many_addresses_input.readonly = False
                    self.verify_button.enabled = True
                    self.error_dialog(
                        "Invalid address...",
                        f"[Line {line_num}]: {address}"
                    )
                    return
            else:
                self.verify_address_txt.text = address
                self.verify_address_txt.style.color = RED
                self.add_addresses_window.on_close = self.display_cashout_window
                self.many_addresses_input.readonly = False
                self.verify_button.enabled = True
                self.error_dialog(
                    "Invalid address...",
                    f"[Line {line_num}] : {address}"
                )
                return
        
        self.verify_address_txt.text = "All addresses are valid !"
        self.add_addresses_window.on_close = self.display_cashout_window
        self.many_addresses_input.readonly = False
        self.verify_button.text = "Done"
        self.verify_button.on_press = self.confirm_addresses_list
        self.verify_button.enabled = True


    def confirm_addresses_list(self, button):
        input_lines = [line for line in self.many_addresses_input.value.strip().split('\n') if line]
        self.input_lines = self.many_addresses_input.value.strip()
        number_addresses = len(input_lines)
        addresses_list_txt = Label(
            f"{number_addresses} addresses",
            style=LabelStyle.addresses_list_txt
        )
        edit_addresses_button = Button(
            "Edit",
            style=ButtonStyle.edit_addresses_button,
            on_press=self.edit_addresses
        )
        delete_addresses_button = Button(
            "Delete",
            style=ButtonStyle.edit_addresses_button,
            on_press=self.delete_addresses
        )
        empty_txt = Label(
            "",
            style=LabelStyle.empty_txt
        )
        self.add_addresses_window.close()
        self.show()
        self.to_address_box.clear()
        self.to_address_box.add(
            self.to_address_txt,
            addresses_list_txt,
            edit_addresses_button,
            delete_addresses_button,
            empty_txt
        )


    async def create_addresses_array(self):
        selected_address = self.select_address.value.select_address if self.select_address.value else None
        addresses = [line.strip() for line in self.input_lines.split('\n') if line.strip()]
        amount_value = self.amount_input.value.strip()
        if self.split_switch.value is True:
            amount = float(amount_value) / len(addresses)
            amount = f"{amount:.8f}"
        elif self.each_switch.value is True:
            amounts = float(amount_value) * len(addresses)
            if os.path.exists(self.db_path):
                address_balance = self.client.z_getBalance(selected_address)
            else:
                address_balance = await self.command.z_getBalance(selected_address)
            if float(amounts) > float(address_balance):
                self.error_dialog(
                    "Error...",
                    f"Insufficient balance for this transaction.\nTotal amount = {amounts:.8f}"
                )
                return
            else:
                amount = f"{amount_value:.8f}"
        transactions = [{"address": address, "amount": amount} for address in addresses]
        await self.get_sending_to_many_method(selected_address, transactions)


    
    async def get_sending_to_many_method(self, address, transactions):
        self.send_button.enabled = False
        try:
            if os.path.exists(self.db_path):
                operation = self.client.sendToManyAddresses(address, transactions)
            else:
                operation = await self.command.sendToManyAddresses(address, transactions)
            if operation:
                if os.path.exists(self.db_path):
                    transaction_status = self.client.z_getOperationStatus(operation)
                else:
                    transaction_status = await self.command.z_getOperationStatus(operation)
                    transaction_status = json.loads(transaction_status)
                if isinstance(transaction_status, list) and transaction_status:
                    status = transaction_status[0].get('status')
                    if status == "executing" or status =="success":
                        await asyncio.sleep(1)
                        while True:
                            if os.path.exists(self.db_path):
                                transaction_result = self.client.z_getOperationResult(operation)
                            else:
                                transaction_result = await self.command.z_getOperationResult(operation)
                                transaction_result = json.loads(transaction_result)
                            if isinstance(transaction_result, list) and transaction_result:
                                result = transaction_result[0].get('result', {})
                                txid = result.get('txid')
                                await self.clear_inputs_many()
                                await self.send_notification_system("Many", txid)
                                await asyncio.sleep(1)
                                await self.get_transactions_list()
                                return
                            await asyncio.sleep(3)
                    else:
                        self.send_button.enabled = True
            else:
                self.send_button.enabled = True
                
        except Exception as e:
            self.send_button.enabled = True
            print(f"An error occurred: {e}")



    def edit_addresses(self, button):
        self.display_addresses_input(None)
        self.many_addresses_input.value = self.input_lines

        

    def delete_addresses(self, button):
        self.input_lines = None
        self.to_address_box.clear()
        self.to_address_box.add(
            self.to_address_txt,
            self.add_addresses_button
        )


    def update_verify_button(self, input):
        self.verify_button.text = "Verify Addresses"
        self.verify_button.on_press = self.verify_addresses


    def disable_close_window(self, window):
        return
            

    def display_cashout_window(self, window):
        self.add_addresses_window.close()
        self.show()
        
        
        
    async def get_transparent_addresses(self):
        if os.path.exists(self.db_path):
            addresses_data = self.client.ListAddresses()
        else:
            addresses_data = await self.command.ListAddresses()
            if addresses_data:
                addresses_data = json.loads(addresses_data)
            else:
                addresses_data = []
        
        if addresses_data:
            address_items = [("Main Account")] + [(address_info, address_info) for address_info in addresses_data]
        else:
            address_items = [("Main Account")]
        
        return address_items
    
    
    async def get_shielded_addresses(self):
        if os.path.exists(self.db_path):
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
        if selected_address != "Main Account":
            self.many_switch.style.visibility = VISIBLE
            self.to_address_input.placeholder = "paste T or Z address"
            self.comment_memo_input.placeholder = "memo"
            if os.path.exists(self.db_path):
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
            self.many_switch.value = False
            self.many_switch.style.visibility = HIDDEN
            if self.fee_input.value is not None:
                self.fee_input.value = ""
            self.comment_memo_input.placeholder = "comment"
            self.to_address_input.placeholder = "paste T address"
            if os.path.exists(self.db_path):
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
        if not address:
            self.verified_icon.style.visibility = HIDDEN
            self.invalid_icon.style.visibility = HIDDEN
            return
        if selected_address == "Main Account" and address.startswith("t"):
            if os.path.exists(self.db_path):
                result = self.client.validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        elif selected_address != "Main Account" and address.startswith("t"):
            if os.path.exists(self.db_path):
                result = self.client.validateAddress(address)
                is_valid = result["isvalid"]
            else:
                result = await self.command.validateAddress(address)
                result = json.loads(result)
                is_valid = result.get('isvalid')
        elif selected_address != "Main Account" and address.startswith("z"):
            if os.path.exists(self.db_path):
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
            if os.path.exists(self.db_path):
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


    async def check_inputs_many_value(self, button):
        selected_address = self.select_address.value.select_address if self.select_address.value else None
        amount = self.amount_input.value       
        txfee = self.fee_input.value
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
        elif self.input_lines is None:
            self.error_dialog(
                "No addresses",
                "The distination addresses was not entred"
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
            if os.path.exists(self.db_path):
                data = self.client.getInfo()
            else:
                data = await self.command.getInfo()
                data = json.loads(data)
            if data is not None:
                relayfee = data["relayfee"]
            txfee = relayfee
        await self.create_addresses_array()



            
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
            if os.path.exists(self.db_path):
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
        try:
            if selected_address == "Main Account" and address.startswith("t"):
                if os.path.exists(self.db_path):
                    operation = self.client.sendToAddress(address, amount, comment)
                else:
                    operation = await self.command.sendToAddress(address, amount, comment)
                if operation is not None:
                    txid = operation
                    await self.clear_inputs()
                    await self.send_notification_system(amount, txid)
                    await asyncio.sleep(1)
                    await self.get_transactions_list()
                else:
                    self.send_button.enabled = True
                    
                    
            elif selected_address != "Main Account":
                if os.path.exists(self.db_path):
                    operation = self.client.z_sendMany(selected_address, address, amount, comment, txfee)
                else:
                    operation = await self.command.z_sendMany(selected_address, address, amount, comment, txfee)
                if operation:
                    if os.path.exists(self.db_path):
                        transaction_status = self.client.z_getOperationStatus(operation)
                    else:
                        transaction_status = await self.command.z_getOperationStatus(operation)
                        transaction_status = json.loads(transaction_status)
                    if isinstance(transaction_status, list) and transaction_status:
                        status = transaction_status[0].get('status')
                        if status == "executing" or status =="success":
                            await asyncio.sleep(1)
                            while True:
                                if os.path.exists(self.db_path):
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
                                    await self.get_transactions_list()
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

    
    async def clear_inputs_many(self):
        if self.transaction_mode == "transparent":
            address_list = await self.get_transparent_addresses()
        else:
            address_list = await self.get_shielded_addresses()
        self.select_address.items.clear()
        self.select_address.items = address_list
        self.amount_input.value = ""
        self.send_button.enabled = True
            
            
    async def send_notification_system(self, amount, txid):
        icon_path = os.path.join(self.app.paths.app, "icons/cashout.ico")
        icon = Drawing.Icon(icon_path)
        self.notify_icon = Forms.NotifyIcon()
        self.notify_icon.Visible = True
        self.notify_icon.BalloonTipClicked += lambda sender, event: asyncio.create_task(self.on_notification_click(txid))
        self.notify_icon.Icon = icon
        self.notify_icon.BalloonTipTitle = f"Sent {amount} BTCZ"
        self.notify_icon.BalloonTipText = txid
        self.notify_icon.ShowBalloonTip(5)
        threading.Timer(5, self.hide_toast).start()


    async def on_notification_click(self, txid):
        await self.transaction_window(txid)


    def hide_toast(self):
        self.notify_icon.Visible = False
            
    
    async def verify_balances(self, input):
        amount = self.amount_input.value
        if not amount:
            self.amount_note.text = ""
            return
        selected_address = self.select_address.value.select_address if self.select_address.value else None
        if selected_address != "Main Account":
            if os.path.exists(self.db_path):
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
            if os.path.exists(self.db_path):
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