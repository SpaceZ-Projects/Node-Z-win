from toga.style import Pack
from toga.colors import BLACK
from toga.constants import CENTER, BOTTOM, TOP, ROW, COLUMN


class BoxStyle():
    
    
    home_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        width = 305,
        height = 200,
    )
    
    home_buttons_box = Pack(
        direction = ROW,
        alignment = TOP
    )
    
    home_balances_box = Pack(
        direction = ROW,
        alignment = CENTER
    )
    
    home_total_balances_box = Pack(
        direction = ROW,
        alignment = CENTER
    )
    
    home_price_box = Pack(
        direction = ROW,
        alignment = BOTTOM
    )
    
    home_blockchain_info_box = Pack(
        direction = ROW,
        background_color = BLACK,
        padding = 2
    )