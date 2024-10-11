import clr
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Optional, Tuple, Callable, Type
from .style import Font, FontStyle, Color

class TextInput(Forms.TextBox):
    def __init__(
        self,
        value: str = "",
        size: Tuple[int, int] = (100,30),
        font: Optional[Font] = Font.SERIF,
        style: Optional[FontStyle] = FontStyle.REGULAR,
        text_color: Optional[Color] = Color.BLACK,
        background_color: Optional[Color] = Color.WHITE,
        location: Tuple[int, int] = (0, 0),
        text_size: Optional[int] = 12,
        multiline: bool = False,
        password: bool = False,
        read_only: bool = False,
        on_enter: Optional[Callable[[Type], None]] = None,
        on_leave: Optional[Callable[[Type], None]] = None,
        on_confirm: Optional[Callable[[Type], None]] = None,
        on_change: Optional[Callable[[str], None]] = None,
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None,
    ):
        super().__init__()

        self._value = value
        self._size = size
        self._font = font
        self._style = style
        self._text_color = text_color
        self._background_color = background_color
        self._location = location
        self._text_size = text_size
        self._multiline = multiline
        self._password = password
        self._read_only = read_only
        self._on_enter_handler = on_enter
        self._on_leave_handler = on_leave
        self._on_confirm_handler = on_confirm
        self._on_change_handler = on_change
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave

        self._font_object = Drawing.Font(self._font, self._text_size, self._style)

        self.Text = self._value
        self.ForeColor = self._text_color
        self.BackColor = self._background_color
        self.Location = Drawing.Point(self._location[0], self._location[1])
        self.Font = self._font_object
        self.Multiline = self._multiline
        self.BorderStyle = Forms.BorderStyle(1)
        self.ReadOnly = self._read_only

        self.ClientSize = Drawing.Size(self._size[0], self._size[1])

        if self._password:
            self.PasswordChar = '●'

        if self._on_enter_handler:
            self.Enter += self._on_enter_handler

        if self._on_leave_handler:
            self.Leave += self._on_leave_handler

        if self._on_confirm_handler:
            self.KeyDown += self._on_key_down

        if self._on_change_handler:
            self.TextChanged += self._on_text_changed

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave



    @property
    def value(self) -> str:
        return self._value
    

    @value.setter
    def value(self, value: Optional[str]):
        if value is None:
            value = ""
        self._value = value

        if '\n' in value:
            self.Text = value.replace('\n', '\r\n')
        else:
            self.Text = value


    @property
    def size(self) -> Tuple[int, int]:
        return (self.Width, self.Height)


    @size.setter
    def size(self, value: Tuple[int, int]):
        if value[0] > 0:
            self.Width = value[0]
        if value[1] > 0:
            self.Height = value[1]



    @property
    def font(self) -> Font:
        return self._font
    


    @font.setter
    def font(self, value: Font):
        self._font = value
        self._update_font()



    @property
    def style(self) -> FontStyle:
        return self._style
    


    @style.setter
    def style(self, value: FontStyle):
        self._style = value
        self._update_font()



    @property
    def text_color(self) -> Color:
        return self._text_color
    


    @text_color.setter
    def text_color(self, value: Color):
        self._text_color = value
        self.ForeColor = value



    @property
    def background_color(self) -> Color:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Color):
        self._background_color = value
        self.BackColor = value



    @property
    def location(self) -> Tuple[int, int]:
        return (self.Location.X, self.Location.Y)
    


    @location.setter
    def location(self, value: Tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(value[0], value[1])



    @property
    def text_size(self) -> int:
        return self._text_size
    


    @text_size.setter
    def size(self, value: int):
        if value <= 0:
            raise ValueError("Font size must be a positive integer.")
        self._text_size = value
        self._update_font()



    @property
    def multiline(self) -> bool:
        return self._multiline
    


    @multiline.setter
    def multiline(self, value: bool):
        self._multiline = value
        self.Multiline = value


    
    @property
    def on_enter(self) -> Optional[Callable[[Type], None]]:
        return self._on_enter_handler
    



    @on_enter.setter
    def on_enter(self, handler: Optional[Callable[[Type], None]]):
        if self._on_enter_handler:
            self.Enter -= self._on_enter_handler
        self._on_enter_handler = handler




    @property
    def on_leave(self) -> Optional[Callable[[Type], None]]:
        return self._on_leave_handler
    



    @on_leave.setter
    def on_leave(self, handler: Optional[Callable[[Type], None]]):
        if self._on_leave_handler:
            self.Leave -= self._on_leave_handler
        self._on_leave_handler = handler




    @property
    def on_confirm(self) -> Optional[Callable[[Type], None]]:
        return self._on_confirm_handler
    
    


    @on_confirm.setter
    def on_confirm(self, handler: Optional[Callable[[Type], None]]):
        if self._on_confirm_handler:
            self.KeyDown -= self._on_key_down
        self._on_confirm_handler = handler




    @property
    def on_change(self) -> Optional[Callable[[Type], None]]:
        return self._on_change_handler
    



    @on_change.setter
    def on_change(self, handler: Optional[Callable[[], None]]):
        if self._on_change_handler:
            self.TextChanged -= self._on_text_changed
        self._on_change_handler = handler


    
    def focus(self):
        self.Focus()



    def _update_font(self):
        self._font_object = Drawing.Font(self._font, self._text_size, self._style)
        self.Font = self._font_object



    def _on_enter(self, sender, event):
        if self._on_enter_handler:
            self._on_enter_handler(sender, event)


            
    def _on_leave(self, sender, event):
        if self._on_leave_handler:
            self._on_leave_handler(sender, event)


    
    def _on_key_down(self, sender, event):
        if event.KeyCode == Forms.Keys.Enter:
            if self._on_confirm_handler:
                self._on_confirm_handler(sender, self.Text)
            self.Text += '\n'
            event.Handled = True



    def _on_text_changed(self, sender, event):
        if self._on_change_handler:
            self._on_change_handler(self.Text)


    def _handle_mouse_enter(self, sender, event):
        if self._mouse_enter:
            self._mouse_enter()


    def _handle_mouse_leave(self, sender, event):
        if self._mouse_leave:
            self._mouse_leave()
