from toga.style.pack import Pack
from toga.colors import CYAN, BLACK


class InputStyle():
    
    rpc_input = Pack(
        background_color = BLACK,
        color = CYAN,
        padding_left = 20,
        padding_right = 20,
        padding_bottom = 10
    )


    custom_params_input = Pack(
        font_size = 10,
        background_color = BLACK,
        color = CYAN,
        padding_top = 15,
        padding_left = 8,
        flex =1
    )