import asyncio
import aiohttp
import os
import zipfile

from toga import (
    App,
    Window,
    Box,
    Label,
    ProgressBar,
    Divider,
    Icon,
    ImageView
)
from toga.window import OnCloseHandler
from toga.constants import Direction
from toga.colors import RED, BLUE

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.progressbar import ProgressStyle
from .styles.divider import DividerStyle

from .config import MakeConfig


class NodeSetup(Window):
    def __init__(self, app:App, rpc_button, local_button):
        super().__init__(
            title="Loading...",
            size=(280, 40),
            position=(220, 250),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.rpc_button = rpc_button
        self.local_button = local_button
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.cheking_txt = Label(
            "Checking node files...",
            style=LabelStyle.setup_cheking_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.setup_divider_top
        )
        self.main_box = Box(
            style=BoxStyle.setup_main_box
        )
        self.progress_bar = ProgressBar(
            max=100,
            style=ProgressStyle.setup_progress_bar
        )
        self.file_progress_bar = ProgressBar(
            max=100,
            style=ProgressStyle.setup_file_progress_bar
        )
        self.file_name_txt = Label(
            "File :",
            style=LabelStyle.setup_file_name_txt
        )
        self.main_box.add(
            self.cheking_txt,
            self.divider_top
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.check_node_files
        )
        
    async def check_node_files(self, widget):
        data_path = self.app.paths.data
        required_files = [
            'bitcoinzd.exe',
            'bitcoinz-cli.exe',
            'bitcoinz-tx.exe'
        ]
        missing_files = [
            file_name for file_name in required_files
            if not os.path.exists(os.path.join(data_path, file_name))
        ]

        if missing_files:
            self.download_task = asyncio.create_task(self.download_node_file(data_path))
            await self.download_task
        await asyncio.sleep(1)
        await self.check_zcash_params()

    async def check_zcash_params(self):
        self.cheking_txt.text = "Checking Zcash Params..."
        directory_path = os.path.join(os.getenv('APPDATA'), "ZcashParams")
        required_files = [
            'sprout-proving.key',
            'sprout-verifying.key',
            'sapling-spend.params',
            'sapling-output.params',
            'sprout-groth16.params'
        ]
        missing_files = [
            file_name for file_name in required_files
            if not os.path.exists(os.path.join(directory_path, file_name))
        ]

        if missing_files:
            self.download_task = asyncio.create_task(self.download_zcash_params(missing_files))
            await self.download_task
        await asyncio.sleep(1)
        await self.check_config_file()
        

    async def check_config_file(self):
        config_file = "bitcoinz.conf"
        self.cheking_txt.text = f"Checking {config_file}..."
        await asyncio.sleep(1)
        config_path = os.path.join(os.getenv('APPDATA'), ".bitcoinz")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        file_path = os.path.join(config_path, config_file)
        if not os.path.exists(file_path):
            self.cheking_txt.style.color = BLUE
            self.cheking_txt.text = f"Making {config_file}..."
            await asyncio.sleep(1)
            self.close()
            config_window = MakeConfig(
                self.app,
                self.rpc_button,
                self.local_button
            )
            config_window.show()
            
            

    async def download_node_file(self, data_path):
        await asyncio.sleep(1)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        self.cheking_txt.text = "Downloading node files..."
        self.title = "Downloading..."
        url = "https://github.com/btcz/bitcoinz/releases/download/2.0.8-EXT/"
        file_name = "bitcoinz-2.0.8-EXT-6c6447fba1-win64.zip"
        destination = os.path.join(data_path, file_name)
        self.current_download_file = destination

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + file_name, timeout=None) as response:
                    if response.status == 200:
                        self.main_box.add(self.progress_bar, self.file_name_txt)
                        self.file_name_txt.text = f"File : {file_name}"

                        total_size = int(response.headers.get('content-length', 0))
                        chunk_size = 256
                        downloaded_size = 0

                        self.file_handle = open(destination, 'wb')
                        async for chunk in response.content.iter_chunked(chunk_size):
                            if not chunk:
                                break
                            self.file_handle.write(chunk)
                            downloaded_size += len(chunk)
                            progress = int(downloaded_size / total_size * 100)
                            self.progress_bar.value = progress
                        self.file_handle.close()
                        self.file_handle = None

                        self.cheking_txt.text = "Extracting node files..."
                        await asyncio.sleep(1)
                        with zipfile.ZipFile(destination, 'r') as zip_ref:
                            zip_ref.extractall(data_path)
                        self.cheking_txt.text = "Node files ready."
                        self.progress_bar.value = 100
                        os.remove(destination)
                        self.main_box.remove(self.progress_bar, self.file_name_txt)
                        self.current_download_file = None
                        self.size = (280, 40)
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()

    async def download_zcash_params(self, missing_files):
        await asyncio.sleep(1)
        zcash_path = os.path.join(os.getenv('APPDATA'), "ZcashParams")
        if not os.path.exists(zcash_path):
            os.makedirs(zcash_path, exist_ok=True)

        self.cheking_txt.text = "Downloading Zcash Params..."
        self.title = "Downloading..."
        self.main_box.add(
            self.progress_bar,
            self.file_progress_bar,
            self.file_name_txt
        )
        base_url = "https://d.btcz.rocks/"
        total_files = len(missing_files)

        try:
            async with aiohttp.ClientSession() as session:
                for idx, file_name in enumerate(missing_files):
                    url = base_url + file_name
                    destination = os.path.join(zcash_path, file_name)
                    self.current_download_file = destination
                    self.file_name_txt.text = f"File : {file_name}"
                    async with session.get(url, timeout=None) as response:
                        if response.status == 200:
                            total_size = int(response.headers.get('content-length', 0))
                            chunk_size = 512
                            downloaded_size = 0

                            self.file_handle = open(destination, 'wb')
                            async for chunk in response.content.iter_chunked(chunk_size):
                                if not chunk:
                                    break
                                self.file_handle.write(chunk)
                                downloaded_size += len(chunk)
                                file_progress = int(downloaded_size / total_size * 100)
                                overall_progress = int(((idx + downloaded_size / total_size) / total_files) * 100)
                                self.file_progress_bar.value = file_progress
                                self.progress_bar.value = overall_progress
                            self.file_handle.close()
                            self.file_handle = None
                    self.current_download_file = None
                self.cheking_txt.text = "Zcash Params ready."
                await asyncio.sleep(1)
                self.main_box.remove(
                    self.progress_bar,
                    self.file_progress_bar,
                    self.file_name_txt
                )
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()

    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.cheking_txt.style.color = RED
        self.cheking_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.rpc_button.enabled = True
        self.local_button.enabled = True
        self.close()

    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.rpc_button.enabled = True
        self.local_button.enabled = True
        self.close()
        