from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW, WHITE


class InputStyle():
    
    
    to_address_input = Pack(
        padding_top = 10,
        padding_left = 97,
        font_size = 11,
        color = YELLOW,
        background_color = BLACK,
        flex = 1
    )
    
    
    amount_input = Pack(
        padding_top = 15,
        padding_left = 60,
        width = 150,
        font_size = 11,
        color = YELLOW,
        background_color = BLACK
    )
    
    fee_input = Pack(
        padding_top = 15,
        padding_left = 75,
        font_size = 11,
        color = YELLOW,
        background_color = BLACK
    )
    
    comment_memo_input = Pack(
        padding_top = 16,
        padding_left = 18,
        font_size = 11,
        width = 300,
        color = YELLOW,
        background_color = BLACK
    )


    many_addresses_input = Pack(
        padding_top = 5,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )