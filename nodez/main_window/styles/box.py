from toga.style import Pack
from toga.constants import CENTER, BOTTOM, TOP, ROW, COLUMN
from toga.colors import BLACK, YELLOW, WHITE


class BoxStyle():
    
    connect_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding = 5
    )
    
    connect_button_box = Pack(
        direction = ROW,
        padding_top = 5
    )
    
    social_main_box = Pack(
        direction = ROW
    )
    
    start_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER
    )
    
    download_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER
    )
    
    wizard_main_box = Pack(
        direction = COLUMN,
        width = 405,
        height = 400,
        alignment = CENTER
    )
    
    wizard_nodez_banner = Pack(
        direction= COLUMN
    )
    
    wizard_row_top = Pack(
        direction = ROW,
        alignment = TOP
    )
    
    wizard_center = Pack(
        direction = COLUMN,
        alignment = CENTER,
    )
    
    wizard_local_row = Pack(
        direction = ROW,
        padding_top = 30,
        background_color = BLACK,
        width = 450,
        height = 100,
    )
    
    wizard_rpc_row = Pack(
        direction = ROW,
        padding = 3,
        background_color = BLACK,
        width = 450,
        height = 100,
    )
    
    wizard_row_bottom = Pack(
        direction = ROW,
        alignment = BOTTOM,
        flex = 1
    )