from toga.style.pack import Pack
from toga.colors import rgb, YELLOW, BLACK, GREEN
from toga.constants import CENTER, BOLD, MONOSPACE


class ButtonStyle():
    
    done_button = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 11,
        padding_top = 3,
        padding_bottom = 2,
        padding_left = 110,
        padding_right = 110,
        color = GREEN,
        background_color = BLACK
    )
    
    info_button = Pack(
        width = 21,
        height = 21,
        padding_top = 3,
        padding_bottom = 1,
        padding_left = 5,
        padding_right = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    switch_info_button = Pack(
        width = 21,
        height = 21,
        padding_top = 5,
        padding_bottom = 3,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    addnode_info = Pack(
        width = 21,
        height = 21,
        padding_top = 32,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    connect_info = Pack(
        width = 21,
        height = 21,
        padding_top = 80,
        padding_bottom = 3,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    rpcbind_info = Pack(
        width = 21,
        height = 21,
        padding_top = 32,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    rpcclienttimeout_info = Pack(
        width = 21,
        height = 21,
        padding_top = 52,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    rpcallowip_info = Pack(
        width = 21,
        height = 21,
        padding_top = 40,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )
    
    rpcconnect_info = Pack(
        width = 21,
        height = 21,
        padding_top = 45,
        padding_left = 5,
        color = YELLOW,
        background_color = BLACK
    )