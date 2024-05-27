
from toga import(
    App,
    Group,
    Command,
    Key,
    Icon
)


class Toolbar():
    def __init__(self, app:App):
        self.app = app
    
    file = Group.FILE
    help = Group.HELP
    utils = Group("Utils")
    
    config_cmd = Command(
        text="Edit config",
        group=utils,
        enabled=True,
        tooltip="Edit bitcoinz.conf file",
        shortcut=Key.F2,
        action=True,
        order=0,
        section=0
    )

    import_wallet_cmd = Command(
        text="Import wallet",
        group=file,
        enabled=True,
        tooltip="Import wallet.dat file",
        shortcut=Key.MOD_1 + Key.I,
        action=None,
        order=0,
        section=0
    )