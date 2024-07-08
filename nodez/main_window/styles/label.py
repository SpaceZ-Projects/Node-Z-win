from toga.style.pack import Pack
from toga.constants import BOLD, MONOSPACE, CENTER
from toga.colors import BLACK, WHITE, BLUE, YELLOW


class LabelStyle():
    
    version_text_style = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 8,
        padding_bottom =5
    )
    
    loading_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        font_size = 10,
    )
    
    node_files_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 32,
        padding_left = 20
    )
    
    params_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 32,
        padding_left = 10
    )
    
    config_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 32,
        padding_left = 10
    )
    
    rpc_description_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 38,
        padding_left = 20
    )
    
    starting_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        text_align = CENTER,
        padding_top = 5,
        padding_bottom = 5
    )
    
    download_txt = Pack(
        font_family = MONOSPACE,
        font_weight = BOLD,
        text_align = CENTER,
        padding_top = 5,
        padding_bottom = 5
    )
    
    file_name_txt = Pack(
        text_align = CENTER,
        padding_top = 5,
        color = BLUE
    )
    
    rpc_txt = Pack(
        font_weight = BOLD,
        font_size = 10,
        padding_bottom = 5,
        padding_top = 5,
        padding_left = 20,
        background_color = BLACK,
        color = YELLOW
    )
    
    status_txt = Pack(
        font_weight = BOLD,
        font_size = 10,
        text_align = CENTER,
        color = WHITE,
        background_color = BLACK,
        padding_top = 15
    )