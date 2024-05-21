from toga.style.pack import Pack
from toga.colors import BLUE


class InputStyle():
    
    connect_rpcuser_input = Pack(
        font_family = "monospace",
        color = BLUE
    )
    
    connect_rpcpassword_input = Pack(
        color = BLUE
    )
    
    connect_rpchost_input = Pack(
        font_family = "monospace",
        color = BLUE
    )
    
    connect_rpcport_input = Pack(
        padding_bottom = 5,
        font_family = "monospace",
        color = BLUE
    )