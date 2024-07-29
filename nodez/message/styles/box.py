from toga.style.pack import Pack
from toga.colors import BLACK, GRAY
from toga.constants import COLUMN, ROW, CENTER, LEFT, RIGHT



class BoxStyle():


    main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    chat_main_box = Pack(
        direction = ROW,
        background_color = BLACK,
        flex = 1
    )


    banner_box = Pack(
        direction = COLUMN,
        background_color = GRAY,
        alignment = CENTER
    )

    contacts_box = Pack(
        direction = COLUMN,
        background_color = BLACK
    )

    discussion_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    chat_inputs_box = Pack(
        direction = ROW,
        background_color = BLACK
    )


    send_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )


    amount_box = Pack(
        direction = ROW,
        background_color = BLACK
    )