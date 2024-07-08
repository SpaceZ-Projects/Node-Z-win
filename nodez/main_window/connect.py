import asyncio
import os
import sqlite3

from toga import (
    App,
    Window,
    Box,
    Divider,
    Label,
    TextInput,
    PasswordInput,
    Button,
    Icon
)

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from .styles.button import ButtonStyle
from .styles.divider import DividerStyle

from toga.colors import RED, GREEN, WHITE, YELLOW

from ..home.home import HomeWindow
from ..system import SystemOp
from ..client import rpc_test


class WindowRPC(Window):
    def __init__(self, app:App):
        super().__init__(
            title="RPC Connect",
            size=(350, 350),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        
        self.rpcuser_txt = Label(
            "rpcuser :",
            style=LabelStyle.rpc_txt
        )
        self.rpcuser_input = TextInput(
            style=InputStyle.rpc_input,
            on_gain_focus=self.update_status
        )
        self.rpcpassword_txt = Label(
            "rpcpassword :",
            style=LabelStyle.rpc_txt
        )
        self.rpcpassword_input = PasswordInput(
            style=InputStyle.rpc_input,
            on_gain_focus=self.update_status
        )
        self.rpchost_txt = Label(
            "rpchost :",
            style=LabelStyle.rpc_txt
        )
        self.rpchost_input = TextInput(
            style=InputStyle.rpc_input,
            on_gain_focus=self.update_status
        )
        self.rpcport_txt = Label(
            "rpcport :",
            style=LabelStyle.rpc_txt
        )
        self.rpcport_input = TextInput(
            style=InputStyle.rpc_input,
            on_gain_focus=self.update_status,
            validators=[
                self.is_digit
            ]
        )
        self.rpc_divider = Divider(
            style=DividerStyle.rpc_divider
        )
        self.connect_button = Button(
            icon=Icon("icones/connect"),
            style=ButtonStyle.connect_button,
            on_press=self.check_inputs
        )
        self.button_box = Box(
            style=BoxStyle.connect_button_box
        )
        self.main_box = Box(
            style=BoxStyle.connect_main_box
        )
        self.button_box.add(
            self.connect_button
        )
        self.main_box.add(
            self.rpcuser_txt,
            self.rpcuser_input,
            self.rpcpassword_txt,
            self.rpcpassword_input,
            self.rpchost_txt,
            self.rpchost_input,
            self.rpcport_txt,
            self.rpcport_input,
            self.rpc_divider,
            self.button_box
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.auto_focus
        )
        
        
    async def auto_focus(self, widget):
        self.app.main_window.hide()
        await asyncio.sleep(1)
        self.show()
        self.rpcuser_input.focus()
        
        
    async def check_inputs(self, button):
        rpcuser = self.rpcuser_input.value
        rpcpassword = self.rpcpassword_input.value
        rpchost = self.rpchost_input.value
        rpcport = self.rpcport_input.value
        if rpcuser == '':
            self.info_dialog(
                "Empty input...",
                "- rpcuser is required"
            )
            self.rpcuser_txt.style.color = RED
            return
        elif rpcpassword == '':
            self.info_dialog(
                "Empty input...",
                "- rpcpassword is required"
            )
            self.rpcpassword_txt.style.color = RED
            return
        elif rpchost == '':
            self.info_dialog(
                "Empty input...",
                "- rpchost is required"
            )
            self.rpchost_txt.style.color = RED
            return
        elif rpcport is None:
            self.info_dialog(
                "Empty input...",
                "- rpcport is required"
            )
            self.rpcport_txt.style.color = RED
            return
        await self.try_to_connect(rpcuser, rpcpassword, rpchost, rpcport)
    
    
    async def try_to_connect(self, rpcuser, rpcpassword, rpchost, rpcport):
        self.rpcuser_input.readonly = True
        self.rpcpassword_input.readonly = True
        self.rpchost_input.readonly = True
        self.rpcport_input.readonly = True
        self.status_txt = Label(
            "connecting...",
            style=LabelStyle.status_txt
        )
        self.button_box.remove(
            self.connect_button
        )
        self.button_box.add(
            self.status_txt
        )
        result = rpc_test(
            rpcuser,
            rpcpassword,
            rpchost,
            rpcport
        )
        await asyncio.sleep(2)
        if result is False:
            self.status_txt.style.color = RED
            self.status_txt.text = "failed"
            await asyncio.sleep(2)
            self.button_box.remove(
                self.status_txt
            )
            self.button_box.add(
                self.connect_button
            )
            self.rpcuser_input.readonly = False
            self.rpcpassword_input.readonly = False
            self.rpchost_input.readonly = False
            self.rpcport_input.readonly = False
            return
        if result is True:
            self.status_txt.style.color = GREEN
            self.status_txt.text = "connected"
            await asyncio.sleep(2)
            await self.save_temp_config(
                rpcuser,
                rpcpassword,
                rpchost,
                rpcport
            )
    
    async def save_temp_config(
        self,
        rpcuser,
        rpcpassword,
        rpchost,
        rpcport
    ):
        config_path = self.app.paths.config
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        db_path = os.path.join(config_path, 'config.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS config (
                rpcuser TEXT,
                rpcpassword TEXT,
                rpchost TEXT,
                rpcport INTEGER
            )
            '''
        )
        cursor.execute(
            '''
            INSERT OR REPLACE INTO config (rpcuser, rpcpassword, rpchost, rpcport)
            VALUES (?, ?, ?, ?)
            ''', 
            (rpcuser, rpcpassword, rpchost, int(rpcport))
        )
        conn.commit()
        conn.close()
        await self.start_the_gui()
    
    async def start_the_gui(self):
        await asyncio.sleep(1)
        self.status_txt.text = "starting GUI..."
        self.status_txt.style.color = WHITE
        await asyncio.sleep(2)
        self.home_window = HomeWindow(self.app)
        self.home_window.title = "MainMenu (RPC)"
        self.close()

    
    def update_status(self, input):
        self.rpcuser_txt.style.color = YELLOW
        self.rpcpassword_txt.style.color = YELLOW
        self.rpchost_txt.style.color = YELLOW
        self.rpcport_txt.style.color = YELLOW


    def is_digit(self, value):
        if not value.isdigit():
            self.rpcport_input.value = ""
        
        
    async def close_window(self, widget):
        self.system.clean_config_path()
        self.close()
        await asyncio.sleep(1)
        self.app.main_window.show()