from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW
from toga.constants import BOLD, HIDDEN


class ButtonStyle():
    
    
    menu_button = Pack(
        padding_top = 15,
        padding_left = 29,
        background_color = BLACK
    )


    peerinfo_button = Pack(
        padding_top = 1,
        color = YELLOW,
        background_color = BLACK
    )


    clear_button = Pack(
        padding_top = 10,
        padding_right = 10,
        background_color = BLACK,
        color = YELLOW,
        font_weight = BOLD,
        visibility = HIDDEN
    )