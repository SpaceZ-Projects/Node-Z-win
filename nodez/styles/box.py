from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb, BLACK


class BoxStyle():
    
    connect_main_box = Pack(
        direction = COLUMN,
        alignment = "center",
        padding = 5
    )
    
    connect_button_box = Pack(
        direction = ROW,
        padding_top = 5
    )
    
    home_main_box = Pack(
        direction = COLUMN,
        alignment ="center",
        width = 305,
        height = 200,
    )
    
    home_buttons_box = Pack(
        direction = ROW,
        alignment = "top"
    )
    
    home_balances_box = Pack(
        direction = ROW,
        alignment = "center"
    )
    
    home_total_balances_box = Pack(
        direction = ROW,
        alignment = "center"
    )
    
    home_price_box = Pack(
        direction = ROW,
        alignment = "bottom"
    )
    
    home_blockchain_info_box = Pack(
        direction = ROW,
        background_color = BLACK,
        padding = 2
    )
    
    setup_main_box = Pack(
        direction = COLUMN,
        alignment ="center"
    )
    
    social_main_box = Pack(
        direction = ROW
    )
    
    wizard_main_box = Pack(
        direction = COLUMN,
        width = 405,
        height = 400,
        alignment = "center"
    )
    
    wizard_nodez_banner = Pack(
        direction= COLUMN
    )
    
    wizard_row_top = Pack(
        direction = ROW,
        alignment = "top"
    )
    
    wizard_row_center = Pack(
        direction = ROW,
        alignment = "center",
        flex = 1
    )
    
    wizard_row_bottom = Pack(
        direction = ROW,
        alignment = "bottom",
        flex = 1
    )