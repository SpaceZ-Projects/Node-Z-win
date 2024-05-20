import webbrowser
from toga import (
    App,
    Box,
    Button,
    Icon
)
from toga.widgets.base import Widget
from .styles.box import BoxStyle
from .styles.button import ButtonStyle

class Social(Box):
    def __init__(self, app:App, id: str | None = None, style=None, children: list[Widget] | None = None):
        style = BoxStyle.row
        super().__init__(id, style, children)
        self.app = app
        
        self.website_button = Button(
            icon=Icon("icones/website"),
            on_press=self.open_website,
            style=ButtonStyle.social_button
        )
        self.github_button = Button(
            icon=Icon("icones/github"),
            on_press=self.open_github,
            style=ButtonStyle.social_button
        )
        self.xcom_button = Button(
            icon=Icon("icones/twitterx"),
            on_press=self.open_xcom,
            style=ButtonStyle.social_button
        )
        self.facebook_button = Button(
            icon=("icones/facebook"),
            on_press=self.open_facebook,
            style=ButtonStyle.social_button
        )
        self.discord_button = Button(
            icon=Icon("icones/discord"),
            on_press=self.open_discord,
            style=ButtonStyle.social_button
        )
        
        self.add(
            self.website_button,
            self.github_button,
            self.xcom_button,
            self.facebook_button,
            self.discord_button
        )
        
    def open_website(self, button):
        self.app.visit_homepage()
        
    def open_github(self, button):
        webbrowser.open("https://github.com/btcz/")
        
    def open_xcom(self, button):
        webbrowser.open("https://x.com/BTCZOfficial")
        
    def open_facebook(self, button):
        webbrowser.open("https://www.facebook.com/BTCZCommunity/")
        
    def open_discord(self, button):
        webbrowser.open("https://discord.com/servers/bitcoinz-official-365065626668105728")