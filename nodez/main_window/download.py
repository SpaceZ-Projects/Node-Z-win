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
    ImageView
)
from toga.constants import Direction
from toga.colors import RED

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.progressbar import ProgressStyle
from .styles.divider import DividerStyle

from ..system import SystemOp


class DownloadNode(Window):
    def __init__(
        self,
        app:App,
        download_button,
        local_botton,
        rpc_button
    ):
        super().__init__(
            title="Loading...",
            size=(280, 90),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.download_button = download_button
        self.local_button = local_botton
        self.rpc_button = rpc_button
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.download_txt = Label(
            "Downloading node files...",
            style=LabelStyle.download_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.download_divider_top
        )
        self.main_box = Box(
            style=BoxStyle.download_main_box
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
            style=LabelStyle.file_name_txt
        )
        self.bitcoinz_coin = ImageView(
            ("resources/btcz_coin1.gif")
        )
        self.main_box.add(
            self.download_txt,
            self.divider_top,
            self.bitcoinz_coin
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.download_node_files
        )
        
        
    async def download_node_files(self, widget):
        self.app.main_window.hide()
        await asyncio.sleep(1)
        self.show()
        data_path = self.app.paths.data
        self.download_task = asyncio.create_task(self.fetch_node_files(data_path))
        await self.download_task
            
        
         
    async def fetch_node_files(self, data_path):
        await asyncio.sleep(1)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        self.title = "Downloading..."
        url = "https://github.com/btcz/bitcoinz/releases/download/2.0.8-EXT/"
        file_name = "bitcoinz-2.0.8-EXT-6c6447fba1-win64.zip"
        destination = os.path.join(data_path, file_name)
        self.current_download_file = destination
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + file_name, timeout=None) as response:
                    if response.status == 200:
                        self.main_box.remove(
                            self.bitcoinz_coin
                        )
                        self.main_box.add(
                            self.progress_bar,
                            self.file_name_txt
                        )
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

                        self.download_txt.text = "Extracting node files..."
                        self.main_box.remove(
                            self.progress_bar,
                            self.file_name_txt
                        )
                        self.main_box.add(
                            self.bitcoinz_coin
                        )
                        await asyncio.sleep(1)
                        with zipfile.ZipFile(destination, 'r') as zip_ref:
                            zip_ref.extractall(data_path)
                        self.download_txt.text = "Node files ready."
                        os.remove(destination)
                        self.current_download_file = destination
                        await asyncio.sleep(1)
                        self.close()
                        self.rpc_button.enabled = True
                        self.check_requirements_files()
                        self.app.main_window.show()
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()
            
            
    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.download_txt.style.color = RED
        self.download_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.rpc_button.enabled = True
        self.close()
        self.app.main_window.show()

    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.rpc_button.enabled = True
        self.check_requirements_files()
        self.close()
        self.app.main_window.show()
        
    
    def check_requirements_files(self):
        config_file = self.system.load_config_file()
        if config_file is None:
            config_status = False
        else:
            config_status = True
        node_files = self.system.load_node_files()
        if node_files is not None:
            node_status = False
            self.download_button.enabled = True
        else:
            node_status = True
            self.download_button.enabled = False
        params_files = self.system.load_params_files()
        if params_files is not None:
            params_status = False
        else:
            params_status = True
        if config_status is True and node_status is True and params_status is True:
            self.local_button.enabled = True
        
        
        
            
            
class DownloadParams(Window):
    def __init__(
        self,
        app:App,
        download_button,
        local_button,
        rpc_button
    ):
        super().__init__(
            title="Loading...",
            size=(280, 90),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.download_button = download_button
        self.local_button = local_button
        self.rpc_button = rpc_button
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.download_txt = Label(
            "Downloading Params...",
            style=LabelStyle.download_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.download_divider_top
        )
        self.main_box = Box(
            style=BoxStyle.download_main_box
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
            style=LabelStyle.file_name_txt
        )
        self.bitcoinz_coin = ImageView(
            ("resources/btcz_coin1.gif")
        )
        self.main_box.add(
            self.download_txt,
            self.divider_top,
            self.bitcoinz_coin
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.download_zcash_params
        )
            
            
    async def download_zcash_params(self, widget):
        self.app.main_window.hide()
        await asyncio.sleep(1)
        self.show()
        missing_files = self.system.load_params_files()
        if missing_files:
            self.download_task = asyncio.create_task(self.fetch_zcash_params(missing_files))
            await self.download_task
            

    async def fetch_zcash_params(self, missing_files):
        await asyncio.sleep(1)
        zcash_path = os.path.join(os.getenv('APPDATA'), "ZcashParams")
        if not os.path.exists(zcash_path):
            os.makedirs(zcash_path, exist_ok=True)
            
        self.title = "Downloading..."
        self.main_box.remove(
            self.bitcoinz_coin
        )
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
                self.download_txt.text = "Params ready."
                await asyncio.sleep(1)
                self.close()
                self.rpc_button.enabled = True
                self.check_requirements_files()
                self.app.main_window.show()
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()
            

    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.download_txt.style.color = RED
        self.download_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.rpc_button.enabled = True
        self.close()
        self.app.main_window.show()
        

    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.rpc_button.enabled = True
        self.check_requirements_files()
        self.close()
        self.app.main_window.show()
        
        
    def check_requirements_files(self):
        config_file = self.system.load_config_file()
        if config_file is None:
            config_status = False
        else:
            config_status = True
        node_files = self.system.load_node_files()
        if node_files is not None:
            node_status = False
        else:
            node_status = True
        params_files = self.system.load_params_files()
        if params_files is not None:
            params_status = False
            self.download_button.enabled = True
        else:
            params_status = True
            self.download_button.enabled = False
        if config_status is True and node_status is True and params_status is True:
            self.local_button.enabled = True
        