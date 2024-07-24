
import asyncio
import os
import subprocess
import json
import shutil

from toga import (
    App,
    Window,
    Box,
    Label,
    Divider,
    ImageView
)
from toga.constants import Direction

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..home.home import HomeWindow
from ..system import SystemOp


class StartNode(Window):
    def __init__(self, app:App, local_button):
        super().__init__(
            title="Loading...",
            size=(250, 300),
            resizable=False,
            minimizable=False,
            closable=False
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.local_button = local_button
        self.bitcoinzd_file = os.path.join(self.app.paths.data, "bitcoinzd.exe")
        
        self.loading_image = ImageView(
            "icones/loading_blocks.gif"
        )
        self.starting_txt = Label(
            "Starting Node...",
            style=LabelStyle.starting_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.start_divider
        )
        self.main_box = Box(
            style=BoxStyle.start_main_box
        )
        self.main_box.add(
            self.loading_image,
            self.divider_top,
            self.starting_txt
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.check_node_status
        )


    async def check_node_status(self, widget):
        self.local_button.enabled = False
        result = await self.getNodeStatus()
        if result:
            self.app.main_window.hide()
            self.local_button.enabled = True
            await asyncio.sleep(1)
            self.home_window = HomeWindow(self.app)
            self.home_window.title = "MainMenu (Local)"
        else:
            self.local_button.enabled = True
            await self.start_node()
    
    
    async def start_node(self):
        settings_path = os.path.join(self.app.paths.config, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                blockchain_path = settings_data.get('blockchainpath')
                if 'blockchainpath' not in settings_data:
                    async def on_confirm(window, result):
                        if result is True:
                            await self.setup_blockchain_path()
                        if result is False:
                            command = [self.bitcoinzd_file]
                            await self.run_node(command)
                    self.question_dialog(
                        "Blockchain path...",
                        "Do you want to set a custom path for the blockchain index ?",
                        on_result=on_confirm
                    )
                    return
                elif blockchain_path is not None:
                    command = [self.bitcoinzd_file, f'-datadir={blockchain_path}']
                await self.run_node(command)
        else:
            async def on_confirm(window, result):
                if result is True:
                    await self.setup_blockchain_path()
                if result is False:
                    command = [self.bitcoinzd_file]
                    await self.run_node(command)
            self.question_dialog(
                "Blockchain path...",
                "Do you want to set a custom path for the blockchain index ?",
                on_result=on_confirm
            )
    

    async def setup_blockchain_path(self):
        config_file = "bitcoinz.conf"
        config_path = os.path.join(os.getenv('APPDATA'), "BitcoinZ")
        file_path = os.path.join(config_path, config_file)
        async def on_confirm(window, path):
            if path:
                blockchain_path = path
                if isinstance(blockchain_path, os.PathLike):
                    blockchain_path = str(blockchain_path)
                self.system.update_settings('blockchainpath', blockchain_path)
                command = [self.bitcoinzd_file, f'-datadir={blockchain_path}']     
                target_file_path = os.path.join(blockchain_path, config_file)
                shutil.copyfile(file_path, target_file_path)
                await asyncio.sleep(1)
                await self.run_node(command)
        self.select_folder_dialog(
            "Select path",
            initial_directory=self.app.paths.data,
            on_result=on_confirm
        )


    async def run_node(self, command):
        self.app.main_window.hide()
        self.show()
        await asyncio.sleep(1)
        await asyncio.create_subprocess_exec(
                *command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
        )
        await self.waiting_node_status()
        
        
    async def waiting_node_status(self):
        await asyncio.sleep(1)
        result, error_message = await self.getNodeStatus()
        if result:
            self.home_window = HomeWindow(self.app)
            self.home_window.title = "MainMenu (Local)"
            self.close()
            return
        else:
            while True:
                result, error_message = await self.getNodeStatus()
                if result:
                    self.starting_txt.text = "Starting GUI..."
                    self.home_window = HomeWindow(self.app)
                    self.home_window.title = "MainMenu (Local)"
                    self.close()
                    return
                else:
                    if error_message:
                        self.starting_txt.text = error_message

                await asyncio.sleep(4)
        

        
    async def getNodeStatus(self):
        data_path = self.app.paths.data
        bitcoinz_cli_file = os.path.join(data_path, "bitcoinz-cli.exe")

        command = f'{bitcoinz_cli_file} getinfo'
        return await self._start_command(command)
    

    

    async def _start_command(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                if stdout:
                    try:
                        data = json.loads(stdout.decode())
                        result = json.dumps(data, indent=4)
                        return result, None
                    except json.JSONDecodeError:
                        return stdout.decode().strip()
                else:
                    return None, None
            else:
                error_message = stderr.decode()
                if "error message:" in error_message:
                    index = error_message.index("error message:")+len("error message:")
                    return None, error_message[index:].strip()
        except Exception as e:
            print(f"An error occurred while running command {command}: {e}")
            return None