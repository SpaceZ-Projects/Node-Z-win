from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW
from toga.constants import BOLD


class SwitchStyle():


    many_switch = Pack(
        font_weight = BOLD,
        padding_left = 145,
        padding_top = 15,
        color = YELLOW,
        background_color = BLACK,
        flex = 1
    )


    split_switch = Pack(
        padding_left = 10,
        padding_top = 20,
        font_weight = BOLD,
        color = YELLOW,
        background_color = BLACK
    )


    each_switch = Pack(
        padding_top = 20,
        font_weight = BOLD,
        color = YELLOW,
        background_color = BLACK
    )