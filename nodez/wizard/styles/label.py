from toga.style.pack import Pack
from toga.constants import BOLD, MONOSPACE


class LabelStyle():
    
    version_text_style = Pack(
        font_family = MONOSPACE,
        font_size = 8,
        padding_bottom =5
    )
    
    loading_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 10,
    )