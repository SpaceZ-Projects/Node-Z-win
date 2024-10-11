import clr
import System
import System.Windows.Forms as Forms
import System.Drawing as Drawing

from typing import List, Optional, Tuple, Callable
from .style import Color, Font, FontStyle

class Selection(Forms.ComboBox):
    def __init__(
            self,
            size: Tuple[int, int] = None,
            text_size: Optional[int] = 10,
            font: Optional[Font] = Font.SERIF,
            style: Optional[FontStyle] = FontStyle.REGULAR,
            color: Optional[Color] = Color.BLACK,
            background_color: Optional[Color] = Color.WHITE,
            location: Tuple[int, int] = (0, 0),
            items: Optional[List[str]] = None,
            index: Optional[int] = None,
            value: Optional[str] = None,
            on_change: Optional[Callable[[int], None]] = None
        ):
        super().__init__()

        self._size = size
        self._text_size = text_size
        self._font = font
        self._style = style
        self._color = color
        self._background_color = background_color
        self._location = location
        self._items = items if items else []
        self._index = index if index is not None else 0
        self._value = value if value is not None else (self._items[self._index] if self._items else None)
        self._on_change = on_change

        if self._size is None:
            self.AutoSize = True
        else:
            self.AutoSize = False
            self.Size = Drawing.Size(*self._size)

        self.Location = Drawing.Point(*self._location)
        self.DropDownStyle = Forms.ComboBoxStyle.DropDownList
        self.FlatStyle = Forms.FlatStyle.Flat
        self.MaxDropDownItems = 4
        self.IntegralHeight = False
        self.Font = Drawing.Font(self.font, self._text_size, self.style)
        self.ForeColor = self._color
        self.BackColor = self._background_color

        self.Items.AddRange(self._items)

        if self._on_change:
            self.SelectedIndexChanged += self.on_selection_change




    @property
    def size(self) -> Tuple[int, int]:
        return self._size
    


    @size.setter
    def size(self, value: Tuple[int, int]):
        self._size = value
        self.Size = Drawing.Size(value[0], value[1])



    @property
    def text_size(self) -> Optional[int]:
        return self._text_size
    


    @text_size.setter
    def text_size(self, value: Optional[int]):
        self._text_size = value
        self.Font = Drawing.Font(self.font, self._text_size, self.style)



    @property
    def font(self) -> Optional[Font]:
        return self._font
    


    @font.setter
    def font(self, value: Optional[Font]):
        self._font = value
        self.Font = Drawing.Font(self.font, self._text_size, self.style)



    @property
    def style(self) -> Optional[FontStyle]:
        return self._style
    


    @style.setter
    def style(self, value: Optional[FontStyle]):
        self._style = value
        self.Font = Drawing.Font(self.font, self._text_size, self.style)



    @property
    def color(self) -> Optional[Color]:
        return self._color
    


    @color.setter
    def color(self, value: Optional[Color]):
        self._color = value



    @property
    def background_color(self) -> Optional[Color]:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Optional[Color]):
        self._background_color = value



    @property
    def location(self) -> Tuple[int, int]:
        return self._location
    

    @location.setter
    def location(self, value: Tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(value[0], value[1])



    @property
    def items(self) -> List[str]:
        return self._items
    


    @items.setter
    def items(self, value: List[str]):
        self._items = value
        self.Items.Clear()
        for item in value:
            self.Items.Add(item)



    @property
    def index(self) -> Optional[int]:
        return self._index
    


    @index.setter
    def index(self, value: Optional[int]):
        self._index = value
        self.SelectedIndex = value


    @property
    def value(self) -> Optional[str]:
        return self._value
    


    @value.setter
    def value(self, value: Optional[str]):
        if value in self._items:
            self._value = value
            self.SelectedItem = value
            self.SelectedIndex = self._items.index(value)
        else:
            raise ValueError(f"{value} is not in the items list.")
        


    @property
    def on_change(self) -> Optional[Callable[[int], None]]:
        return self._on_change
    


    @on_change.setter
    def on_change(self, value: Optional[Callable[[int], None]]):
        if self._on_change:
            self.SelectedIndexChanged -= self.on_selection_change
        self._on_change = value
        if self._on_change:
            self.SelectedIndexChanged += self.on_selection_change



    def on_selection_change(self, sender, event):
        if self._on_change:
            self._on_change(self.SelectedItem)
        


    def add_item(self, item: str):
        self.Items.Add(item)



    def add_items(self, items: List[str]):
        self.Items.AddRange(items)



    def clear_items(self):
        self.Items.Clear()
