from toga.style.pack import Pack
from toga.colors import BLUE


class InputStyle():
    
    rpcuser_input = Pack(
        font_family = "monospace",
        color = BLUE
    )
    
    rpcpassword_input = Pack(
        color = BLUE
    )
    
    rpchost_input = Pack(
        font_family = "monospace",
        color = BLUE
    )
    
    rpcport_input = Pack(
        padding_bottom = 5,
        font_family = "monospace",
        color = BLUE
    )