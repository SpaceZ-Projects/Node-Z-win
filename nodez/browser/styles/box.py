from toga.style import Pack
from toga.colors import BLACK
from toga.constants import CENTER, ROW, COLUMN


class BoxStyle():
    
    navigator_main_box = Pack(
        direction=COLUMN,
        background_color = BLACK
    )
    
    navigator_barre_box = Pack(
        direction=ROW,
        alignment=CENTER,
        padding=5,
        background_color = BLACK
    )