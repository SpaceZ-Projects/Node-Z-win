from toga.style.pack import Pack
from toga.colors import BLACK, GREY
from toga.constants import COLUMN, ROW, CENTER


class BoxStyle():

    
    cash_main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )
    
    loading_box = Pack(
        direction = COLUMN,
        flex = 1,
        height = 250,
        background_color = BLACK,
        alignment = CENTER
    )
    
    cash_send_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        background_color = GREY,
        flex = 1,
        padding = 3
    )
    
    cash_transaction_box = Pack(
        direction = COLUMN,
        background_color = GREY,
        flex = 1,
        padding = 3
    )
    
    switch_button_box = Pack(
        direction = ROW,
        background_color = GREY
    )
    
    select_address_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    to_address_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    amount_box = Pack(
        direction = ROW,
        background_color = BLACK,
    )
    
    txfee_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    comment_memo_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    
    buttons_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )
    
    transaction_box = Pack(
        direction = ROW,
        padding = 2,
        background_color = BLACK
    )
    
    
    transaction_address_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        width = 350
    )

    transaction_amount_box = Pack(
        direction = COLUMN,
        background_color = BLACK
    )

    transaction_time_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )