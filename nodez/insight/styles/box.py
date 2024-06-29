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

    block_info = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    blockhash_box = Pack(
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

    addresses_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    transaction_address_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex=1
    )

    block_details_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )

    block_details_right_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    block_details_left_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    block_lines_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    block_txids_box = Pack(
        direction = COLUMN,
        padding = 5,
        background_color = GRAY
    )


    address_info = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    address_balances_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    address_balances_list_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    address_lines_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    address_transaction_box = Pack(
        direction = COLUMN,
        padding = 5,
        background_color = GRAY
    )