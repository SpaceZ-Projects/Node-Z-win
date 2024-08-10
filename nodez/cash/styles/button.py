from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW, CYAN, RED
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
    
    
    max_button = Pack(
        padding_top = 16,
        padding_left = 10,
        color = CYAN,
        background_color = BLACK
    )
    
    
    send_button = Pack(
        padding_top = 25,
        padding_left = 145,
        padding_right = 500,
        background_color = YELLOW,
        font_size = 10,
        font_weight = BOLD,
        color = BLACK,
        flex = 1
    )

    explorer_button = Pack(
        padding_top = 2,
        padding_right = 3,
        background_color = BLACK,
        color = YELLOW
    )


    add_addresses_button = Pack(
        padding_top = 10,
        padding_left = 100,
        padding_right = 450,
        color = YELLOW,
        background_color = BLACK,
        flex = 1
    )


    verify_button = Pack(
        padding_top = 10,
        padding_bottom = 5,
        padding_left = 20,
        padding_right = 20,
        color = YELLOW,
        background_color = BLACK
    )


    edit_addresses_button = Pack(
        padding_top = 12,
        padding_left = 10,
        color = YELLOW,
        background_color = BLACK
    )


    delete_addresses_button = Pack(
        padding_top = 12,
        padding_left = 10,
        color = RED,
        background_color = BLACK
    )