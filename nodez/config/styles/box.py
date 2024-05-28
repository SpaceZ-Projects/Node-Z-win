from toga.style import Pack
from toga.colors import rgb, BLACK, GREY, WHITE, GRAY
from toga.constants import CENTER, BOTTOM, TOP, ROW, COLUMN, RIGHT, LEFT


class BoxStyle():
    
    
    main_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1
    )
    
    button_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding = 5
    )
    
    scroll_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1
    )
    
    guide_box = Pack(
        direction = COLUMN,
        padding_top = 5,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    net_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    rpc_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    fee_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )

    option_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        padding_top = 2,
        padding_bottom = 3,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK
    )
    
    rpc_row_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_top = 3,
        padding_bottom = 3,
        padding_left = 3,
        padding_right = 3
    )
    
    net_row_box = Pack(
        direction = ROW,
        background_color = BLACK,
        padding_left = 3,
        padding_right = 3
    )
    
    fee_row_box = Pack(
        direction = ROW,
        background_color = BLACK,
        padding_left = 3,
        padding_right = 3
    )
    
    net_row2_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_bottom = 3,
        padding_left = 3,
        padding_right = 3
    )
    
    fee_row2_box = Pack(
        direction = ROW,
        background_color = GREY,
        padding_bottom = 3,
        padding_left = 3,
        padding_right = 3
    )
    
    net_switch_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK
    )
    
    fee_switch_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK
    )
    
    net_txt_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1,
        background_color = GREY
    )
    
    fee_txt_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1,
        background_color = GREY
    )
    
    rpc_txt_box = Pack(
        direction = COLUMN,
        alignment = CENTER,
        flex = 1,
        background_color = GREY
    )
    
    rpc_input_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = GREY
    )
    
    net_input_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = GREY
    )
    
    fee_input_box = Pack(
        direction = COLUMN,
        flex = 1,
        background_color = GREY
    )
    
    rpc_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = GREY
    )
    
    net_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK,
        flex = 1
    )
    
    net_button2_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = GREY
    )
    
    fee_button_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = BLACK,
        flex = 1
    )
    
    fee_button2_box = Pack(
        direction = COLUMN,
        alignment = LEFT,
        background_color = GREY
    )