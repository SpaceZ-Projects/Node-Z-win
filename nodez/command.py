
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
    config = Group("Config")
    
    config_cmd = Command(
        text="Edit config",
        group=config,
        enabled=True,
        tooltip="Edit bitcoinz.conf file",
        shortcut=Key.F2,
        action=True,
        order=0,
        section=0
    )
    
    start_config_cmd = Command(
        text="Start with <config file>",
        group=config,
        enabled=True,
        tooltip="Start the node with spcecific config file",
        shortcut=Key.F3,
        action=True,
        order=1,
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