from toga.style.pack import Pack
from toga.colors import BLACK, GREENYELLOW
from toga.constants import HIDDEN



class SelectionStyle():


    peer_option_select = Pack(
        font_size = 11,
        padding_right = 20,
        padding_top = 10,
        background_color = BLACK,
        color = GREENYELLOW,
        visibility = HIDDEN
    )


    node_option_select = Pack(
        font_size = 11,
        padding_right = 55,
        padding_top = 10,
        background_color = BLACK,
        color = GREENYELLOW,
        visibility = HIDDEN
    )


    ban_option_select = Pack(
        font_size = 11,
        padding_right = 180,
        padding_top = 10,
        background_color = BLACK,
        color = GREENYELLOW,
        visibility = HIDDEN
    )