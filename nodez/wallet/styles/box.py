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
        direction = ROW,
        flex = 1,
        background_color = BLACK,
        alignment = CENTER
    )

    switch_button_box = Pack(
        direction = ROW,
        background_color = GRAY,
        padding = 3
    )

    buttons_box = Pack(
        direction = ROW,
        background_color = BLACK
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
        padding_top = 20,
        padding_left = 5,
        padding_right = 5,
        padding_bottom = 5,
        flex = 1
    )


    address_balance_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        padding_top = 20,
        padding_right = 5,
        padding_left = 5,
        flex = 1
    )


    address_buttons_box = Pack(
        direction = COLUMN,
        background_color = GRAY
    )

    txids_list_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    transaction_box = Pack(
        direction = ROW,
        padding = 2,
        background_color = BLACK
    )

    transaction_address_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        width = 350
    )

    transaction_amount_box = Pack(
        direction = COLUMN,
        background_color = BLACK
    )

    transaction_time_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    navigation_box = Pack(
        direction =COLUMN,
        background_color = GRAY,
        alignment = CENTER
    )

    navigation_buttons_box = Pack(
        direction = ROW,
        background_color = GRAY
    )

    import_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    import_button_box = Pack(
        alignment = CENTER,
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    wallet_manage_box = Pack(
        direction = COLUMN,
        background_color = BLACK
    )

    merge_operation_box = Pack(
        alignment = CENTER,
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    merge_result_box = Pack(
        direction = COLUMN,
        background_color = BLACK
    )

    merge_manage_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )


    merge_buttons_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )

    merge_fee_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )