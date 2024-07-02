
import os
import shutil
import asyncio
import clr
clr.AddReference("System")
from System import UriFormatException

from toga import (
    App,
    Window,
    WebView,
    Box,
    Button,
    Label,
    TextInput,
    Divider,
)
from urllib.parse import urlparse, urlunparse
from toga.constants import Direction, VISIBLE

from .styles.webview import WebStyle
from .styles.input import InputStyle
from .styles.box import BoxStyle
from .styles.button import ButtonStyle

from ..system import SystemOp


class BrowserWindow(Window):
    def __init__(self, app: App, window_button):
        super().__init__(
            title="Web Browser",
            position=(0, 0),
            resizable=True,
            minimizable=True,
            on_close=self.close_window,
        )
        self.system = SystemOp(self.app)
        screen_size = self.system.windows_full_screen()
        self.size = screen_size
        
        self.window_button = window_button
        
        self.web_navigator = WebView(
            style=WebStyle.navigator_webview,
            on_webview_load=self.on_webview_loaded
        )
        self.divider_barre = Divider(
            direction=Direction.HORIZONTAL
        )
        self.url_input = TextInput(
            value="https://www.getbtcz.com/",
            style=InputStyle.url_input,
            on_confirm=self.load_page
        )
        self.go_button = Button(
            "Go",
            style=ButtonStyle.go_button,
            on_press=self.load_page
        )
        self.loading_txt = Label(
            "Loading Page..."
        )
        self.barre_box = Box(
            style=BoxStyle.navigator_barre_box
        )
        self.main_box = Box(
            style=BoxStyle.navigator_main_box
        )
        self.barre_box.add(
            self.url_input,
            self.go_button
        )
        self.main_box.add(
            self.barre_box,
            self.divider_barre,
            self.web_navigator
        )
        
        self.content = self.main_box
        default_url = self.url_input.value
        self.web_navigator.url = default_url
        
        self.show()
        
    def load_page(self, button):
        url = self.url_input.value
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url
        try:
            parsed_url = urlparse(url)
            url = urlunparse(parsed_url)
            self.url_input.value = url
            self.web_navigator.url = url
        except UriFormatException:
            self.error_dialog(
                "Invalid Url",
                "Invalid URI: Failed to parse hostname."
            )

        
    async def on_webview_loaded(self, widget):
        pass
        
        
    async def close_window(self, window):
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('browser_window', False)
        self.close()

        cache_path = self.app.paths.cache
        if os.path.exists(cache_path):
            try:
                await asyncio.sleep(10)
                shutil.rmtree(cache_path)
            except OSError as e:
                print(f"Error deleting cache: {e}")
