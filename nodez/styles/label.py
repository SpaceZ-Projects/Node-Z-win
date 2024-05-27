from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb, RED, YELLOW, BLUE, WHITE, BLACK, GREY, GRAY
from toga.constants import CENTER, BOLD, MONOSPACE


class LabelStyle():
    
    connect_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 10,
        padding_bottom = 5,
        padding_top = 5
    )
    
    config_guide_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 3,
        padding_bottom = 5,
        padding_left = 5
    )
    
    config_rpc_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        text_align = CENTER,
        font_size = 10,
        color = YELLOW,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 5,
    )
    
    config_rpcuser_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 5,
        padding_left = 5
    )
    
    config_rpcpassword_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 8,
        padding_left = 5
    )
    
    config_rpcport_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 9,
        padding_left = 5
    )
    
    config_rpcbind_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 40,
        padding_left = 5
    )
    
    config_rpcclienttimeout_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 55,
        padding_left = 5
    )
    
    config_rpcallowip_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 45,
        padding_left = 5
    )
    
    config_rpcconnect_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 50,
        padding_left = 5
    )
    
    config_proxy_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 5,
        padding_left = 5
    )
    
    config_bind_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 8,
        padding_left = 5
    )
    
    config_whitebind_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 9,
        padding_left = 5
    )
    
    config_maxconnections_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 8,
        padding_left = 5
    )
    
    config_addnode_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 40,
        padding_left = 5
    )
    
    config_connect_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = WHITE,
        background_color = GREY,
        padding_top = 85,
        padding_left = 5
    )
    
    home_total_balances_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 11,
        padding_right = 5
    )
    
    home_total_balances = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 12,
        padding_left = 5
    )
    
    home_transparent_balance_txt= Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        padding_right = 5
    )
    
    home_transparent_balance= Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        background_color = YELLOW,
        padding_right = 5
    )
    
    home_private_balance_txt= Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        padding_left = 5
    )
    
    home_private_balance= Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        color= WHITE,
        background_color = BLUE,
        padding_left = 5
    )
    
    home_price_txt = Pack(
        font_family = MONOSPACE
    )
    
    home_chain_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3,
    )
    
    home_chain_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_blocks_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_blocks_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_sync_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_sync_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_dep_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_dep_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    setup_cheking_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        text_align = CENTER,
        padding_top = 5,
        padding_bottom = 5
    )
    
    setup_file_name_txt = Pack(
        text_align = CENTER,
        padding_top = 5,
        color = BLUE
    )
    
    version_text_style = Pack(
        font_family = MONOSPACE,
        font_size = 8,
        padding_bottom =5
    )
    
    default_txt_bold_style = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 10,
    )
    
    default_txt_style = Pack(
        font_family = MONOSPACE,
        font_size = 10,
    )