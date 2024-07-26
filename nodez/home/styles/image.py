from toga.style.pack import Pack
from toga.colors import BLACK
from toga.constants import HIDDEN


class ImageStyle():
    
    btcz_coin = Pack(
        background_color = BLACK,
        padding_top = 8
    )

    peer_image = Pack(
        padding_top = 5,
        visibility = HIDDEN
    )


    status_icon = Pack(
        width = 27,
        height = 27,
        padding_top = 10,
        padding_right = 160,
        background_color = BLACK,
        visibility = HIDDEN
    )