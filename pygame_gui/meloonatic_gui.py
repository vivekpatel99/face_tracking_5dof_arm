"""
Meloonatic Melons
GUI Framework
By Harry Hitchen
"""

import pygame
from scripts.UltraColor import *

pygame.init()


def MouseOver(rect):
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > rect[0] and mouse_pos[0] < rect[0] + rect[2] and mouse_pos[1] > rect[1] and mouse_pos[1] < rect[1] + rect[3]:
        return True
    else:
        return False

        
    


class Font:

    Default = pygame.font.SysFont("Verdana", 20)
    Small = pygame.font.SysFont("Verdana", 15)
    Medium = pygame.font.SysFont("Verdana", 40)
    Large = pygame.font.SysFont("Verdana", 60)
    Scanner = pygame.font.SysFont("Verdana", 30)
    

        

class Menu:  

    class Button:

        All = []

        def __init__(self, text, rect, bg, fg, bgr, font = Font.Default, tag = ("menu", None)):
            self.Text = text
            self.Left = rect[0]
            self.Top = rect[1]
            self.Width = rect[2]
            self.Height = rect[3]
            self.Command = None
            self.Rolling = False
            self.Tag = tag

            # NORMAL BUTTON
            self.Normal = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE|pygame.SRCALPHA)
            self.Normal.fill(bg)
            RText = font.render(text, True, fg)   # text, antialiasing, color
            txt_rect = RText.get_rect()
            self.Normal.blit(RText, (self.Width / 2 - txt_rect[2] / 2, self.Height / 2 - txt_rect[3] / 2))

            # HIGHLIGHTED BUTTON
            self.High = pygame.Surface((self.Width, self.Height), pygame.HWSURFACE|pygame.SRCALPHA)
            self.High.fill(bgr)
            self.High.blit(RText, (self.Width / 2 - txt_rect[2] / 2, self.Height / 2 - txt_rect[3] / 2))

            # SAVE BUTTON
            Menu.Button.All.append(self)


        def Render(self, to, pos = (0, 0)):
            if MouseOver((self.Left + pos[0], self.Top + pos[1], self.Width, self.Height)):
                to.blit(self.High, (self.Left + pos[0], self.Top + pos[1]))
                self.Rolling = True
            else:
                to.blit(self.Normal, (self.Left + pos[0], self.Top + pos[1]))
                self.Rolling = False



    class Text:

        All = []

        def __init__(self, text, font = Font.Default, color = Color.Lime, bg = None):
            self.Text = text
            self.LastText = text
            self.Font = font
            self.Color = color
            self.Left = 0
            self.Top = 0
            self.Bg = bg

            bitmap = font.render(text, True, color)
            self.Bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA|pygame.HWSURFACE)
            if bg != None:
                self.Bitmap.fill(bg)
            self.Bitmap.blit(bitmap, (0, 0))

            self.Width = self.Bitmap.get_width()
            self.Height = self.Bitmap.get_height()

        def Render(self, to, pos = (0, 0)):
            if self.Text != self.LastText:
                # TEXT HAS BEEN CHANGED
                self.LastText = self.Text

                # RECREATE BITMAP (Dynamic Text Rendering)
                bitmap = self.Font.render(self.Text, True, self.Color)
                self.Bitmap = pygame.Surface(bitmap.get_size(), pygame.SRCALPHA|pygame.HWSURFACE)
                if self.Bg != None:
                    self.Bitmap.fill(self.Bg)
                self.Bitmap.blit(bitmap, (0, 0))

                self.Width = self.Bitmap.get_width()
                self.Height = self.Bitmap.get_height()



            to.blit(self.Bitmap, (self.Left + pos[0], self.Top + pos[1]))



    class Image:

        def __init__(self, bitmap, pos = (0, 0)):
            self.Bitmap = bitmap
            self.Left = pos[0]
            self.Top = pos[1]
            self.Height = bitmap.get_height()
            self.Width = bitmap.get_width()

        def Render(self, to, pos = (0, 0)):
            to.blit(self.Bitmap, (self.Left + pos[0], self.Top + pos[1]))













    
            
