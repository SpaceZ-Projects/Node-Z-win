from toga.style.pack import Pack
from toga.colors import BLACK, WHITE, CYAN



class OutputStyle():


    discussion_outputs = Pack(
        font_size = 12,
        padding = 5,
        flex = 1,
        background_color = BLACK,
        color = WHITE
    )


    contacts_list = Pack(
        flex = 1,
        background_color = BLACK,
        color = CYAN,
        padding_bottom = 5
    )