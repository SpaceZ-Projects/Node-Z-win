from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW, CYAN, WHITE
from toga.constants import BOLD



class ButtonStyle():


    transparent_button = Pack(
        padding_top = 20,
        padding_right = 250,
        padding_left = 30,
        font_size = 11,
        font_weight = BOLD,
        background_color = BLACK,
        color = YELLOW,
        flex = 1
    )
    
    shielded_button = Pack(
        padding_top = 20,
        padding_right = 30,
        padding_left = 250,
        font_size = 11,
        font_weight = BOLD,
        background_color = BLACK,
        color = CYAN,
        flex = 1
    )

    new_address_button = Pack(
        padding_left = 10,
        padding_right = 30,
        padding_top = 12,
        color = YELLOW,
        background_color = BLACK,
        flex = 1
    )


    address_buttons = Pack(
        color = BLACK,
        font_weight = BOLD,
        padding_top = 20,
        padding_right = 10
    )