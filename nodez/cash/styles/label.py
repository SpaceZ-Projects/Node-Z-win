from toga.style.pack import Pack
from toga.colors import BLACK, WHITE, RED, GREENYELLOW
from toga.constants import HIDDEN, BOLD, CENTER


class LabelStyle():
    
    
    select_address_txt = Pack(
        padding_top = 13,
        padding_left = 15,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )
    
    address_balance = Pack(
        visibility = HIDDEN,
        color = WHITE,
        font_weight = BOLD,
        background_color = BLACK,
        padding_top = 15,
        padding_left = 20,
        font_size = 9,
        flex = 1
    )
    
    to_address_txt = Pack(
        padding_top = 14,
        padding_left = 15,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )
    
    
    amount_txt = Pack(
        padding_top = 17,
        padding_left = 15,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )
    
    
    amount_note = Pack(
        color = RED,
        font_weight = BOLD,
        background_color = BLACK,
        padding_top = 19,
        padding_left = 20,
        flex = 1
    )
    
    fee_txt = Pack(
        padding_top = 16,
        padding_left = 15,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )
    
    
    txfee_info_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 20,
        padding_left = 20,
        flex = 1
    )
    
    comment_memo_txt = Pack(
        padding_top = 20,
        padding_left = 18,
        font_size = 9,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
        
    )
    
    transaction_address = Pack(
        padding = 5,
        color = WHITE,
        font_weight = BOLD,
        background_color = BLACK,
    )
    
    transaction_amount = Pack(
        padding = 5,
        color = WHITE,
        font_weight = BOLD,
        background_color = BLACK
    )
    
    time_received = Pack(
        padding_top = 5,
        padding_left = 20,
        color = WHITE,
        font_weight = BOLD,
        background_color = BLACK,
    )

    comment_calculate = Pack(
        padding_top = 20,
        padding_left = 10,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )


    info_txt = Pack(
        text_align = CENTER,
        padding_top = 10,
        color = WHITE,
        background_color = BLACK
    )


    verify_address_txt = Pack(
        visibility = HIDDEN,
        text_align = CENTER,
        padding_top = 10,
        background_color = BLACK
    )


    addresses_list_txt = Pack(
        padding_top = 14,
        padding_left = 95,
        font_size = 10,
        font_weight = BOLD,
        color = GREENYELLOW,
        background_color = BLACK
    )


    empty_txt = Pack(
        background_color = BLACK,
        flex = 1
    )