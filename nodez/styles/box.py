from toga.style import Pack
from toga.colors import rgb, BLACK, GREY, WHITE
from toga.constants import CENTER, BOTTOM, TOP, ROW, COLUMN, RIGHT, LEFT


class BoxStyle():
    
    connect_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding = 5
    )
    
    connect_button_box = Pack(
        direction = ROW,
        padding_top = 5
    )
    
    config_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1
    )
    
    config_rpc_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding = 5,
        flex = 1,
        background_color = BLACK
    )
    
    config_rpc_row_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_left = 3,
        padding_right = 3
    )
    
    config_rpc_txt_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1,
        background_color = GREY
    )
    
    config_rpc_input_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = GREY
    )
    
    config_rpc_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        flex = 1,
        background_color = GREY
    )
    
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
    
    setup_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER
    )
    
    social_main_box = Pack(
        direction = ROW
    )
    
    wizard_main_box = Pack(
        direction = COLUMN,
        width = 405,
        height = 400,
        alignment = CENTER
    )
    
    wizard_nodez_banner = Pack(
        direction= COLUMN
    )
    
    wizard_row_top = Pack(
        direction = ROW,
        alignment = TOP
    )
    
    wizard_row_center = Pack(
        direction = ROW,
        alignment = CENTER,
        flex = 1
    )
    
    wizard_row_bottom = Pack(
        direction = ROW,
        alignment = BOTTOM,
        flex = 1
    )