

from toga import (
    App,
    MainWindow
)

from .main_window.wizard import MainWizard
from .system import SystemOp


class NodeZ(App):
    def __init__(self):
        super().__init__()
        self._version = None
        self._formal_name = None
        self._app_id = None
        self._home_page = None
        self._author = None
        
    @property
    def version(self):
        return self._version
    @version.setter
    def version(self, value):
        self._version = value

    @property
    def formal_name(self):
        return self._formal_name
    @formal_name.setter
    def formal_name(self, value):
        self._formal_name = value
        
    @property
    def app_id(self):
        return self._app_id
    @app_id.setter
    def app_id(self, value):
        self._app_id = value

    @property
    def home_page(self):
        return self._home_page
    @home_page.setter
    def home_page(self, value):
        self._home_page = value

    @property
    def author(self):
        return self._author
    @author.setter
    def author(self, value):
        self._author = value
        
        
    def startup(self):
        self.system = SystemOp(self.app)

        self.main_window = MainWindow(
            title=self.formal_name,
            size=(550 ,400),
            resizable=False
        )
        position_center = self.system.windows_screen_center(
            self.main_window.size
        )
        self.main_window.position = position_center
        self.main_window.content = MainWizard(self.app)
        self.on_exit = self.prevent_close
        
        
    async def prevent_close(self, window):
        async def on_confirm(window, result):
            if result is False:
                return
            if result is True:
                self.exit()

        self.main_window.question_dialog(
            title="Exit...",
            message="You are about to exit the app. Are you sure ?",
            on_result=on_confirm
        )


def main():
    app = NodeZ()
    app.icon="resources/app_logo"
    app.formal_name = "Node-Z"
    app.app_id = "com.nodez"
    app.home_page = "https://www.getbtcz.com"
    app.author = "BTCZCommunity"
    app.version = "1.0.3"
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
