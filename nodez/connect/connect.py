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
    NumberInput,
    Button,
    Icon
)
from ..request import rpc_test
from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.input import InputStyle
from toga.colors import RED, BLACK, GREEN

from ..home.home import MainMenu


class WindowRPC(Window):
    def __init__(self, app:App, rpc_button, local_button):
        super().__init__(
            title="RPC Connect",
            size=(280, 200),
            position=(200, 200),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.rpc_button = rpc_button
        self.local_button = local_button
        if self.local_button.enabled is True:
            self.button_status = True
        else:
            self.button_status = False
        
        self.rpcuser_txt = Label(
            "rpcuser :",
            style=LabelStyle.rpcuser_txt
        )
        self.rpcuser_input = TextInput(
            on_gain_focus=self.rpcuser_on_gain_focus,
            style=InputStyle.rpcuser_input
        )
        self.rpcpassword_txt = Label(
            "rpcpassword :",
            style=LabelStyle.rpcpassword_txt
        )
        self.rpcpassword_input = PasswordInput(
            on_gain_focus=self.rpcpassword_on_gain_focus,
            style=InputStyle.rpcpassword_input
        )
        self.rpchost_txt = Label(
            "rpchost :",
            style=LabelStyle.rpchost_txt
        )
        self.rpchost_input = TextInput(
            on_gain_focus=self.rpchost_on_gain_focus,
            style=InputStyle.rpchost_input
        )
        self.rpcport_txt = Label(
            "rpcport :",
            style=LabelStyle.rpcport_txt
        )
        self.rpcport_input = NumberInput(
            on_change=self.rpcport_on_change,
            style=InputStyle.rpcport_input
        )
        self.divider = Divider()
        self.connect_button = Button(
            icon=Icon("icones/connect"),
            on_press=self.check_inputs
        )
        self.button_box = Box(
            style=BoxStyle.button_box
        )
        self.main_box = Box(
            style=BoxStyle.main_box
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
            self.divider,
            self.button_box
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.auto_focus
        )
        
    def auto_focus(self, widget):
        if self.button_status is True:
            self.local_button.enabled = False
        self.rpc_button.enabled = False
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
        self.status_txt.style.color = BLACK
        await asyncio.sleep(2)
        self.close()
        self.app.main_window.hide()
        await asyncio.sleep(2)
        self.app.main_window.content.clear()
        self.app.main_window.content = MainMenu(self.app)
        self.app.main_window.size = (450, 200)
        self.app.main_window.position = (0,0)
        self.app.main_window.title = "Node-Z (RPC)"
        self.app.main_window.show()
    
    
    async def rpcuser_on_gain_focus(self, txt_input):
        self.rpcuser_txt.style.color = BLACK    
    
    async def rpcpassword_on_gain_focus(self, txt_input):
        self.rpcpassword_txt.style.color = BLACK
    
    async def rpchost_on_gain_focus(self, txt_input):
        self.rpchost_txt.style.color = BLACK
        
    async def rpcport_on_change(self, number_input):
        if number_input.value is not None:
            self.rpcport_txt.style.color = BLACK
        
        
    def close_window(self, widget):
        if self.button_status is True:
            self.local_button.enabled = True
        self.rpc_button.enabled = True
        
        self.close()