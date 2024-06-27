import asyncio
from datetime import datetime
from typing import Iterable

from toga import (
    App,
    Box,
    Button,
    Label,
    Icon,
    ImageView,
    TextInput,
    Divider
)
from toga.widgets.base import Widget
from toga.constants import Direction
from toga.colors import RED, GREEN

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..command import ClientCommands
from ..system import SystemOp


class AddressIndex(Box):
    def __init__(
            self,
            app:App,
            result: str | None = None,
            id: str | None = None,
            style= None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.address_info
        super().__init__(id, style, children)
        self.app = app
        self.result = result
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)