from toga.style.pack import Pack
from toga.colors import BLACK, GRAY
from toga.constants import CENTER, COLUMN, ROW, RIGHT


class BoxStyle():


    explorer_main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    explorer_menu = Pack(
        direction = COLUMN,
        background_color = GRAY,
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


    transaction_details_box = Pack(
        direction = COLUMN,
        background_color = GRAY,
        padding = 5
    )

    confirmations_box = Pack(
        direction = ROW,
        background_color = GRAY
    )