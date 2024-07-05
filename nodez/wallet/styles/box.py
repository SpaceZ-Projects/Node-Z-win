from toga.style.pack import Pack
from toga.colors import BLACK, GRAY
from toga.constants import COLUMN, ROW, CENTER, LEFT, RIGHT



class BoxStyle():


    wallet_main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    loading_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = BLACK,
        alignment = CENTER
    )

    switch_button_box = Pack(
        direction = ROW,
        background_color = GRAY,
        padding = 3
    )


    select_address_box = Pack(
        direction = ROW,
        background_color = BLACK
    )


    address_manage_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        background_color = BLACK,
        flex = 1
    )

    address_info_box = Pack(
        direction = ROW,
        background_color = GRAY,
        padding_top = 50,
        padding_left = 5,
        padding_right = 5,
        padding_bottom = 5,
        flex = 1
    )

    address_buttons_box = Pack(
        direction = COLUMN,
        background_color = GRAY,
        flex = 1
    )