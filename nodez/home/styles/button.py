from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW


class ButtonStyle():
    
    
    menu_button = Pack(
        padding_top = 15,
        padding_right = 10,
        padding_left = 10,
        background_color = BLACK
    )


    peerinfo_button = Pack(
        padding_top = 1,
        background_color = BLACK
    )


    addnode_button = Pack(
        padding_left = 10,
        padding_right = 10,
        color = YELLOW,
        background_color = BLACK
    )


    clearbanned_button = Pack(
        padding_right = 10,
        color = YELLOW,
        background_color = BLACK
    )