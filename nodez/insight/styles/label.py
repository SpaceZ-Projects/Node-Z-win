from toga.style.pack import Pack
from toga.colors import BLACK, WHITE, RED, GRAY, BURLYWOOD
from toga.constants import CENTER, BOLD, RIGHT, LEFT


class LabelStyle():

    not_found = Pack(
        text_align = CENTER,
        padding_top = 30,
        font_size = 14,
        color = RED,
        background_color = BLACK
    )


    transaction_title = Pack(
        padding_top = 15,
        text_align = CENTER,
        font_size = 18,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )


    transaction_id_txt = Pack(
        padding_top = 10,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    
    transaction_id = Pack(
        text_align = RIGHT,
        padding_top = 11,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_received_time_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex=1
    )


    transaction_received_time = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_mined_time_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_mined_time = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_blockhash_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )


    transaction_blockhash = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_version_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_version = Pack(
        text_align = RIGHT,
        padding_top = 7,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_overwintered_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_overwintered = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_versiongroupid_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_versiongroupid = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    transaction_expiryheight_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_expiryheight = Pack(
        text_align = RIGHT,
        padding_top = 7,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    transaction_coinbase_txt = Pack(
        padding_top = 5,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )

    transaction_coinbase = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    transaction_details_title = Pack(
        padding_top = 5,
        text_align = CENTER,
        font_size = 15,
        font_weight = BOLD,
        color = BLACK,
        background_color = GRAY
    )

    transaction_confirmations = Pack(
        text_align = CENTER,
        font_size = 10,
        padding_top = 10,
        padding_bottom = 10,
        padding_left = 430,
        color = BLACK,
        font_weight = BOLD
    )

    transaction_value = Pack(
        text_align = CENTER,
        font_size = 10,
        padding_top = 10,
        padding_bottom = 10,
        padding_left = 5,
        color = BLACK,
        font_weight = BOLD,
        background_color = BURLYWOOD
    )

    transaction_vin_address = Pack(
        text_align = CENTER,
        background_color = BLACK,
        color = WHITE,
        padding_top = 5
    )

    transaction_vout_address = Pack(
        text_align = CENTER,
        background_color = BLACK,
        color = WHITE,
        padding_top = 5,
        padding_bottom = 5
    )


    blocks_title = Pack(
        padding_top = 15,
        text_align = CENTER,
        font_size = 18,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )


    block_blockhash_txt = Pack(
        padding_top = 10,
        padding_left = 15,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_blockhash = Pack(
        text_align = RIGHT,
        padding_top = 11,
        padding_right = 15,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    summary_title = Pack(
        padding_top = 5,
        text_align = CENTER,
        font_size = 15,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    block_number_txids_txt = Pack(
        text_align = LEFT,
        padding_top = 10,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_number_txids = Pack(
        text_align = RIGHT,
        padding_top = 12,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_height_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )


    block_height = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_reward_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_reward = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_timestamp_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_timestamp = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    block_merkleroot_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_merkleroot = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_coinbase_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_coinbase = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )


    block_difficulty_txt = Pack(
        text_align = LEFT,
        padding_top = 10,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_difficulty = Pack(
        text_align = RIGHT,
        padding_top = 12,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_bits_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_bits = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_size_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_size = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_version_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_version = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_nonce_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_nonce = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_solution_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 10,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    block_solution = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    block_transaction_id = Pack(
        text_align = LEFT,
        padding = 10,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
    )

    address_title = Pack(
        padding_top = 15,
        text_align = CENTER,
        font_size = 16,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    address_total_received_txt = Pack(
        text_align = LEFT,
        padding_top = 40,
        padding_left = 20,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    address_total_received = Pack(
        text_align = RIGHT,
        padding_top = 42,
        padding_right = 20,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    address_total_sent_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 20,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    address_total_sent = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 20,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    address_final_balance_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 20,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    address_final_balance = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 20,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    address_number_transactions_txt = Pack(
        text_align = LEFT,
        padding_top = 5,
        padding_left = 20,
        font_size = 11,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
        flex= 1
    )

    address_number_transactions = Pack(
        text_align = RIGHT,
        padding_top = 6,
        padding_right = 20,
        font_size = 10,
        color = WHITE,
        background_color = BLACK
    )

    address_transactions_title = Pack(
        text_align = CENTER,
        padding_top = 10,
        font_size = 16,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK
    )

    address_transaction_id = Pack(
        text_align = LEFT,
        padding = 10,
        font_size = 10,
        font_weight = BOLD,
        color = WHITE,
        background_color = BLACK,
    )