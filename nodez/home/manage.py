

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
from .nodes import NodesList
from .banlist import BannedList


class NodesManage(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Nodes Manage",
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
            "Connected Nodes",
            content=PeersInfo(self.app),
            enabled=True
        )
        self.nodes_list = OptionItem(
            "Added Nodes",
            content=NodesList(self.app),
            enabled=True
        )
        self.banned_list = OptionItem(
            "Banned List",
            content=BannedList(self.app),
            enabled=True
        )
        self.peer_tabs = OptionContainer(
            content=[
                self.peer_info,
                self.nodes_list,
                self.banned_list
            ],
            style=ContainerStyle.peer_main,
            on_select=self.update_tabs
        )
        self.app.add_background_task(
            self.display_window
        )

    async def display_window(self, widget):
    
        self.content = self.peer_tabs
        await asyncio.sleep(1)
        self.show()


    async def update_tabs(self, container):
        if self.peer_tabs.current_tab.text == "Connected Nodes":
            self.peer_tabs.content.remove(index=self.nodes_list)
            self.peer_tabs.content.remove(index=self.banned_list)
            self.nodes_list = OptionItem(
                "Added Nodes",
                content=NodesList(self.app),
                enabled=True
            )
            self.banned_list = OptionItem(
                "Banned List",
                content=BannedList(self.app),
                enabled=True
            )
            self.peer_tabs.content.insert(index=1, text_or_item=self.nodes_list)
            self.peer_tabs.content.insert(index=2, text_or_item=self.banned_list)

        elif self.peer_tabs.current_tab.text == "Added Nodes":
            self.peer_tabs.content.remove(index=self.peer_info)
            self.peer_tabs.content.remove(index=self.banned_list)
            self.peer_info = OptionItem(
                "Connected Nodes",
                content=PeersInfo(self.app),
                enabled=True
            )
            self.banned_list = OptionItem(
                "Banned List",
                content=BannedList(self.app),
                enabled=True
            )
            self.peer_tabs.content.insert(index=0, text_or_item=self.peer_info)
            self.peer_tabs.content.insert(index=2, text_or_item=self.banned_list)
        
        elif self.peer_tabs.current_tab.text == "Banned List":
            self.peer_tabs.content.remove(index=self.peer_info)
            self.peer_tabs.content.remove(index=self.nodes_list)
            self.peer_info = OptionItem(
                "Connected Nodes",
                content=PeersInfo(self.app),
                enabled=True
            )
            self.nodes_list = OptionItem(
                "Added Nodes",
                content=NodesList(self.app),
                enabled=True
            )
            self.peer_tabs.content.insert(index=0, text_or_item=self.peer_info)
            self.peer_tabs.content.insert(index=1, text_or_item=self.nodes_list)


    
    def close_window(self, window):
        self.close()
        self.system.update_settings('node_window', False)
        self.window_button.enabled = True