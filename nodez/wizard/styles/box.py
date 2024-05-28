from toga.style import Pack
from toga.constants import CENTER, BOTTOM, TOP, ROW, COLUMN


class BoxStyle():
    
    setup_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER
    )
    
    social_main_box = Pack(
        direction = ROW
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
    
    wizard_row_center = Pack(
        direction = ROW,
        alignment = CENTER,
        flex = 1
    )
    
    wizard_row_bottom = Pack(
        direction = ROW,
        alignment = BOTTOM,
        flex = 1
    )