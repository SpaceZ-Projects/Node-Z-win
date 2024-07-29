from toga.style.pack import Pack
from toga.colors import BLACK, CYAN, YELLOW
from toga.constants import BOLD


class InputStyle():


    chat_inputs = Pack(
        font_size = 12,
        font_weight = BOLD,
        padding_top = 15,
        padding_bottom = 10,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK,
        color = CYAN,
        width = 600
    )


    amount_input = Pack(
        font_size = 10,
        padding_top = 3,
        padding_right = 2,
        background_color = BLACK,
        color = YELLOW
    )


    fee_input = Pack(
        font_size = 10,
        padding_top = 3,
        padding_right = 5,
        padding_left = 2,
        background_color = BLACK,
        color = YELLOW
    )