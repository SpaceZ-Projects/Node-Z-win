import clr
import System
import System.Drawing as Drawing


class Font:

    SERIF = Drawing.FontFamily.GenericSerif
    MONOSPACE = Drawing.FontFamily.GenericMonospace
    SANSSERIF = Drawing.FontFamily.GenericSansSerif


class FontStyle:

    REGULAR = Drawing.FontStyle.Regular
    BOLD = Drawing.FontStyle.Bold
    ITALIC = Drawing.FontStyle.Italic

class Alignement:

    LEFT = Drawing.ContentAlignment.MiddleLeft
    CENTER = Drawing.ContentAlignment.MiddleCenter
    RIGHT = Drawing.ContentAlignment.MiddleRight


class Color:
    AQUA = Drawing.Color.Aqua
    ANTIQUEWHITE = Drawing.Color.AntiqueWhite
    AQUAMARINE = Drawing.Color.Aquamarine
    AZURE = Drawing.Color.Azure
    WHITE = Drawing.Color.White
    WHITESMOKE = Drawing.Color.WhiteSmoke
    BLACK = Drawing.Color.Black
    ORANGE = Drawing.Color.Orange
    RED = Drawing.Color.Red
    GREEN = Drawing.Color.Green
    BLUE = Drawing.Color.Blue
    ALICEBLUE = Drawing.Color.AliceBlue
    LIGHT_BLUE = Drawing.Color.LightBlue
    LIGHT_GRAY = Drawing.Color.LightGray
    DARK_GRAY = Drawing.Color.DarkGray
    YELLOW = Drawing.Color.Yellow
    CYAN = Drawing.Color.Cyan
    MAGENTA = Drawing.Color.Magenta
    GRAY = Drawing.Color.Gray
    TOMATO = Drawing.Color.Tomato
    TURQUOISE = Drawing.Color.Turquoise
    VIOLET = Drawing.Color.Violet
    SILVER = Drawing.Color.Silver
    SEAGREEN = Drawing.Color.SeaGreen
    SANDYBROWN = Drawing.Color.SandyBrown
    SALMON = Drawing.Color.Salmon
    SADDLEBRWON = Drawing.Color.SaddleBrown
    PURPLE = Drawing.Color.Purple
    PINK = Drawing.Color.Pink
    TRANSPARENT = Drawing.Color.Transparent

    @staticmethod
    def rgb(r, g, b):
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return Drawing.Color.FromArgb(r, g, b)