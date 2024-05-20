from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb


class BoxStyle():
        
    column = Pack(
        direction = COLUMN
    )
    
    column_center = Pack(
        direction= COLUMN,
        alignment="center"
    )
    
    column_center_padding_5 = Pack(
        direction= COLUMN,
        alignment="center",
        padding = 5
    )
    
    clomun_center_flex = Pack(
        direction = COLUMN,
        alignment = "center",
        flex = 1
    )
    
    row = Pack(
        direction = ROW
    )
    
    row_top_flex = Pack(
        direction = ROW,
        alignment = "top"
    )
    
    row_center_flex = Pack(
        direction = ROW,
        alignment = "center",
        flex = 1
    )
    
    row_bottom_flex = Pack(
        direction = ROW,
        alignment = "bottom",
        flex = 1
    )