from toga.style.pack import Pack
from toga.constants import CENTER, BOLD
from toga.colors import BLACK, WHITE, BLUE, GREENYELLOW



class LabelStyle():


    select_miner_txt = Pack(
        padding_top = 20,
        padding_left = 30,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    select_pool_txt = Pack(
        padding_top = 20,
        padding_left = 30,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    select_server_txt = Pack(
        padding_top = 20,
        padding_left = 30,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    worker_name_txt = Pack(
        padding_top = 17,
        padding_left = 30,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    select_address_txt = Pack(
        padding_top = 20,
        padding_left = 30,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    download_txt = Pack(
        font_weight = BOLD,
        text_align = CENTER,
        padding_top = 5,
        padding_bottom = 5
    )
    
    file_name_txt = Pack(
        text_align = CENTER,
        padding_top = 5,
        color = BLUE
    )


    mining_output_txt = Pack(
        padding_top = 2,
        padding_left = 5,
        font_size = 8,
        color = GREENYELLOW,
        background_color = BLACK
    )