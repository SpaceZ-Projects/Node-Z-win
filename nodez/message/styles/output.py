from toga.style.pack import Pack
from toga.colors import BLACK, WHITE, CYAN
from toga.constants import BOLD



class OutputStyle():


    discussion_outputs = Pack(
        font_size = 12,
        padding = 5,
        flex = 1,
        background_color = BLACK,
        color = WHITE
    )


    contacts_list = Pack(
        font_size = 14,
        font_weight = BOLD,
        flex = 1,
        background_color = BLACK,
        color = CYAN,
        padding_bottom = 5
    )