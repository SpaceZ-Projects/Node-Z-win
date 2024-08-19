
import os
import json
import asyncio
import subprocess
import psutil
import re
from .gputil import getGPUs

from toga import (
    App,
    Window,
    Box,
    Label,
    Selection,
    TextInput,
    Button,
    Divider,
    ScrollContainer
)
from toga.constants import VISIBLE, Direction
from toga.colors import WHITE, RED, YELLOW, BLACK

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.selection import SelectionStyle
from .styles.input import InputStyle
from .styles.button import ButtonStyle
from .styles.container import ContainerStyle
from .styles.divider import DividerStyle

from ..system import SystemOp
from ..client import RPCRequest
from ..command import ClientCommands

from .download import DownloadMiniZ, DownloadGminer, DownloadLolminer




class MiningWindow(Window):
    def __init__(self, app:App, window_button):
        super().__init__(
            title="Mining Tools",
            size=(800, 600),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button

        data_path = self.app.paths.data
        self.miners_dir = os.path.join(data_path, 'miners')

        
        self.select_miner_txt = Label(
            "Select Miner :",
            style=LabelStyle.select_miner_txt
        )
        self.select_miner = Selection(
            items=[
                {"miner": ""},
                {"miner": "MiniZ"},
                {"miner": "Gminer"},
                {"miner": "Lolminer"}
            ],
            accessor="miner",
            style=SelectionStyle.select_miner,
            on_change=self.verify_miners_apps
        )
        self.select_miner_box = Box(
            style=BoxStyle.select_miner_box
        )
        self.select_pool_txt = Label(
            "Mining Pool :",
            style=LabelStyle.select_pool_txt
        )
        self.select_pool = Selection(
            items=[
                {"pool": ""},
                {"pool": "2Mars"},
                {"pool": "Swgroupe"},
                {"pool": "Zeropool"},
                {"pool": "PCmining"},
                {"pool": "Darkfibersmines"},
                {"pool": "Zergpool"}
            ],
            accessor="pool",
            style=SelectionStyle.select_pool,
            on_change=self.update_server_selection
        )
        self.select_pool_box = Box(
            style=BoxStyle.select_pool_box
        )
        self.select_server_txt = Label(
            "Server :",
            style=LabelStyle.select_server_txt
        )
        self.select_server = Selection(
            enabled=False,
            style=SelectionStyle.select_server,
            accessor="region"
        )
        self.select_server_box = Box(
            style=BoxStyle.select_server_box
        )
        self.worker_name_txt = Label(
            "Worker :",
            style=LabelStyle.worker_name_txt
        )
        self.worker_name = TextInput(
            placeholder= "Worker Name",
            style=InputStyle.worker_name
        )
        self.worker_name_box = Box(
            style=BoxStyle.worker_name_box
        )
        self.worker_pass_txt = Label(
            "Pass :",
            style=LabelStyle.worker_pass_txt
        )
        self.worker_pass = TextInput(
            placeholder="[ Optional ]",
            style=InputStyle.worker_pass
        )
        self.worker_pass_box = Box(
            style=BoxStyle.worker_pass_box
        )
        self.select_address_txt = Label(
            "Address :",
            style=LabelStyle.select_address_txt
        )
        self.select_address = Selection(
            accessor="select_address",
            enabled=True,
            style=SelectionStyle.select_address
        )
        self.select_address_box = Box(
            style=BoxStyle.select_address_box
        )
        self.mining_button = Button(
            "Start",
            enabled=True,
            style=ButtonStyle.mining_button,
            on_press=self.verify_mining_params
        )
        self.options_box = Box(
            style=BoxStyle.options_box
        )
        self.name_txt = Label(f"GPU : __", style=LabelStyle.gpu_info_txt)
        self.load_txt = Label(f"Load __ %", style=LabelStyle.gpu_info_txt)
        self.memory_total_txt = Label(f"Memory Total : __ MB", style=LabelStyle.gpu_info_txt)
        self.memory_used_txt = Label(f"Memomry Used : __ MB", style=LabelStyle.gpu_info_txt)
        self.memory_free_txt = Label(f"Memory Free : __ MB", style=LabelStyle.gpu_info_txt)
        self.driver_txt = Label(f"Driver : __", style=LabelStyle.gpu_info_txt)
        self.temperature_txt = Label(f"Temperature : __ °C", style=LabelStyle.gpu_info_txt)
        self.display_active_txt = Label(f"Display : __", style=LabelStyle.gpu_info_txt)
        self.fan_speed_txt = Label(f"Fan : __ %", style=LabelStyle.gpu_info_txt)

        self.gpuinfo_box = Box(
            style=BoxStyle.gpuinfo_box
        )
        self.params_box = Box(
            style=BoxStyle.params_box
        )
        self.divider_params = Divider(
            direction=Direction.VERTICAL,
            style=DividerStyle.divider_params
        )
        self.divider = Divider(
            direction=Direction.HORIZONTAL
        )
        self.mining_output_box = Box(
            style=BoxStyle.mining_output_box
        )
        self.mining_output = ScrollContainer(
            content=self.mining_output_box,
            style=ContainerStyle.mining_output
        )
        self.main_box = Box(
            style=BoxStyle.mining_main_box
        )

        self.gpuinfo_box.add(
            self.name_txt,
            self.load_txt,
            self.memory_total_txt,
            self.memory_used_txt,
            self.memory_free_txt,
            self.driver_txt,
            self.temperature_txt,
            self.display_active_txt,
            self.fan_speed_txt
        )

        self.content = self.main_box
        
        self.app.add_background_task(
            self.get_addresses_list
        )



    async def get_addresses_list(self, widget):
        transparent_address = await self.get_transparent_addresses()
        self.select_miner.value = self.select_miner.items[0]
        self.select_pool.value = self.select_pool.items[0]
        self.select_address.items = transparent_address
        
        await self.display_window()

    

    async def display_window(self):
        self.select_miner_box.add(
            self.select_miner_txt,
            self.select_miner
        )
        self.select_pool_box.add(
            self.select_pool_txt,
            self.select_pool
        )
        self.select_server_box.add(
            self.select_server_txt,
            self.select_server
        )
        self.worker_name_box.add(
            self.worker_name_txt,
            self.worker_name
        )
        self.worker_pass_box.add(
            self.worker_pass_txt,
            self.worker_pass
        )
        self.select_address_box.add(
            self.select_address_txt,
            self.select_address
        )
        self.options_box.add(
            self.select_miner_box,
            self.select_pool_box,
            self.select_server_box,
            self.worker_name_box,
            self.worker_pass_box,
            self.select_address_box,
            self.mining_button,
        )
        self.params_box.add(
            self.options_box,
            self.divider_params,
            self.gpuinfo_box
        )
        self.main_box.add(
            self.params_box,
            self.divider,
            self.mining_output
        )
        self.update_gpu_info_task = asyncio.create_task(self.update_gpu_info())
        await asyncio.sleep(1)
        self.show()
        await asyncio.gather(
            self.update_gpu_info_task
        )


    async def update_gpu_info(self):
        while True:
            gpu_info = self.get_nvidia_gpu_info()
            if gpu_info is not None:
                id = gpu_info['id']
                name = gpu_info['name']
                load = gpu_info['load']
                memory_total = gpu_info['memory_total']
                memory_used = gpu_info['memory_used']
                memory_free = gpu_info['memory_free']
                driver = gpu_info['driver']
                temperature = gpu_info['temperature']
                display_active = gpu_info['display_active']
                fan_speed = gpu_info['fan_speed']

                self.name_txt.text = f"GPU {id} : {name}"
                self.load_txt.text = f"Load {load} %"
                self.memory_total_txt.text = f"Memory Total : {memory_total} MB"
                self.memory_used_txt.text = f"Memory Used : {memory_used} MB"
                self.memory_free_txt.text = f"Memory Free : {memory_free} MB"
                self.driver_txt.text = f"Driver : {driver}"
                self.temperature_txt.text = f"Temperature : {temperature} °C"
                self.display_active_txt.text = f"Display Active : {display_active}"
                self.fan_speed_txt.text = f"Fan : {fan_speed} %"
            await asyncio.sleep(5)
    


    async def verify_miners_apps(self, selection):
        selected_value = self.select_miner.value.miner
        miners = {
            "MiniZ": {
                "executable": "miniZ.exe",
                "dir_name": "MiniZ"
            },
            "Gminer": {
                "executable": "miner.exe",
                "dir_name": "Gminer"
            },
            "Lolminer": {
                "executable": "lolMiner.exe",
                "dir_name": "Lolminer"
            }
        }
        if not os.path.exists(self.miners_dir):
            os.makedirs(self.miners_dir)

        if selected_value in miners:
            miner_details = miners[selected_value]
            miner_executable = miner_details["executable"]
            miner_dir = os.path.join(self.miners_dir, miner_details["dir_name"])
            miner_path = os.path.join(miner_dir, miner_executable)

            if not os.path.exists(miner_dir):
                await self.ask_for_download(selected_value, miner_dir)
            elif not os.path.exists(miner_path):
                await self.ask_for_download(selected_value, miner_dir)

    
            
    async def ask_for_download(self, selected_app, miner_dir):
        async def on_confirm(window, result):
            if result is True:
                self.select_miner.enabled = False
                if not os.path.exists(miner_dir):
                    os.makedirs(miner_dir, exist_ok=True)
                if selected_app == "MiniZ":
                    DownloadMiniZ(
                        self.app,
                        self.select_miner,
                        miner_dir
                    )
                elif selected_app == "Gminer":
                    DownloadGminer(
                        self.app,
                        self.select_miner,
                        miner_dir
                    )
                elif selected_app == "Lolminer":
                    DownloadLolminer(
                        self.app,
                        self.select_miner,
                        miner_dir
                    )

            if result is False:
                self.select_miner.value = self.select_miner.items[0]
        self.question_dialog(
            "Download miner...",
            f"{selected_app} was not found in {miner_dir}. Would you like to download it?",
            on_result=on_confirm
        )

    
    async def update_server_selection(self, selection):
        selected_value = self.select_pool.value.pool
        if selected_value == "2Mars":
            server_items = [
                {"region": "Canada", "server": "btcz.ca.2mars.biz:1234"},
                {"region": "USA", "server": "btcz.us.2mars.biz:1234"},
                {"region": "Netherlands", "server": "btcz.eu.2mars.biz:1234"},
                {"region": "Singapore", "server": "btcz.sg.2mars.biz:1234"}
            ]
        elif selected_value == "Swgroupe":
            server_items = [
                {"region": "France", "server": "swgroupe.fr:2001"}
            ]
        elif selected_value == "Zeropool":
            server_items = [
                {"region": "USA", "server": "zeropool.io:1235"}
            ]
        elif selected_value == "PCmining":
            server_items = [
                {"region": "Germany", "server": "btcz.pcmining.xyz:3333"}
            ]
        elif selected_value == "Darkfibersmines":
            server_items = [
                {"region": "USA", "server": "142.4.211.28:4000"},
            ]
        elif selected_value == "Zergpool":
            server_items = [
                {"region": "North America", "server": "equihash144.na.mine.zergpool.com:2146"},
                {"region": "Europe", "server": "equihash144.eu.mine.zergpool.com:2146"},
                {"region": "Asia", "server": "equihash144.asia.mine.zergpool.com:2146"}
            ]
        else:
            self.select_server.items.clear()
            self.select_server.enabled = False
            return
        
        self.select_server.items = server_items
        self.select_server.enabled = True


    
    async def verify_mining_params(self, button):
        if not self.select_miner.value.miner:
            self.error_dialog(
                "Missing Miner Selection",
                "Please select a mining application."
            )
            return
        elif not self.select_pool.value.pool:
            self.error_dialog(
                "Missing Pool Selection",
                "Please select a mining pool."
            )
            return
        elif not self.worker_name.value:
            self.error_dialog(
                "Missing Worker Name",
                "Please set a worker name."
            )
            self.worker_name.focus()
            return
        else:
            self.mining_button_stop()
            self.disable_params()
            await self.prepare_mining_command()



    async def prepare_mining_command(self):

        selected_miner = self.select_miner.value.miner
        selected_server = self.select_server.value.server
        worker_name = self.worker_name.value
        worker_pass = self.worker_pass.value
        selected_address = self.select_address.value.select_address
        miners_dir = os.path.join(self.app.paths.data, 'miners')
        miner_path = os.path.join(miners_dir, selected_miner)
        if selected_miner == "MiniZ":
            miner_file = os.path.join(miner_path, 'miniZ.exe')
            command = [f'{miner_file} --url {selected_address}.{worker_name}@{selected_server} --pass {worker_pass} --par 144,5 --pers BitcoinZ']
        elif selected_miner == "Gminer":
            miner_file = os.path.join(miner_path, 'miner.exe')
            command = [f'{miner_file} --server {selected_server} --user {selected_address}.{worker_name} --pass {worker_pass} --algo 144_5 --pers BitcoinZ']
        elif selected_miner == "Lolminer":
            miner_file = os.path.join(miner_path, 'lolMiner.exe')
            command = [f'{miner_file}  --pool {selected_server} --user {selected_address}.{worker_name} -a EQUI144_5 --pass {worker_pass} --pers BitcoinZ']

        await self.start_mining_command(command)



    async def start_mining_command(self, command):
        try:
            self.process = await asyncio.create_subprocess_shell(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.mining_button.on_press = self.stop_mining
            self.mining_button.enabled = True
            clean_regex = re.compile(r'\x1b\[[0-9;]*[mGK]|[^a-zA-Z0-9\s\[\]=><.%()/,`\'":]')
            while True:
                stdout_line = await self.process.stdout.readline()
                if stdout_line:
                    decoded_line = stdout_line.decode().strip()
                    cleaned_line = clean_regex.sub('', decoded_line)
                    mining_output_txt = Label(
                        cleaned_line,
                        style=LabelStyle.mining_output_txt
                    )
                    self.mining_output_box.add(
                        mining_output_txt
                    )
                    self.mining_output.vertical_position = self.mining_output.max_vertical_position
                else:
                    break
            await self.process.wait()

            remaining_stdout = await self.process.stdout.read()
            remaining_stderr = await self.process.stderr.read()
            
            if remaining_stdout:
                remaining_stdout_txt = Label(
                    remaining_stdout.decode().strip(),
                    style=LabelStyle.mining_output_txt
                )
                self.mining_output_box.add(
                    remaining_stdout_txt
                )
            if remaining_stderr:
                remaining_stderr_txt = Label(
                    remaining_stderr.decode().strip(),
                    style=LabelStyle.mining_output_txt
                )
                self.mining_output_box.add(
                    remaining_stderr_txt
                )

        except Exception as e:
            print(f"Exception occurred: {e}")
        finally:
            self.add_mining_button()
            self.enable_params()

    

    async def stop_mining(self, button):
        selected_miner = self.select_miner.value.miner
        if selected_miner == "MiniZ":
            process_name =  "miniZ.exe"
        elif selected_miner == "Gminer":
            process_name = "miner.exe"
        elif selected_miner == "Lolminer":
            process_name = "lolMiner.exe"
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    print(f"Killing process {proc.pid} - {proc.info['name']}...")
                    proc.kill()
            print(f"All processes named {process_name} killed.")
            self.process.terminate()
        except Exception as e:
            print(f"Exception occurred while killing process: {e}")



    async def get_transparent_addresses(self):
        config_path = self.app.paths.config
        db_path = os.path.join(config_path, 'config.db')
        
        if os.path.exists(db_path):
            addresses_data = self.client.getAddressesByAccount()
        else:
            addresses_data = await self.command.getAddressesByAccount()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            address_items = [(address_info, address_info) for address_info in addresses_data]
        else:
            address_items = []
        
        return address_items
    

    def get_nvidia_gpu_info(self):
        gpus = getGPUs()
        if gpus:
            gpu = gpus[0]
            info = {
                'id': gpu.id,
                'name': gpu.name,
                'load': gpu.load,
                'memory_total': gpu.memoryTotal,
                'memory_used': gpu.memoryUsed,
                'memory_free': gpu.memoryFree,
                'driver': gpu.driver,
                'temperature': gpu.temperature,
                'display_active': gpu.display_active,
                'fan_speed': gpu.fan_speed
            }
            return info
        else:
            return None
    

    def disable_params(self):
        self.select_miner.enabled = False
        self.select_pool.enabled = False
        self.select_server.enabled = False
        self.worker_name.readonly = True
        self.select_address.enabled = False


    def enable_params(self):
        self.select_miner.enabled = True
        self.select_pool.enabled = True
        self.select_server.enabled = True
        self.worker_name.readonly = False
        self.select_address.enabled = True
    
    
    def add_mining_button(self):
        self.on_close = self.close_window
        self.mining_button.style.color = BLACK
        self.mining_button.style.background_color = YELLOW
        self.mining_button.text = "Start"
        self.mining_button.on_press = self.verify_mining_params
        self.mining_button.enabled = True

    
    def mining_button_stop(self):
        self.on_close = self.disable_closing_window
        self.mining_button.enabled = False
        self.mining_button.style.color = WHITE
        self.mining_button.style.background_color = RED
        self.mining_button.text = "Stop"
    

    def disable_closing_window(self, window):
        return


        
    async def close_window(self, window):
        try:
            if self.update_gpu_info_task and not self.update_gpu_info_task.done():
                self.update_gpu_info_task.cancel()
                await self.update_gpu_info_task
        except asyncio.CancelledError:
            pass
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('mining_window', False)
        self.close()