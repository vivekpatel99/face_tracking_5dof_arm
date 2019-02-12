# Created by viv at 14.10.18

"""
The display_gui contains classes and function for display gui.
This script contains following classes
 - main display initialisation such as font, text, buttons and image

"""

import os
import sys
import time
import pygame
import logging

sys.path.append(os.path.dirname(__file__))
from colors import *

sys.path.append("../../")
import config

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" pygame initialisation """

pygame.init()

# path = os.path.abspath(os.path.join("../../", "definition"))
#
# if not os.path.exists(path):
#     print("[ERROR] define module can not import, path does not exist")
# sys.path.append(path)
# import config

# -----------------------------------------------
""" constants declaration  """

SCREEN_WIDTH = 1265
SCREEN_HEIGHT = 1015
# SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
# SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)  # width, height

# SCREEN_SIZE = (0, 0)  # width, height
TITLE_POSTION = (200, 25)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------------------------------------------------------------------------------
# """ Font """
# ------------------------------------------------------------------------------


class Font:
    Default = pygame.font.SysFont("Comic Sans MS", 20)
    Small = pygame.font.SysFont("Verdana", 30)
    Medium = pygame.font.SysFont("Verdana", 40)
    Large = pygame.font.SysFont("Verdana", 60)
    Scanner = pygame.font.SysFont("Verdana", 30)


# ------------------------------------------------------------------------------
# """ MouseOver """
# ------------------------------------------------------------------------------

def MouseOver(rect):
    """ """
    mouse_pos = pygame.mouse.get_pos()
    # mouse_pos[0] > rect[0] and mouse_pos[0] < rect[0] + rect[2] and mouse_pos[1] > rect[1] and mouse_pos[1] < rect[
    #     1] + rect[3]:
    if rect[0] < mouse_pos[0] < rect[0] + rect[2] and rect[1] < mouse_pos[1] < rect[1] + rect[3]:
        return True
    else:
        return False


# ------------------------------------------------------------------------------
# """ Menu """
# ------------------------------------------------------------------------------


class Menu:
    """ Menu class """

    def __init__(self, framebuffer="/dev/fb1"):
        """ """
        # os.putenv("SDL_FBDEV", framebuffer)
        # os.environ["SDL_FBDEV"] = fb3

        self.screen = None

        try:
            if not pygame.init():
                pygame.init()
                log.info("pygame initialisation done ")
                # print("pygame initialisation done ")

        except Exception as error:
            log.info(error)

    def display_init(self, size=SCREEN_SIZE, flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF):
        """ display initialisation function will initialise pygame display with given size and flags """

        log.info("display initialisation done ")
        # print("display initialisation done ")
        self.screen = pygame.display.set_mode(size)

        return self.screen

    def display_color(self, color=WHITE):
        """ display_color will fill the color on display, default color is white"""

        self.screen.fill(color)

    def render(self):
        """ render display """
        pygame.display.update()

    # ------------------------------------------------------------------------------
    # """ Button """
    # ------------------------------------------------------------------------------

    class Button:
        """ Button class will initialise button with fonts and render it """
        All = []

        def __init__(self, text, rect, bg=Color.Gray, fg=Color.White, bgr=Color.CornflowerBlue, font=Font.Default,
                     tag=("menu", None)):
            self.Text = text
            self.Left = rect[0]
            self.Top = rect[1]
            self.Width = rect[2]
            self.Height = rect[3]
            self.Command = None
            self.Rolling = False
            self.Tag = tag

            # NORMAL BUTTON
            self.Normal = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            self.Normal.fill(bg)
            RText = font.render(text, True, fg)  # text, actualising, color
            txt_rect = RText.get_rect()
            self.Normal.blit(RText, (self.Width / 2 - txt_rect[2] / 2, self.Height / 2 - txt_rect[3] / 2))

            # HIGHLIGHTED BUTTON
            self.High = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE | pygame.SRCALPHA)
            self.High.fill(bgr)
            self.High.blit(RText, (self.Width / 2 - txt_rect[2] / 2, self.Height / 2 - txt_rect[3] / 2))

            # SAVE BUTTON
            Menu.Button.All.append(self)

        # -----------------------------------------------
        """ Render """

        def Render(self, to, pos=(0, 0)):  # pos = x, y
            """ Render function """

            if MouseOver((self.Left + pos[0], self.Top + pos[1], self.Width, self.Height)):
                to.blit(self.High, (self.Left + pos[0], self.Top + pos[1]))
                self.Rolling = True
            else:
                to.blit(self.Normal, (self.Left + pos[0], self.Top + pos[1]))
                self.Rolling = False

    # ------------------------------------------------------------------------------
    # """ Text """
    # ------------------------------------------------------------------------------

    class Text:
        """ Text class will initialise input text and render it """
        All = []

        def __init__(self, text, font=Font.Default, color=Color.Black, bg=None):
            self.Text = text
            self.LastText = text
            self.Font = font
            self.Color = color
            self.Left = 0
            self.Top = 0
            self.Bg = bg

            bitmap = font.render(text, True, color)
            self.Bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
            if bg != None:
                self.Bitmap.fill(bg)
            self.Bitmap.blit(bitmap, (0, 0))

            self.Width = self.Bitmap.get_width()
            self.Height = self.Bitmap.get_height()

        # -----------------------------------------------
        """ Render """

        def Render(self, to, pos=(0, 0)):
            if self.Text != self.LastText:
                # TEXT HAS BEEN CHANGED
                self.LastText = self.Text

                # RECREATE BITMAP (Dynamic Text Rendering)
                bitmap = self.Font.render(self.Text, True, self.Color)
                self.Bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
                if self.Bg != None:
                    self.Bitmap.fill(self.Bg)
                self.Bitmap.blit(bitmap, (0, 0))

                self.Width = self.Bitmap.get_width()
                self.Height = self.Bitmap.get_height()

            to.blit(self.Bitmap, (self.Left + pos[0], self.Top + pos[1]))

    # ------------------------------------------------------------------------------
    # """ display """
    # ------------------------------------------------------------------------------

    class Image:
        """ Image class initialise input image and render it """

        def __init__(self, bitmap, pos=(0, 0)):
            self.Bitmap = bitmap
            self.Left = pos[0]
            self.Top = pos[1]
            self.Height = bitmap.get_height()
            self.Width = bitmap.get_width()

        def Render(self, to, pos=(0, 0)):
            """ """
            to.blit(self.Bitmap, (self.Left + pos[0], self.Top + pos[1]))

    # ------------------------------------------------------------------------------
    # """ FrameText """
    # ------------------------------------------------------------------------------

    class FrameText:
        """ FrameText class will initialise frame on display and text and render it"""
        rect_x = 50
        rect_y = config.HORIZ_PIXELS_SMALL + 10  # 10 pixel down from frame
        rect_width = SCREEN_WIDTH - 100  # reduce distance from edge of the screen width
        rect_height = 330

        text_x = rect_x + 5
        text_y = rect_y + 5

        def __init__(self, screen, font=Font.Small):
            self.font = font
            # self.font = pygame.font.SysFont("Verdana", 15)
            self.screen = screen
            self.Left = 0
            self.Top = 0

        # -----------------------------------------------
        """ add_frame """

        def add_frame(self, color=Color.CornflowerBlue, rect=(rect_x, rect_y, rect_width, rect_height)):
            """ """
            self.rect = rect
            self.rect = pygame.draw.rect(self.screen, color, rect, 2)

        # -----------------------------------------------
        """ add_text """

        def add_text(self, text, text_color=Color.Black, flag=True, pos=(text_x, text_y)):
            """ """
            self.screen.blit(self.font.render(text, flag, text_color), pos)

            # bitmap = self.font.render(text, flag, text_color)
            # self.Bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
            # self.Bitmap.blit(bitmap, (0, 0)
            # pygame.display.update()

        # def Render(self, to, pos=(0,0)):
        #     to.blit(self.screen, (self.Left + pos[0], self.Top + pos[1]))


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------

def main():
    pass
    # scope = display()
    # scope.test()
    # time.sleep(10)


if __name__ == "__main__":
    main()

    # pass
