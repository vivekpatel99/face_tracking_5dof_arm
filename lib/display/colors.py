"""
UltraColor - Meloonatic Melons
Build for Python 3
Designed for PyGame
Version 1.2

http://www.youtube.com/meloonaticmelons
http://www.meloonaticmessage.btck.co.uk

"""

import random
import os
import sys

sys.path.append(os.path.dirname(__file__))

# ------------------------------------------------------------------------------
# """ Color """
# ------------------------------------------------------------------------------


class Color:
    """ Color Variables """

    # Transparent
    Transparent = (0, 0, 0, 0)
    Null = Transparent
    Nothing = Transparent
    Blank = Transparent
    SeeThrough = Transparent

    # White Shades
    White = (255, 255, 255)
    Silver = (150, 150, 150)
    LightGray = (200, 200, 200)
    Gainsboro = (220, 220, 220)
    WhiteSmoke = (245, 245, 245)

    # Black Shades
    Black = (0, 0, 0)
    Fog = (20, 20, 20)
    DimGray = (50, 50, 50)
    Gray = (70, 70, 70)
    Mist = (120, 120, 120)

    # Red Shades
    Red = (255, 0, 0)
    Blood = (30, 0, 0)
    Maroon = (40, 0, 0)
    DarkRed = (50, 0, 0)
    Brown = (60, 50, 0)
    RedBrown = (165, 42, 42)
    Mud = (70, 60, 0)
    Firebrick = (178, 34, 34)
    IndianRed = (205, 92, 92)
    LightCoral = (240, 128, 128)
    RosyBrown = (188, 143, 143)
    MistyRose = (255, 228, 225)

    # Orange Shades
    Orange = (255, 150, 0)
    LightOrange = (255, 200, 0)
    DarkOrange = (255, 100, 0)
    Salmon = (250, 128, 114)
    Tomato = (255, 99, 71)
    DarkSalmon = (233, 150, 122)
    Coral = (255, 127, 80)
    OrangeRed = (255, 69, 0)
    LightSalmon = (255, 160, 122)
    Sienna = (160, 82, 45)
    SeaShell = (255, 245, 238)
    Chocolate = (210, 105, 30)
    SaddleBrown = (139, 69, 19)
    SandyBrown = (244, 164, 96)
    PeachPuff = (255, 218, 185)
    Peru = (205, 133, 63)
    DarkOrange = (255, 140, 0)
    BurlyWood = (222, 184, 135)
    Tan = (210, 180, 140)

    # Yellow Shades
    Yellow = (255, 255, 0)
    Linen = (250, 240, 230)
    Bisque = (255, 228, 196)
    AntiqueWhite = (250, 235, 215)
    NavajoWhite = (255, 222, 173)
    BlanchedAlmond = (255, 235, 205)
    PapayaWhip = (255, 239, 213)
    Moccasin = (255, 228, 181)
    Wheat = (245, 222, 179)
    OldLace = (253, 245, 230)
    FloralWhite = (255, 250, 240)
    DarkGoldenrod = (184, 134, 11)
    Goldenrod = (218, 165, 32)
    Cornsilk = (255, 248, 220)
    Gold = (255, 215, 0)
    Khaki = (240, 230, 140)
    LemonChiffon = (255, 250, 205)
    PaleGoldenrod = (238, 232, 170)
    DarkKhaki = (189, 183, 107)
    Beige = (245, 245, 220)
    LightGoldenrodYellow = (250, 250, 210)
    LightYellow = (255, 255, 224)
    Ivory = (255, 255, 240)

    # Green Shades
    Green = (0, 128, 0)
    Olive = (128, 128, 0)
    OliveDrab = (107, 142, 35)
    YellowGreen = (154, 205, 50)
    DarkOliveGreen = (85, 107, 47)
    GreenYellow = (173, 255, 47)
    Chartreuse = (127, 255, 0)
    LawnGreen = (124, 252, 0)
    DarkSeaGreen = (143, 188, 139)
    LightGreen = (144, 238, 144)
    ForestGreen = (34, 139, 34)
    LimeGreen = (50, 205, 50)
    PaleGreen = (152, 251, 152)
    DarkGreen = (0, 100, 0)
    Lime = (0, 255, 0)
    HoneyDew = (240, 255, 240)
    SeaGreen = (46, 139, 87)
    MediumSeaGreen = (60, 179, 113)
    SpringGreen = (0, 255, 127)
    MintCream = (245, 255, 250)
    MediumSpringGreen = (0, 250, 154)

    # Blue Shades
    Blue = (0, 0, 255)
    MediumAquamarine = (102, 205, 170)
    Aquamarine = (127, 255, 212)
    Turquoise = (64, 224, 208)
    LightSeaGreen = (32, 178, 170)
    MediumTurquoise = (72, 209, 204)
    DarkSlateGray = (47, 79, 79)
    PaleTurquoise = (175, 238, 238)
    Teal = (0, 128, 128)
    DarkCyan = (0, 139, 139)
    Aqua = (0, 255, 250)
    Cyan = (0, 255, 255)
    LightCyan = (224, 255, 255)
    Azure = (240, 255, 255)
    DarkTurqoise = (0, 206, 209)
    CadetBlue = (95, 158, 160)
    PowderBlue = (176, 224, 230)
    LightBlue = (173, 216, 230)
    DeepSkyBlue = (0, 191, 255)
    SkyBlue = (135, 206, 235)
    LightSkyBlue = (135, 206, 250)
    SteelBlue = (70, 130, 180)
    AliceBlue = (240, 248, 255)
    DodgerBlue = (30, 144, 255)
    SlateGray = (112, 128, 144)
    LightSlateGray = (119, 136, 153)
    LightSteelBlue = (176, 196, 222)
    CornflowerBlue = (100, 149, 237)
    RoyalBlue = (65, 105, 225)
    MidnightBlue = (25, 25, 112)
    Lavender = (230, 230, 250)
    Navy = (0, 0, 128)
    DarkBlue = (0, 0, 139)
    MediumBlue = (0, 0, 205)
    GhostWhite = (0, 0, 205)
    SlateBlue = (106, 90, 205)

    # Purple Shades
    Purple = (255, 0, 255)
    DarkSlateBlue = (72, 61, 139)
    MediumSlateBlue = (123, 104, 238)
    MediumPurple = (147, 112, 219)
    BlueViolet = (138, 43, 226)
    Indigo = (75, 0, 130)
    DarkOrchid = (153, 50, 204)
    DarkViolet = (148, 0, 211)
    MediumOrchid = (186, 85, 211)
    Thistle = (216, 191, 216)
    Plum = (221, 160, 221)
    Violet = (238, 130, 238)
    DarkMagenta = (139, 0, 139)
    Orchid = (218, 112, 214)
    MediumVioletRed = (199, 21, 133)
    DeepPink = (255, 20, 147)
    HotPink = (255, 105, 180)
    LavenderBlush = (255, 240, 245)
    PaleVioletRed = (219, 112, 147)
    Crimson = (220, 20, 60)
    Pink = (255, 192, 203)
    LightPink = (255, 182, 193)

    # -----------------------------------------------
    """ Random Color Generator """

    def Random(includeAlpha=False):
        """ """
        if includeAlpha:
            values = [0, 0, 0, 0]
        else:
            values = [0, 0, 0]

        for c in range(len(values)):
            values[c] = random.randrange(0, 255)

        return tuple(values)

    # -----------------------------------------------
    """ Edit Transparency """

    def WithAlpha(alpha, color):
        """ """
        listColor = list(color)
        listColor.append(alpha)
        return tuple(listColor)
