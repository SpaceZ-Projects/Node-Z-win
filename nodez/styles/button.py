from toga.style.pack import Pack
from toga.colors import rgb, YELLOW, BLACK


class ButtonStyle():
    
    config_info_button = Pack(
        width = 21,
        height = 21,
        padding_top = 3,
        padding_bottom = 1,
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