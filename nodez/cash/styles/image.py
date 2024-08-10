from toga.style.pack import Pack
from toga.colors import BLACK, GRAY
from toga.constants import HIDDEN, CENTER


class ImageStyle():
    
    
    transparent_icon = Pack(
        padding = 10,
        background_color = GRAY
    )
    
    shielded_icon = Pack(
        padding = 10,
        background_color = GRAY
    )
    
    verified_icon = Pack(
        visibility = HIDDEN,
        background_color = BLACK,
        padding_top = 8,
        padding_left = 5,
        padding_right = 200
    )
    
    invalid_icon = Pack(
        visibility = HIDDEN,
        background_color = BLACK,
        padding_top = 8,
        padding_left = 5,
        padding_right = 200
    )
    
    cash_icon = Pack(
        padding = 5,
        background_color = BLACK
    )
    
    
    loading_icon = Pack(
        alignment = CENTER,
        padding_top = 50
    )