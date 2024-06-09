from toga.style import Pack
from toga.colors import BLACK
from toga.constants import CENTER, ROW, COLUMN


class BoxStyle():
    
    
    home_main_box = Pack(
        direction = ROW,
        width = 695,
        height = 150
    )
    
    home_node_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        background_color = BLACK,
        width = 200,
        height = 150
    )
    
    balances_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    price_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    total_value_box = Pack(
        direction = ROW,
        background_color = BLACK
    )
    
    home_menu_box = Pack(
        direction = COLUMN,
    )
    
    home_blockchain_info_box = Pack(
        direction = ROW,
        background_color = BLACK,
        width = 695,
        height = 30
    )
    
    home_buttons_box = Pack(
        direction = ROW,
        background_color = BLACK,
        width = 695,
        height = 110
    )