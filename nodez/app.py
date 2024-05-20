from toga import (
    App,
    MainWindow
)

from .wizard import MainWinzard


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

        self.main_window = MainWindow(
            title=self.formal_name,
            position=(550, 250),
            size=(500, 400),
            resizeable=False
        )
        self.main_window.content = MainWinzard(self)
        self.main_window.show()
        self.on_exit = self.prevent_close
        
    async def prevent_close(self, window):
        async def on_confirm(window, result):
            if result is False:
                return
            if result is True:
                self.exit()

        self.main_window.confirm_dialog(
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
    app.author = "EzzyG"
    app.version = "2024.5"
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
