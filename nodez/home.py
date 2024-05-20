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


class MainMenu(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None
    ):
        style=BoxStyle.column
        super().__init__(id, style, children)