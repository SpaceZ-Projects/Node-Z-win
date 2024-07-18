
import asyncio
import aiohttp
import os
import zipfile
import shutil

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


class DownloadMiniZ(Window):
    def __init__(
        self,
        app:App,
        selected_miner,
        miner_dir
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

        self.selected_miner = selected_miner
        self.miner_dir = miner_dir
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.download_txt = Label(
            "Downloading MiniZ...",
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
            self.download_miner_files
        )
        
        
    async def download_miner_files(self, widget):
        await asyncio.sleep(1)
        self.show()
        data_path = self.miner_dir
        self.download_task = asyncio.create_task(self.fetch_miner_files(data_path))
        await self.download_task
            
        
         
    async def fetch_miner_files(self, data_path):
        await asyncio.sleep(1)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        self.title = "Downloading..."
        url = "https://github.com/miniZ-miner/miniZ/releases/download/v2.4d/"
        file_name = "miniZ_v2.4d_win-x64.zip"
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

                        self.download_txt.text = "Extracting files..."
                        self.main_box.remove(
                            self.progress_bar,
                            self.file_name_txt
                        )
                        self.main_box.add(
                            self.bitcoinz_coin
                        )
                        await asyncio.sleep(1)
                        await self.extract_files(destination, data_path)
                        self.close()
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()

    
    async def extract_files(self, destination, data_path):
        password = "miniZ"
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(data_path, pwd=password.encode())
        await asyncio.sleep(1)
        self.download_txt.text = "MiniZ is ready."
        await asyncio.sleep(1)
        await self.cleanup_after_extraction()



    async def cleanup_after_extraction(self):
        for file in os.listdir(self.miner_dir):
            file_path = os.path.join(self.miner_dir, file)
            if file != "miniZ.exe":
                os.remove(file_path)
        self.selected_miner.enabled = True
            
            
    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.download_txt.style.color = RED
        self.download_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.close()


    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.close()




class DownloadGminer(Window):
    def __init__(
        self,
        app:App,
        selected_miner,
        miner_dir
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

        self.selected_miner = selected_miner
        self.miner_dir = miner_dir
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.download_txt = Label(
            "Downloading Gminer...",
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
            self.download_miner_files
        )
        
        
    async def download_miner_files(self, widget):
        await asyncio.sleep(1)
        self.show()
        data_path = self.miner_dir
        self.download_task = asyncio.create_task(self.fetch_miner_files(data_path))
        await self.download_task
            
        
         
    async def fetch_miner_files(self, data_path):
        await asyncio.sleep(1)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        self.title = "Downloading..."
        url = "https://github.com/develsoftware/GMinerRelease/releases/download/3.44/"
        file_name = "gminer_3_44_windows64.zip"
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

                        self.download_txt.text = "Extracting files..."
                        self.main_box.remove(
                            self.progress_bar,
                            self.file_name_txt
                        )
                        self.main_box.add(
                            self.bitcoinz_coin
                        )
                        await asyncio.sleep(1)
                        await self.extract_files(destination, data_path)
                        self.close()
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()

    
    async def extract_files(self, destination, data_path):
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(data_path)
        await asyncio.sleep(1)
        self.download_txt.text = "Gminer is ready."
        await asyncio.sleep(1)
        await self.cleanup_after_extraction()



    async def cleanup_after_extraction(self):
        for file in os.listdir(self.miner_dir):
            file_path = os.path.join(self.miner_dir, file)
            if file != "miner.exe":
                os.remove(file_path)
        self.selected_miner.enabled = True
            
            
    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.download_txt.style.color = RED
        self.download_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.close()


    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.close()



class DownloadLolminer(Window):
    def __init__(
        self,
        app:App,
        selected_miner,
        miner_dir
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

        self.selected_miner = selected_miner
        self.miner_dir = miner_dir
        self.download_task = None
        self.current_download_file = None
        self.file_handle = None
        
        self.download_txt = Label(
            "Downloading Lolminer...",
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
            self.download_miner_files
        )
        
        
    async def download_miner_files(self, widget):
        await asyncio.sleep(1)
        self.show()
        data_path = self.miner_dir
        self.download_task = asyncio.create_task(self.fetch_miner_files(data_path))
        await self.download_task
            
        
         
    async def fetch_miner_files(self, data_path):
        await asyncio.sleep(1)
        if not os.path.exists(data_path):
            os.makedirs(data_path, exist_ok=True)
        self.title = "Downloading..."
        self.version = "1.88"
        url = f"https://github.com/Lolliedieb/lolMiner-releases/releases/download/{self.version}/"
        file_name = "lolMiner_v1.88_Win64.zip"
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

                        self.download_txt.text = "Extracting files..."
                        self.main_box.remove(
                            self.progress_bar,
                            self.file_name_txt
                        )
                        self.main_box.add(
                            self.bitcoinz_coin
                        )
                        await asyncio.sleep(1)
                        await self.extract_files(destination, data_path)
                        self.close()
        except aiohttp.ClientError as e:
            print(e)
            self.handle_download_error()

    
    async def extract_files(self, destination, data_path):
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(data_path)
        await asyncio.sleep(1)
        self.download_txt.text = "Lolminer is ready."
        await asyncio.sleep(1)
        os.remove(destination)
        await self.cleanup_after_extraction()



    async def cleanup_after_extraction(self):
        app_folder = os.path.join(self.miner_dir, self.version)
        for file in os.listdir(app_folder):
            file_path = os.path.join(app_folder, file)
            if file == "lolMiner.exe":
                destination_path = os.path.join(self.miner_dir, "lolMiner.exe")
                shutil.move(file_path, destination_path)
        
        shutil.rmtree(app_folder)
        self.selected_miner.enabled = True
            
            
    def handle_download_error(self):
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
        if self.current_download_file and os.path.exists(self.current_download_file):
            os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.download_txt.style.color = RED
        self.download_txt.text = "Download Failed"
        self.progress_bar.value = 0
        self.close()


    def close_window(self, widget):
        if self.download_task is not None:
            self.download_task.cancel()
            if self.file_handle:
                self.file_handle.close()
                self.file_handle = None
            if self.current_download_file and os.path.exists(self.current_download_file):
                os.remove(self.current_download_file)
        self.selected_miner.enabled = True
        self.close()