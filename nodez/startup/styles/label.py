from toga.style.pack import Pack
from toga.colors import BLUE
from toga.constants import CENTER, BOLD, MONOSPACE


class LabelStyle():
    
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