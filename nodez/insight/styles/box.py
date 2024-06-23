from toga.style.pack import Pack
from toga.colors import BLACK
from toga.constants import CENTER, COLUMN, ROW


class BoxStyle():


    explorer_main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    transaction_info = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    transaction_info_box = Pack(
        direction = ROW,
        background_color = BLACK
    )