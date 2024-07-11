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

    import_key_button = Pack(
        background_color = BLACK,
        padding_left = 50,
        padding_top = 10,
        padding_bottom = 20
    )

    confirm_key_button = Pack(
        background_color = BLACK,
        color = YELLOW,
        padding_left = 150,
        padding_right = 150
    )

    new_address_button = Pack(
        padding_left = 30,
        padding_top = 12,
        background_color = BLACK
    )


    address_buttons = Pack(
        background_color = BLACK,
        padding_top = 40,
        padding_right = 20
    )

    explorer_button = Pack(
        padding_top = 2,
        padding_right = 3,
        background_color = BLACK,
        color = YELLOW
    )

    previous_button = Pack(
        color = YELLOW,
        background_color = BLACK,
        padding_top = 10,
        padding_bottom = 10,
        padding_right = 10
    )

    next_button = Pack(
        color = YELLOW,
        background_color = BLACK,
        padding_top = 10,
        padding_bottom = 10,
        padding_left = 10
    )

    copy_button = Pack(
        background_color = BLACK,
        color = YELLOW,
        padding_left = 150,
        padding_right = 150
    )