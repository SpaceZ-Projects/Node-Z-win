from toga.style.pack import Pack
from toga.constants import CENTER, BOLD
from toga.colors import BLACK, WHITE, GRAY



class LabelStyle():


    contacts_txt = Pack(
        font_size = 10,
        padding_top = 20,
        font_weight = BOLD,
        text_align = CENTER,
        color = GRAY,
        background_color = BLACK
    )

    
    amount_txt = Pack(
        padding_top = 15,
        color = GRAY,
        background_color = BLACK
    )

    
    fee_txt = Pack(
        padding_top = 15,
        padding_left = 42,
        padding_right = 5,
        color = GRAY,
        background_color = BLACK
    )


    memo_calculate = Pack(
        padding_top = 3,
        text_align = CENTER,
        background_color = BLACK,
        color = WHITE
    )