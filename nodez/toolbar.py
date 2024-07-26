
from toga import(
    App,
    Group,
    Command,
    Key
)


class Toolbar():
    def __init__(self, app:App):
        self.app = app
    
        self.start_group = Group(
            "Start",
            order=0
        )
        self.settings_group = Group(
            "Settings",
            order=1
        )
        
        self.custom_params = Command(
            text="Custom params",
            group=self.start_group,
            enabled=True,
            shortcut=Key.MOD_1 + Key.S,
            action=True,
            order=0,
            section=0
        )

        self.blockchain_dir = Command(
            text="Blockchain dir",
            group=self.settings_group,
            enabled=True,
            action=True,
            order=0,
            section=0
        )