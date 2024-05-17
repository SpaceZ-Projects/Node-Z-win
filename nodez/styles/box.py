from toga.style.pack import Pack, COLUMN, ROW
from toga.colors import rgb


class BoxStyle():
        
    main_box = Pack(
        direction = COLUMN,
    )
    
    clomun_box_center = Pack(
        direction = COLUMN,
        alignment = "center",
        flex = 1
    )
    
    row_box_top = Pack(
        direction = ROW,
        alignment = "top",
        flex = 1
    )
    
    row_box_center = Pack(
        direction = ROW,
        alignment = "center",
        flex = 1
    )
    
    row_box_bottom = Pack(
        direction = ROW,
        alignment = "bottom",
        flex = 1
    )
    
    nodez_banner_box = Pack(
        direction= COLUMN,
        alignment="center"
    )