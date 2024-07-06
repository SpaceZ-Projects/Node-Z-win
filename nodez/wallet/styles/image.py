from toga.style.pack import Pack
from toga.constants import CENTER
from toga.colors import BLACK, GRAY


class ImageStyle():


    loading_icon = Pack(
        alignment = CENTER
    )

    transparent_icon = Pack(
        padding = 10,
        background_color = GRAY
    )
    
    shielded_icon = Pack(
        padding = 10,
        background_color = GRAY
    )

    qr_code_img = Pack(
        width = 155,
        height = 155,
        padding = 20,
        background_color = BLACK
    )

    cash_icon = Pack(
        padding = 5,
        background_color = BLACK
    )