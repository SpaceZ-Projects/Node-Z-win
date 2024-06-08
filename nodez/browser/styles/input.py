from toga.style.pack import Pack
from toga.colors import BLACK, WHITE
from toga.constants import BOLD


class InputStyle():
    
    
    url_input = Pack(
        padding_top = 15,
        padding_bottom = 5,
        padding_left = 5,
        font_size = 11,
        font_weight = BOLD,
        flex = 1,
        background_color = BLACK,
        color = WHITE
    )