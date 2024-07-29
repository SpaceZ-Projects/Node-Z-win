from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW, CYAN
from toga.constants import BOLD



class ButtonStyle():


    add_contact_button = Pack(
        font_weight = BOLD,
        padding_left = 20,
        padding_right = 20,
        padding_top = 10,
        background_color = BLACK,
        color = YELLOW
    )


    send_button = Pack(
        font_weight = BOLD,
        background_color = CYAN,
        color = BLACK,
        padding_top = 12,
        padding_left = 15,
        padding_right = 20,
        flex = 1
    )