from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW
from toga.constants import CENTER, BOLD, MONOSPACE


class SwitchStyle():
    
    config_net_switch = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 9,
        color = YELLOW,
        background_color = BLACK,
        padding = 5
    )