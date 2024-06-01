import os

from toga import (
    App,
    Box,
    Label,
    Button,
    Divider,
    Switch,
    NumberInput,
    TextInput
)
from toga.constants import Direction
from toga.colors import RED
from toga.widgets.base import Widget

from ..styles.box import BoxStyle
from ..styles.label import LabelStyle
from ..styles.switch import SwitchStyle
from ..styles.button import ButtonStyle
from ..styles.input import InputStyle
        
        
        
        
class DiversConfig(Box):
    def __init__(
        self,
        app:App,
        id: str | None = None,
        style=None,
        children: list[Widget] | None = None,
    ):
        style = BoxStyle.divers_box
        super().__init__(id, style, children)
        self.app = app
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        self.file_path = os.path.join(config_path, config_file)
        
        self.divers_txt = Label(
            "Miscellaneous options",
            style=LabelStyle.title_txt
        )
        self.divers_divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.gen_switch = Switch(
            "gen",
            style=SwitchStyle.switch,
            on_change=lambda switch: self.update_config_switch(
                switch, "gen"
            )
        )
        self.genproclimit_txt = Label(
            "genproclimit :",
            style=LabelStyle.genproclimit_txt
        )
        self.equihashsolver_txt = Label(
            "equihashsolver :",
            style=LabelStyle.equihashsolver_txt
        )
        self.keypool_txt = Label(
            "keypool :",
            style=LabelStyle.keypool_txt
        )
        self.genproclimit_input = NumberInput(
            step=1,
            min=-1,
            style=InputStyle.genproclimit_input,
            on_change=lambda input: self.update_config_input(
                input, "genproclimit"
            )
        )
        self.keypool_input = NumberInput(
            step=1,
            min=0,
            style=InputStyle.keypool_input,
            on_change=lambda input: self.update_config_input(
                input, "keypool"
            )
        )
        self.equihashsolver_input = TextInput(
            placeholder="e.g. “tromp”",
            style=InputStyle.equihashsolver_input,
            on_lose_focus=lambda input: self.update_config_input(
                input, "equihashsolver"
            )
        )
        self.gen_info = Button(
            "?",
            id="gen",
            style=ButtonStyle.switch_info_button,
            on_press=self.display_info
        )
        self.genproclimit_info = Button(
            "?",
            id="genproclimit",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.equihashsolver_info = Button(
            "?",
            id="equihashsolver",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.keypool_info = Button(
            "?",
            id="keypool",
            style=ButtonStyle.info_button,
            on_press=self.display_info
        )
        self.divers_switch_box = Box(
            style=BoxStyle.divers_switch_box
        )
        self.divers_button_box = Box(
            style=BoxStyle.divers_button_box
        )
        self.divers_button2_box = Box(
            style=BoxStyle.divers_button2_box
        )
        self.divers_txt_box = Box(
            style=BoxStyle.divers_txt_box
        )
        self.divers_input_box = Box(
            style=BoxStyle.divers_input_box
        )
        self.divers_row_box = Box(
            style=BoxStyle.divers_row_box
        )
        self.divers_row2_box = Box(
            style=BoxStyle.divers_row2_box
        )
        self.divers_switch_box.add(
            self.gen_switch
        )
        self.divers_button_box.add(
            self.gen_info
        )
        self.divers_button2_box.add(
            self.genproclimit_info,
            self.equihashsolver_info,
            self.keypool_info
        )
        self.divers_txt_box.add(
            self.genproclimit_txt,
            self.equihashsolver_txt,
            self.keypool_txt
        )
        self.divers_row_box.add(
            self.divers_switch_box,
            self.divers_button_box
        )
        self.divers_row2_box.add(
            self.divers_txt_box,
            self.divers_input_box,
            self.divers_button2_box
        )
        self.add(
            self.divers_txt,
            self.divers_divider,
            self.divers_row_box,
            self.divers_row2_box
        )
        self.app.add_background_task(
            self.read_file_lines
        )
                
    
    async def read_file_lines(self, widget):
        gen = None
        genproclimit = None
        equihashsolver = None
        keypool = None
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if "=" in line:
                    key, value = map(str.strip, line.split('=', 1))
                    if key == "gen":
                        gen = value
                    elif key == "genproclimit":
                        genproclimit = value
                    elif key == "equihashsolver":
                        equihashsolver =value
                    elif key == "keypool":
                        keypool = value             
        await self.update_values(
            gen, genproclimit, equihashsolver, keypool
        )
        
    async def update_values(
        self,
        gen, genproclimit, equihashsolver, keypool
    ):
        self.gen_switch.value = (gen == "1")
        self.genproclimit_input.value = genproclimit
        self.equihashsolver_input.value = equihashsolver
        self.keypool_input.value = keypool
        self.divers_input_box.add(
            self.genproclimit_input,
            self.equihashsolver_input,
            self.keypool_input
        )
        
    
    def update_config_switch(self, switch, key):
        new_value = "1" if switch.value else "0"
        key_found = False
        updated_lines = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if "=" in stripped_line:
                current_key, value = map(str.strip, stripped_line.split('=', 1))
                if current_key == key:
                    updated_lines.append(f"{key}={new_value}\n")
                    key_found = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        if not key_found:
            updated_lines.append(f"{key}={new_value}\n")
        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)
            
            
    def update_config_input(self, input, key):
        current_value = input.value
        key_found = False
        updated_lines = []
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            stripped_line = line.strip()
            if "=" in stripped_line:
                current_key, value = map(str.strip, stripped_line.split('=', 1))
                if current_key == key:
                    if current_value is not None:
                        updated_lines.append(f"{key}={current_value}\n")
                    else:
                        updated_lines.append(f"{key}=\n")
                    key_found = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        if not key_found:
            if current_value is not None:
                updated_lines.append(f"{key}={current_value}\n")
            else:
                updated_lines.append(f"{key}=\n")
        with open(self.file_path, 'w') as file:
            file.writelines(updated_lines)
                    
                    
    def display_info(self, button):
        if button.id == "gen":
            info_message = "Enable attempt to mine BitcoinZ"
        elif button.id == "genproclimit":
            info_message = "Set the number of threads to be used for mining BitcoinZ (-1 = all cores)"
        elif button.id =="equihashsolver":
            info_message = "Specify a different Equihash solver (e.g. “tromp”) to try to mine BitcoinZ faster when gen=1"
        elif button.id == "keypool":
            info_message = "Pre-generate this many public/private key pairs, so wallet backups will be valid for both prior transactions and several dozen future transactions."
        self.app.main_window.info_dialog(
            "Info",
            info_message
        )