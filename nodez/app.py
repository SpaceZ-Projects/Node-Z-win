import os

from toga import (
    App,
    MainWindow
)

from .wizard.wizard import MainWizard


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
            size=(550 ,400),
            resizable=False
        )
        self.main_window.content = MainWizard(self.app)
        self.on_exit = self.prevent_close
        
    async def prevent_close(self, window):
        async def on_confirm(window, result):
            if result is False:
                return
            if result is True:
                await self.clean_config_path()
                self.exit()

        self.main_window.question_dialog(
            title="Exit...",
            message="You are about to exit the app. Are you sure ?",
            on_result=on_confirm
        )
    
    async def clean_config_path(self):
        config_path = self.app.paths.config
        if not os.path.exists(config_path):
            return
        db_path = os.path.join(config_path, 'config.db')
        if os.path.exists(db_path):
            os.remove(db_path)


def main():
    app = NodeZ()
    app.icon="resources/app_logo"
    app.formal_name = "Node-Z"
    app.app_id = "com.nodez"
    app.home_page = "https://www.getbtcz.com"
    app.author = "BTCZCommunity"
    app.version = "2024.5"
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
