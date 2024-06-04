
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
    
        self.file = Group.FILE
        self.help = Group.HELP
        self.config = Group("Config")
        
        self.edit_config_cmd = Command(
            text="Edit config",
            group=self.config,
            enabled=True,
            tooltip="Edit bitcoinz.conf file",
            shortcut=Key.F2,
            action=True,
            order=0,
            section=0
        )
        
        self.start_config_cmd = Command(
            text="Start with <config file>",
            group=self.config,
            enabled=True,
            tooltip="Start the node with spcecific config file",
            shortcut=Key.F3,
            action=True,
            order=1,
            section=0
        )

        self.import_wallet_cmd = Command(
            text="Import wallet",
            group=self.file,
            enabled=True,
            tooltip="Import wallet.dat file",
            shortcut=Key.MOD_1 + Key.I,
            action=None,
            order=0,
            section=0
        )