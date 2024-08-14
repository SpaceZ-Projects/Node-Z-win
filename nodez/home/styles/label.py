from toga.style.pack import Pack
from toga.colors import YELLOW, WHITE, BLACK, RED, CYAN, rgb
from toga.constants import BOLD, CENTER, HIDDEN


class LabelStyle():


    stopping_txt = Pack(
        font_weight = BOLD,
        text_align = CENTER,
        padding_top = 20,
        background_color = BLACK,
        color = WHITE
    )
    
    
    home_total_balances_txt = Pack(
        background_color = BLACK,
        color = WHITE,
        text_align = CENTER,
        font_weight = BOLD,
        font_size = 10,
        padding_top = 5
    )
    
    home_total_balances = Pack(
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        font_size = 11,
        padding_top = 5
    )
    
    home_transparent_balance_txt= Pack(
        color = WHITE,
        background_color = BLACK,
        font_weight = BOLD,
        padding_right = 5,
        padding_left = 5,
        padding_top = 5
    )
    
    home_transparent_balance= Pack(
        font_weight = BOLD,
        color = YELLOW,
        background_color = BLACK,
        padding_right = 20,
        padding_top = 5,
        flex = 1
    )
    
    home_private_balance_txt= Pack(
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        padding_right = 5,
        padding_left = 5
    )
    
    home_private_balance= Pack(
        font_weight = BOLD,
        color= CYAN,
        background_color = BLACK,
        padding_right = 20,
        flex = 1
    )
    
    home_unconfirmed_txt = Pack(
        visibility = HIDDEN,
        font_weight = BOLD,
        color= WHITE,
        background_color = BLACK,
        padding_right = 5,
        padding_left = 5
    )
    
    home_unconfirmed_balance = Pack(
        visibility = HIDDEN,
        font_weight = BOLD,
        color= RED,
        background_color = BLACK,
        padding_right = 20,
        flex = 1
    )
    
    home_price_txt = Pack(
        background_color = BLACK,
        color = WHITE,
        padding_top = 5,
        padding_left = 5
    )
    
    home_price_value = Pack(
        background_color = BLACK,
        color = WHITE,
        padding_top = 5,
        padding_left = 5,
        flex = 1
    )
    
    total_value_txt = Pack(
        background_color = BLACK,
        color = WHITE,
        padding_top = 5,
        padding_left = 5
    )
    
    total_value = Pack(
        background_color = BLACK,
        color = WHITE,
        padding_top = 5,
        padding_left = 5,
        flex = 1
    )
    
    home_chain_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3,
        padding_left = 18
    )
    
    home_chain_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_blocks_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )
    
    home_blocks_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_sync_txt = Pack(
        color = WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )
    
    home_sync_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_dep_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )
    
    home_dep_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_networksol_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )
    
    home_networksol_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )
    
    home_difficulty_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )
    
    home_difficulty_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )

    home_connected_node_txt = Pack(
        color= WHITE,
        background_color = BLACK,
        padding_top = 6,
        padding_bottom = 3
    )

    home_connected_node_value = Pack(
        background_color = WHITE,
        padding_top = 6,
        padding_right = 5,
        padding_bottom = 3
    )

    peer_column = Pack(
        padding_top = 15,
        padding_left = 45,
        padding_bottom = 15,
        background_color = BLACK,
        color = CYAN,
        font_weight = BOLD
    )

    node_column = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 20,
        padding_bottom = 15,
        background_color = BLACK,
        color = CYAN,
        font_weight = BOLD,
        flex = 1
    )

    default_column = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 10,
        background_color = BLACK,
        color = CYAN,
        font_weight = BOLD,
        flex = 1
    )

    option_column = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 10,
        padding_right = 10,
        background_color = BLACK,
        color = CYAN,
        font_weight = BOLD,
        flex = 1
    )

    peer_id_txt = Pack(
        padding_top = 15,
        padding_left = 8,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        visibility = HIDDEN
    )

    addr_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 10,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1,
        visibility = HIDDEN
    )

    addrlocal_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 10,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1,
        visibility = HIDDEN
    )

    syncedblocks_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 5,
        padding_right = 15,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1,
        visibility = HIDDEN
    )

    subver_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 5,
        padding_right = 5,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1,
        visibility = HIDDEN
    )

    pingtime_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_left = 5,
        padding_right = 25,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1,
        visibility = HIDDEN
    )


    node_id_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_right = 30,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1
    )

    addednode_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_right = 150,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1
    )


    address_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1
    )

    banned_until_txt = Pack(
        text_align = CENTER,
        padding_top = 15,
        padding_right = 120,
        background_color = BLACK,
        color = WHITE,
        font_weight = BOLD,
        flex = 1
    )


    info_label = Pack(
        font_size = 10,
        padding_left = 10,
        padding_top = 7,
        color = WHITE,
        background_color = BLACK,
        font_weight = BOLD,
    )