from toga.style import Pack
from toga.constants import CENTER, ROW, COLUMN


class BoxStyle():
    
    main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding = 5
    )
    
    button_box = Pack(
        direction = ROW,
        padding_top = 5
    )