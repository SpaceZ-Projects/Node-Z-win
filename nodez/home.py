import asyncio
from toga import (
    App,
    Box,
    Label,
    Button,
    Divider,
    ImageView,
    Icon
)
from toga.widgets.base import Widget

from .styles.box import BoxStyle
from .styles.button import ButtonStyle


class MainMenu(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style=BoxStyle.home_main_box
        super().__init__(id, style, children)
        
        self.cash_button = Button(
            icon=Icon("icones/cash"),
            style=ButtonStyle.menu_button
        )
        self.wallet_buuton = Button(
            icon=Icon("icones/wallet"),
            style=ButtonStyle.menu_button
        )
        self.explorer_button = Button(
            icon=Icon("icones/explorer"),
            style=ButtonStyle.menu_button
        )
        self.message_button = Button(
            icon=Icon("icones/message"),
            style=ButtonStyle.menu_button
        )
        self.tools_button = Button(
            icon=Icon("icones/tools"),
            style=ButtonStyle.menu_button
        )
        self.buttons_box = Box(
            style=BoxStyle.home_buttons_box
        )
        self.buttons_box.add(
            self.cash_button,
            self.wallet_buuton,
            self.explorer_button,
            self.message_button,
            self.tools_button
        )
        self.add(
            self.buttons_box
        )