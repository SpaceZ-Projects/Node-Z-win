from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb, RED


class LabelStyle():
    
    version_text_style = Pack(
        font_family = "monospace",
        font_size = 8,
        padding_bottom =5
    )
    
    default_txt_bold_style = Pack(
        font_family = "monospace",
        font_weight = "bold",
        font_size = 10,
    )
    
    default_txt_style = Pack(
        font_family = "monospace",
        font_size = 10,
    )