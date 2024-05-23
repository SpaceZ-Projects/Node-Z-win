from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb, RED, YELLOW, BLUE, WHITE, BLACK


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
    
    home_price_txt = Pack(
        font_family = "monospace"
    )
    
    home_chain_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3,
    )
    
    home_chain_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_blocks_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_blocks_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_sync_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_sync_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_dep_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 5,
        padding_bottom = 3
    )
    
    home_dep_value = Pack(
        background_color = WHITE,
        padding_top = 5,
        padding_right = 5,
        padding_bottom = 3
    )
    
    setup_cheking_txt = Pack(
        font_family = "monospace",
        font_weight = "bold",
        text_align = "center",
        padding_top = 5,
        padding_bottom = 5
    )
    
    setup_file_name_txt = Pack(
        text_align = "center",
        padding_top = 5,
        color = BLUE
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