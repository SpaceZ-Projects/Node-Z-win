
from toga import (
    App,
    Window,
    Box,
    Label,
    TextInput,
    Button
)
from toga.constants import VISIBLE

from ..system import SystemOp


class WalletWindow(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Receive Coins",
            size=(600, 600),
            resizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center

        self.window_button = window_button
        
        self.show()
        
    def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('wallet_window', False)
        self.close()