from toga.style.pack import Pack
from toga.colors import BLACK, WHITE, RED
from toga.constants import CENTER, BOLD, RIGHT


class LabelStyle():

    not_found = Pack(
        text_align = CENTER,
        padding_top = 30,
        font_size = 14,
        color = RED,
        background_color = BLACK
    )


    transaction_title = Pack(
        padding_top = 15,
        text_align = CENTER,
        font_size = 18,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )


    transcation_id_txt = Pack(
        padding_top = 10,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    
    transcation_id = Pack(
        text_align = RIGHT,
        padding_top = 11,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    received_time_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex=1
    )


    received_time = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    mined_time_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    mined_time = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    blockhash_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )


    blockhash = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    version_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    version = Pack(
        text_align = RIGHT,
        padding_top = 7,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    overwintered_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    overwintered = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    versiongroupid_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    versiongroupid = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    expiryheight_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    expiryheight = Pack(
        text_align = RIGHT,
        padding_top = 7,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    coinbase_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    coinbase = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )