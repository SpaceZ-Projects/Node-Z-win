
import os
import asyncio
from pathlib import Path
import clr
import System
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Callable, Optional

from .app import App
from .style import Color

from translations import Translations


class ConfirmDialog(Forms.Form):
    def __init__(
            self,
            image: Path = None,
            message:str = None,
            text_size:int = 12,
            max_width: int = 350,
            on_confirm: Callable = None,
            on_cancel: Callable = None,
        ):
        super().__init__()

        self.app_path  = App().app_path
        self.languages = Translations()
        self._image = image
        self._message = message
        self._max_width = max_width
        self._on_confirm = on_confirm
        self._on_cancel = on_cancel
        self._text_size = text_size

        message_font = Drawing.Font(Drawing.FontFamily.GenericSerif, self._text_size, Drawing.FontStyle.Bold)
        confirm_active_path = os.path.join(self.app_path, self.languages.get_image("confirm_active"))
        confirm_inactive_path = os.path.join(self.app_path, self.languages.get_image("confirm_inactive"))
        cancel_active_path = os.path.join(self.app_path, self.languages.get_image("cancel_active"))
        cancel_inactive_path = os.path.join(self.app_path, self.languages.get_image("cancel_inactive"))

        self.confirm_active = Drawing.Bitmap(str(confirm_active_path))
        self.confirm_inactive = Drawing.Bitmap(str(confirm_inactive_path))
        self.cancel_active = Drawing.Bitmap(str(cancel_active_path))
        self.cancel_inactive = Drawing.Bitmap(str(cancel_inactive_path))

        self.Size = Drawing.Size(450, 200)
        self.BackColor = Color.rgb(25,25,25)
        self.StartPosition = Forms.FormStartPosition.CenterScreen
        self.FormBorderStyle = Forms.FormBorderStyle(0)

        if self._image:
            image_path = os.path.join(self.app_path, self._image)
            dialog_image = Drawing.Bitmap(str(image_path))

        self.dialog_icon = Forms.PictureBox()
        self.dialog_icon.Image = dialog_image
        self.dialog_icon.Size = Drawing.Size(dialog_image.Width, dialog_image.Height)
        self.dialog_icon.Location = Drawing.Point(25, 50)

        self.dialog_message = Forms.Label()
        self.dialog_message.Text = self._message
        self.dialog_message.AutoSize = False
        self.dialog_message.ForeColor = Color.WHITE
        self.dialog_message.Font = message_font
        self.dialog_message.Location = Drawing.Point(90, 70)

        self.confirm_button = Forms.PictureBox()
        self.confirm_button.Image = self.confirm_inactive
        self.confirm_button.Size = Drawing.Size(self.confirm_inactive.Width, self.confirm_inactive.Height)
        self.confirm_button.Location = Drawing.Point(129, 150)
        self.confirm_button.MouseEnter += self.confirm_button_mouse_enter
        self.confirm_button.MouseLeave += self.confirm_button_mouse_leave

        self.cancel_button = Forms.PictureBox()
        self.cancel_button.Image = self.cancel_inactive
        self.cancel_button.Size = Drawing.Size(self.cancel_inactive.Width, self.cancel_inactive.Height)
        self.cancel_button.Location = Drawing.Point(225, 150)
        self.cancel_button.MouseEnter += self.cancel_button_mouse_enter
        self.cancel_button.MouseLeave += self.cancel_button_mouse_leave

        self.dialog_border = Forms.Panel()
        self.dialog_border.Size = Drawing.Size(440, 190)
        self.dialog_border.BackColor = Color.YELLOW
        self.dialog_border.Location = Drawing.Point(5,5)

        self.dialog_box = Forms.Panel()
        self.dialog_box.Size = Drawing.Size(436, 186)
        self.dialog_box.BackColor = Color.rgb(30,30,30)
        self.dialog_box.Location = Drawing.Point(2,2)

        self.Controls.Add(self.dialog_border)

        self.dialog_border.Controls.Add(self.dialog_box)
        self.dialog_box.Controls.Add(self.dialog_icon)
        self.dialog_box.Controls.Add(self.dialog_message)
        self.dialog_box.Controls.Add(self.confirm_button)
        self.dialog_box.Controls.Add(self.cancel_button)

        self._adjust_size()

        if self._on_confirm:
            self.confirm_button.Click += self._handle_confirm

        if self._on_cancel:
            self.cancel_button.Click += self._handle_cancel


    def _adjust_size(self):
        if self._max_width is not None:
            wrapped_text = self._wrap_text(self.dialog_message.Text, self._max_width)
            graphics = self.dialog_message.CreateGraphics()
            try:
                text_size = graphics.MeasureString(wrapped_text, self.dialog_message.Font)
                padding = 1
                self.dialog_message.Size = Drawing.Size(
                    int(text_size.Width) + padding,
                    int(text_size.Height) + padding
                )
            finally:
                graphics.Dispose()


    def _wrap_text(self, text: str, max_width: int) -> str:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip() if current_line else word
            graphics = self.dialog_message.CreateGraphics()
            try:
                if graphics.MeasureString(test_line, self.dialog_message.Font).Width > max_width:
                    if current_line:
                        lines.append(current_line)
                    while len(word) > 0:
                        part = word[:max_width]
                        lines.append(part)
                        word = word[max_width:]
                    current_line = ""
                else:
                    current_line = test_line
            finally:
                graphics.Dispose()

        if current_line:
            lines.append(current_line)

        return "\n".join(lines)


    def confirm_button_mouse_enter(self, sender, event):
        self.confirm_button.Image = self.confirm_active
        self.confirm_button.Location = Drawing.Point(128, 149)

    def confirm_button_mouse_leave(self, sender, event):
        self.confirm_button.Image = self.confirm_inactive
        self.confirm_button.Location = Drawing.Point(129, 150)

    def cancel_button_mouse_enter(self, sender, event):
        self.cancel_button.Image = self.cancel_active
        self.cancel_button.Location = Drawing.Point(224, 149)

    def cancel_button_mouse_leave(self, sender, event):
        self.cancel_button.Image = self.cancel_inactive
        self.cancel_button.Location = Drawing.Point(225, 150)


    def _handle_confirm(self, sender, event):
        if self._on_confirm:
            self._on_confirm()

    def _handle_cancel(self, sender, event):
        if self._on_cancel:
            self._on_cancel()


    def close(self):
        self.Close()


    def show(self):
        self.ShowDialog()



class SelectFile(Forms.OpenFileDialog):
    def __init__(
        self,
        title: str = "Select File",
        file_types: str = "All Files (*.*)|*.*",
        initial_directory: str = "",
        result: Optional[Callable] = None
    ):
        super().__init__()

        self.Title = title
        self.Filter = file_types
        self.InitialDirectory = initial_directory
        self.result_callback = result
    
    def show(self):
        asyncio.run(self.show_dialog())
    
    async def show_dialog(self):
        loop = asyncio.get_event_loop()
        dialog_result = await loop.run_in_executor(None, self.ShowDialog)

        if dialog_result == Forms.DialogResult.OK:
            selected_file = self.FileName
            if self.result_callback:
                self.result_callback(selected_file)
        else:
            return




class SelectFolder(Forms.FolderBrowserDialog):
    def __init__(
        self,
        description: str = "Select Folder",
        folder_button: bool = True,
        default_path: str = "",
        result: Optional[Callable] = None
    ):
        super().__init__()

        self.Description = description
        self.ShowNewFolderButton = folder_button
        self.SelectedPath = default_path
        self.result_callback = result
    
    def show(self):
        asyncio.run(self.show_dialog())
    
    async def show_dialog(self):
        loop = asyncio.get_event_loop()
        dialog_result = await loop.run_in_executor(None, self.ShowDialog)
        
        if dialog_result == Forms.DialogResult.OK:
            selected_folder = self.SelectedPath
            if self.result_callback:
                self.result_callback(selected_folder)
        elif dialog_result == Forms.DialogResult.Cancel:
            if self.result_callback:
                self.result_callback(None)



