

import asyncio


from toga import (
    App,
    Window,
    OptionContainer,
    OptionItem
)

from .styles.container import ContainerStyle

from ..system import SystemOp
from ..client import RPCRequest
from ..command import ClientCommands

from .peers import PeersInfo


class PeersManage(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Peers Manage",
            minimizable=False,
            resizable=False,
            size=(925, 550),
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)

        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button

        
        self.peer_info = OptionItem(
            "Peers Info",
            content=PeersInfo(self.app),
            enabled=True
        )
        self.peer_tabs = OptionContainer(
            content=[
                self.peer_info
            ],
            style=ContainerStyle.peer_main
        )
        self.app.add_background_task(
            self.display_window
        )

    async def display_window(self, widget):
    
        self.content = self.peer_tabs
        await asyncio.sleep(1)
        self.show()

    
    def close_window(self, window):
        self.close()
        self.system.update_settings('peermanage_window', False)
        self.window_button.enabled = True