from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb


class LabelStyle():
    
    version_text_style = Pack(
        font_family = "monospace",
        font_size = 8,
        padding_bottom =5
    )
    
    loading_txt_style = Pack(
        font_family = "monospace",
        font_weight = "bold",
        font_size = 10,
    )