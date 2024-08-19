from toga.style.pack import Pack
from toga.colors import BLACK
from toga.constants import COLUMN, ROW, CENTER



class BoxStyle():


    mining_main_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        flex = 1
    )

    select_miner_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    select_pool_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    select_server_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    worker_name_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    worker_pass_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    select_address_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    download_main_box = Pack(
        direction = COLUMN,
        alignment = CENTER
    )

    mining_output_box = Pack(
        direction = COLUMN,
        background_color = BLACK,
        padding_bottom = 5,
        flex = 1
    )

    params_box = Pack(
        direction = ROW,
        background_color = BLACK
    )

    options_box = Pack(
        direction = COLUMN,
        background_color= BLACK,
        flex = 1
    )

    gpuinfo_box = Pack(
        direction = COLUMN,
        background_color= BLACK,
        flex = 1
    )