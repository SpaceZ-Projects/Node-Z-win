from toga.style.pack import Pack
from toga.colors import rgb, YELLOW, BLACK


class ButtonStyle():
    
    config_info_button = Pack(
        width = 21,
        height = 21,
        padding_top = 3,
        padding_bottom = 1,
        padding_left = 5,
        padding_right = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_net_info_button = Pack(
        width = 21,
        height = 21,
        padding_top = 5,
        padding_bottom = 3,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_addnode_info = Pack(
        width = 21,
        height = 21,
        padding_top = 32,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_connect_info = Pack(
        width = 21,
        height = 21,
        padding_top = 80,
        padding_bottom = 3,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_rpcbind_info = Pack(
        width = 21,
        height = 21,
        padding_top = 32,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_rpcclienttimeout_info = Pack(
        width = 21,
        height = 21,
        padding_top = 52,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_rpcallowip_info = Pack(
        width = 21,
        height = 21,
        padding_top = 40,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    config_rpcconnect_info = Pack(
        width = 21,
        height = 21,
        padding_top = 45,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    rpc_button = Pack(
        padding_right = 70
    )
    
    local_button = Pack(
        padding_left = 70
    )
    
    social_button = Pack(
        background_color = rgb(0, 0, 0)
    )
    
    menu_button = Pack(
        padding_right = 10,
        padding_left = 10
    )