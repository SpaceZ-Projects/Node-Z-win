import clr
import time
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Optional, Tuple, Callable
from .style import Font, FontStyle, Alignement, Color

class Label(Forms.Label):
    def __init__(
        self,
        text: str = "Hello, World!",
        font: Optional[Font] = Font.SERIF,
        aligne: Optional[Alignement] = Alignement.LEFT,
        style: Optional[FontStyle] = FontStyle.REGULAR,
        text_color: Optional[Color] = Color.BLACK,
        background_color: Optional[Color] = Color.TRANSPARENT,
        location: Tuple[int, int] = (0, 0),
        size: Optional[int] = 12,
        height: Optional[int] = None,
        max_width: Optional[int] = None,
        on_click: Optional[Callable[[], None]] = None,
        mouse_enter: Optional[Callable[[], None]] = None,
        mouse_leave: Optional[Callable[[], None]] = None,
        visible: bool = True
    ):
        super().__init__()

        self._text = text
        self._font = font
        self._aligne = aligne
        self._style = style
        self._text_color = text_color
        self._background_color = background_color
        self._location = location
        self._size = size
        self._height = height
        self._max_width = max_width
        self._on_click = on_click
        self._mouse_enter = mouse_enter
        self._mouse_leave = mouse_leave
        self._visible = visible

        self._font_object = Drawing.Font(self._font, self._size, self._style)

        self.Text = self._text
        self.ForeColor = self._text_color
        self.BackColor = self._background_color
        self.Location = Drawing.Point(self._location[0], self._location[1])
        self.TextAlign = self._aligne
        self.Font = self._font_object
        self.Visible = self._visible

        if self._height:
            self.Height = self._height
            self.AutoSize = False
        else:
            self._adjust_size()

        if self._on_click:
            self.Click += self._handle_click

        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter

        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave


    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.Text = value

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value
        self.Font = value

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
    def size(self) -> int:
        return self._size
    

    @size.setter
    def size(self, value: int):
        if value <= 0:
            raise ValueError("Font size must be a positive integer.")
        self._size = value
        self._update_font()

    
    @property
    def max_width(self) -> int:
        return self._max_width

    @max_width.setter
    def max_width(self, value: int):
        self._max_width = value
        self._adjust_size()


    @property
    def on_click(self) -> Optional[Callable[[], None]]:
        return self._on_click
    

    @on_click.setter
    def on_click(self, value: Optional[Callable[[], None]]):
        if self._on_click:
            self.Click -= self._handle_click
        self._on_click = value
        if self._on_click:
            self.Click += self._handle_click


    @property
    def mouse_enter(self) -> Optional[Callable[[], None]]:
        return self._mouse_enter
    

    @mouse_enter.setter
    def mouse_enter(self, value: Optional[Callable[[], None]]):
        if self._mouse_enter:
            self.MouseEnter -= self._handle_mouse_enter
        self._mouse_enter = value
        if self._mouse_enter:
            self.MouseEnter += self._handle_mouse_enter


    @property
    def mouse_leave(self) -> Optional[Callable[[], None]]:
        return self._mouse_leave


    @mouse_leave.setter
    def mouse_leave(self, value: Optional[Callable[[], None]]):
        if self._mouse_leave:
            self.MouseLeave -= self._handle_mouse_leave
        self._mouse_leave = value
        if self._mouse_leave:
            self.MouseLeave += self._handle_mouse_leave


    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        self.Visible = value
        

    def _update_font(self):
        self._font_object = Drawing.Font(self._font, self._size, self._style)
        self.Font = self._font_object
        self._adjust_size()



    def _adjust_size(self):
        if self._max_width is not None:
            wrapped_text = self._wrap_text(self.Text, self._max_width)
            graphics = self.CreateGraphics()
            try:
                text_size = graphics.MeasureString(wrapped_text, self.Font)
                padding = 1
                self.Size = Drawing.Size(
                    int(text_size.Width) + padding,
                    int(text_size.Height) + padding
                )
            finally:
                graphics.Dispose()
        else:
            self.AutoSize = True


    def _wrap_text(self, text: str, max_width: int) -> str:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip() if current_line else word
            graphics = self.CreateGraphics()
            try:
                if graphics.MeasureString(test_line, self.Font).Width > max_width:
                    if current_line:
                        lines.append(current_line)
                    while len(word) > 0:
                        part = word[:max_width]
                        lines.append(part)
                        word = word[max_width:]
                    current_line = ""
                else:
                    current_line = test_line
            finally:
                graphics.Dispose()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)
    

    def slide(self, target_location: Tuple[int, int], duration: float = 0.5, steps:int = 10):
        sleep_time = duration / steps
        
        delta_x = (target_location[0] - self.Location.X) / steps
        delta_y = (target_location[1] - self.Location.Y) / steps

        for _ in range(steps):
            self.Location = Drawing.Point(int(self.Location.X + delta_x), int(self.Location.Y + delta_y))
            Forms.Application.DoEvents()
            time.sleep(sleep_time)


    def resize(self, target_height: int, duration: float = 0.5, steps: int = 10):
        if self.Height == target_height:
            return

        sleep_time = duration / steps
        delta_height = (target_height - self.Height) / steps

        for _ in range(steps):
            # Update height
            self.Height = int(self.Height + delta_height)

            # Measure the text width based on the current text and font
            graphics = self.CreateGraphics()
            try:
                text_size = graphics.MeasureString(self.Text, self.Font)
                # Update the width to fit the text
                self.Width = int(text_size.Width) + 1  # Add some padding
            finally:
                graphics.Dispose()

            Forms.Application.DoEvents()
            time.sleep(sleep_time)


    def _handle_click(self, sender, event):
        if self._on_click:
            self._on_click()


    def _handle_mouse_enter(self, sender, event):
        if self._mouse_enter:
            self._mouse_enter()



    def _handle_mouse_leave(self, sender, event):
        if self._mouse_leave:
            self._mouse_leave()
