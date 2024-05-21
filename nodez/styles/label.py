from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb, RED, YELLOW, BLUE, WHITE


class LabelStyle():
    
    connect_txt = Pack(
        font_family = "monospace",
        font_weight = "bold",
        font_size = 10,
        padding_bottom = 5,
        padding_top = 5
    )
    
    home_total_balances_txt = Pack(
        font_family = "monospace",
        font_weight = "bold",
        font_size = 11,
        padding_right = 5
    )
    
    home_total_balances = Pack(
        font_family = "monospace",
        font_weight = "bold",
        font_size = 12,
        padding_left = 5
    )
    
    home_transparent_balance_txt= Pack(
        font_family = "monospace",
        font_weight = "bold",
        padding_right = 5
    )
    
    home_transparent_balance= Pack(
        font_family = "monospace",
        font_weight = "bold",
        background_color = YELLOW,
        padding_right = 5
    )
    
    home_private_balance_txt= Pack(
        font_family = "monospace",
        font_weight = "bold",
        padding_left = 5
    )
    
    home_private_balance= Pack(
        font_family = "monospace",
        font_weight = "bold",
        color= WHITE,
        background_color = BLUE,
        padding_left = 5
    )
    
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