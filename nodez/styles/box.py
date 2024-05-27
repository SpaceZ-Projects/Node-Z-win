from toga.style import Pack
from toga.colors import rgb, BLACK, GREY, WHITE, GRAY
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
    
    config_guide_box = Pack(
        direction = COLUMN,
        padding_top = 5,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    config_net_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    config_rpc_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    config_fee_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )

    config_option_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_bottom = 3,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    config_rpc_row_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_top = 3,
        padding_bottom = 3,
        padding_left = 3,
        padding_right = 3
    )
    
    config_net_row_box = Pack(
        direction = ROW,
        background_color = BLACK,
        padding_left = 3,
        padding_right = 3
    )
    
    config_net_row2_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_bottom = 3,
        padding_left = 3,
        padding_right = 3
    )
    
    config_net_switch_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK
    )
    
    config_net_txt_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1,
        background_color = GREY
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
    
    config_net_input_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = GREY
    )
    
    config_rpc_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = GREY
    )
    
    config_net_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK,
        flex = 1
    )
    
    config_net_button2_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
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