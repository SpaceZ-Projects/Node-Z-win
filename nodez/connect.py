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
from toga.window import OnCloseHandler
from .styles.box import BoxStyle
from .styles.label import LabelStyle
from toga.colors import RED, BLACK


class WindowRPC(Window):
    def __init__(self, app:App, rpc_button, local_button):
        super().__init__(
            title="RPC Connect",
            size=(300, 200),
            position=(400, 300),
            resizeable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.rpc_button = rpc_button
        self.local_button = local_button
        
        self.rpcuser_txt = Label(
            "rpcuser :",
            style=LabelStyle.default_txt_bold_style
        )
        self.rpcuser_input = TextInput(
            on_gain_focus=self.rpcuser_on_gain_focus
        )
        self.rpcpassword_txt = Label(
            "rpcpassword :",
            style=LabelStyle.default_txt_bold_style
        )
        self.rpcpassword_input = PasswordInput(
            on_gain_focus=self.rpcpassword_on_gain_focus
        )
        self.rpchost_txt = Label(
            "rpchost :",
            style=LabelStyle.default_txt_bold_style
        )
        self.rpchost_input = TextInput(
            on_gain_focus=self.rpchost_on_gain_focus
        )
        self.rpcport_txt = Label(
            "rpcport :",
            style=LabelStyle.default_txt_bold_style
        )
        self.rpcport_input = NumberInput(
            on_change=self.rpcport_on_change
        )
        self.divider = Divider()
        self.connect_button = Button(
            icon=Icon("icones/connect"),
            on_press=self.check_inputs
        )
        self.button_box = Box(
            style=BoxStyle.row
        )
        self.inputs_box = Box(
            style=BoxStyle.column_center_padding_5
        )
        self.main_box = Box(
            style=BoxStyle.column_center
        )
        self.inputs_box.add(
            self.rpcuser_txt,
            self.rpcuser_input,
            self.rpcpassword_txt,
            self.rpcpassword_input,
            self.rpchost_txt,
            self.rpchost_input,
            self.rpcport_txt,
            self.rpcport_input
        )
        self.button_box.add(
            self.connect_button
        )
        self.main_box.add(
            self.inputs_box,
            self.divider,
            self.button_box
        )
        self.content = self.main_box
        
    async def check_inputs(self, button):
        rpcuser = self.rpcuser_input.value
        rpcpassword = self.rpcpassword_input.value
        rpchost = self.rpchost_input.value
        rpcport = self.rpcport_input.value
        if rpcuser == '':
            self.app.main_window.info_dialog(
                "Empty input...",
                "- rpcuser is required"
            )
            self.rpcuser_txt.style.color = RED
            return
        elif rpcpassword == '':
            self.app.main_window.info_dialog(
                "Empty input...",
                "- rpcpassword is required"
            )
            self.rpcpassword_txt.style.color = RED
            return
        elif rpchost == '':
            self.app.main_window.info_dialog(
                "Empty input...",
                "- rpchost is required"
            )
            self.rpchost_txt.style.color = RED
            return
        elif rpcport is None:
            self.app.main_window.info_dialog(
                "Empty input...",
                "- rpcport is required"
            )
            self.rpcport_txt.style.color = RED
            return
    
    
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
        self.rpc_button.enabled = True
        self.local_button.enabled = True
        self.close()