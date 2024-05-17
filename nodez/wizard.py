import asyncio
import os
import subprocess

from toga import (
    App,
    Box,
    Label,
    ImageView,
    Button,
    Icon
)
from toga.widgets.base import Widget
from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle

from .social import Social

class MainWinzard(Box):
    def __init__(self, app:App, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.main_box
        super().__init__(id, style, children)
        self.app = app
        
        self.nodez_banner = ImageView(
            "resources/nodez_banner.png"
        )
        self.version_txt = Label(
            f"version {self.app._version}",
            style=LabelStyle.version_text_style
        )
        self.nodez_banner_box = Box(
            style=BoxStyle.nodez_banner_box
        )
        self.nodez_banner_box.add(
            self.nodez_banner
        )
        self.row_top_box = Box(
            style=BoxStyle.row_box_top
        )
        self.row_center_box = Box(
            style=BoxStyle.row_box_center
        )
        self.row_bottom_box = Box(
            style=BoxStyle.row_box_bottom
        )
        self.clomun_box_center = Box(
            style=BoxStyle.clomun_box_center
        )
        self.row_top_box.add(
            self.nodez_banner_box
        )
        self.row_bottom_box.add(
            self.version_txt
        )
        self.clomun_box_center.add(
            self.row_top_box,
            self.row_center_box,
            self.row_bottom_box,
            Social(self.app)
        )
        self.add(
            self.clomun_box_center
        )
        
        self.app.add_background_task(
            self.loading_options)
    
    async def loading_options(self, widget):
        await asyncio.sleep(1)
        self.loading_txt = Label(
            "Loading...",
            style=LabelStyle.loading_txt_style
        )
        self.row_center_box.add(
            self.loading_txt
        )
        await self.display_options_setup()
        
    async def display_options_setup(self):
        await asyncio.sleep(1)
        self.row_center_box.remove(
            self.loading_txt
        )
        self.rpc_button = Button(
            icon=Icon("icones/rpc"),
            style=ButtonStyle.rpc_button_style
        )
        self.local_button = Button(
            icon=Icon("icones/setup"),
            style=ButtonStyle.local_button_style
        )
        self.row_center_box.add(
            self.rpc_button,
            self.local_button
        )
            