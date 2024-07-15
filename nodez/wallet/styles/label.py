from toga.style.pack import Pack
from toga.constants import CENTER, BOLD
from toga.colors import BLACK, WHITE, YELLOW



class LabelStyle():


    select_address_txt = Pack(
        padding_top = 17,
        padding_left = 130,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    balance_txt = Pack(
        text_align = CENTER,
        font_size = 21,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        padding_top = 10
    )

    balance_value = Pack(
        text_align = CENTER,
        font_size = 25,
        background_color = BLACK,
        padding_top = 25,
        padding_bottom = 37
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

    private_key_txt = Pack(
        padding = 5,
        font_weight = BOLD,
        background_color = BLACK,
        color = WHITE
    )


    no_transactions_txt = Pack(
        padding_top = 150,
        font_size = 15,
        text_align = CENTER,
        color = WHITE,
        background_color = BLACK,
        font_weight = BOLD,
    )


    merge_select_address_txt = Pack(
        padding_top = 17,
        padding_left = 10,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )


    merge_result_txt = Pack(
        padding_top = 10,
        padding_left = 40,
        padding_right = 40,
        font_size = 12,
        font_weight = BOLD,
        text_align = CENTER,
        color = YELLOW,
        background_color = BLACK,
    )


    merge_info_txt = Pack(
        text_align = CENTER,
        padding_top = 10,
        color = WHITE,
        background_color = BLACK
    )

    merge_list_txt = Pack(
        padding = 15,
        text_align = CENTER,
        color = WHITE,
        background_color = BLACK
    )


    merge_fee_txt = Pack(
        padding_top = 13,
        padding_left = 67,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )