from toga.style.pack import Pack
from toga.colors import rgb


class ButtonStyle():
    
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