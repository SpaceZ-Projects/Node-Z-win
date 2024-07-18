from toga.style.pack import Pack
from toga.colors import YELLOW


class ProgressStyle():
    
    setup_progress_bar = Pack(
        padding_left = 5,
        padding_right = 5,
        height = 20
    )
    
    setup_file_progress_bar = Pack(
        padding_left = 5,
        padding_right = 5,
        padding_top = 2,
        height = 5,
        background_color = YELLOW
    )