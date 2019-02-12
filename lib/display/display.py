# Created by viv at 26.10.18
""" The Display script contains all gui functions """

import os
import cv2
import collections
import logging
import numpy as np

from tkinter import *
import tkinter as tk

import pygame
from pygame.locals import *

sys.path.append("../../")
import config
from lib.display import display_gui, colors

log = logging.getLogger("main." + __name__)

# -----------------------------------------------
""" globals """

# Frames per second
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 500
HEIGHT = 500
MARGIN = 60

RECT_SIZE = (10, 10)
SMALL_BUTTON = (5, 5, 100, 50)
BIG_BUTTON = (5, 5, 200, 50)
EXIT_BUTTON = (5, 5, 40, 40)
PROJECT_TITLE = 'Closed Loop Object Tracking based on Image Recognition'
btn_done = None

# video frame position on the display in pixel values
VID_FRAME_POS = (50, 150)  # x, y


# ------------------------------------------------------------------------------
# """ start_btn_action """
# ------------------------------------------------------------------------------


def start_btn_action():
    """ start_button_action """
    config.CAM_START = True
    log.info("Start Button clicked")


# ------------------------------------------------------------------------------
# """ stop_btn_action """
# ------------------------------------------------------------------------------


def stop_btn_action():
    """ stop_button_action """

    config.CAM_START = False
    log.info("Stop Button clicked")

    btn_done = True


# ------------------------------------------------------------------------------
# """ start_btn_action """
# ------------------------------------------------------------------------------


def exit_btn_action():
    """ start_button_action """
    config.EXIT = True
    log.info("Exit Button clicked")


# ------------------------------------------------------------------------------
# """ forward_btn_action """
# ------------------------------------------------------------------------------


def forward_btn_action():
    """ forward_button_action """

    if config.VID_FRAME_INDEX >= 2:
        config.VID_FRAME_INDEX = 2

    else:
        config.VID_FRAME_INDEX += 1
    log.info("Forward Button clicked")


# ------------------------------------------------------------------------------
# """ backward_btn_action """
# ------------------------------------------------------------------------------


def backward_btn_action():
    """ backward_button_action """

    if config.VID_FRAME_INDEX <= 0:
        config.VID_FRAME_INDEX = 0

    else:
        config.VID_FRAME_INDEX -= 1
    log.info("Backward Button clicked")


# ------------------------------------------------------------------------------
# """ face_recog_btn_action """
# ------------------------------------------------------------------------------

def face_recog_btn_action():
    """ face_recognition_button_action """
    config.TASK_INDEX = 1
    log.info("Face recognition Button clicked")


# ------------------------------------------------------------------------------
# """ object_tracking_btn_action """
# ------------------------------------------------------------------------------

def object_tracking_btn_action():
    """ object_tracking_button_action """
    config.TASK_INDEX = 2
    log.info("Object Tracking Button clicked")


# ------------------------------------------------------------------------------
# """ object_tracking_btn_action """
# ------------------------------------------------------------------------------

def object_recog_btn_action():
    """ object_tracking_button_action """
    config.TASK_INDEX = 3
    log.info("Object Recognition Button clicked")


# ------------------------------------------------------------------------------
# """ display_menu_init """
# ------------------------------------------------------------------------------


def display_menu_init(screen):
    """
    display_menu_init function initialise all gui on the display

    :param screen: object from pygame.display.setmode
    :return: namedtupled of all the objects of gui
    """

    title = display_gui.Menu.Text(text=PROJECT_TITLE, font=display_gui.Font.Medium)

    # image_title = display_gui.Menu.Text(text=task_title, font=display_gui.Font.Medium)
    #
    # info = "INFO"
    # info = display_gui.Menu.Text(text=img_title_str, font=display_gui.Font.Medium)

    frame_info = display_gui.Menu.FrameText(screen)
    frame_info.add_frame()

    # info  = display_gui.Menu.FrameText(text=task_info, font=display_gui.Font.Small)
    # pygame.draw.rect(info, )

    start_btn = display_gui.Menu.Button(text="START", rect=SMALL_BUTTON)
    start_btn.Command = start_btn_action

    stop_btn = display_gui.Menu.Button(text="STOP", rect=SMALL_BUTTON)
    stop_btn.Command = stop_btn_action

    forward_btn = display_gui.Menu.Button(text=">>", rect=SMALL_BUTTON)
    forward_btn.Command = forward_btn_action

    backward_btn = display_gui.Menu.Button(text="<<", rect=SMALL_BUTTON)
    backward_btn.Command = backward_btn_action

    exit_btn = display_gui.Menu.Button(text="X", rect=EXIT_BUTTON, bgr=colors.Color.RedBrown)
    exit_btn.Command = exit_btn_action

    face_recog_btn = display_gui.Menu.Button(text="Face Recognition", rect=BIG_BUTTON)
    face_recog_btn.Command = face_recog_btn_action

    obj_tracking_btn = display_gui.Menu.Button(text="Motion detection", rect=BIG_BUTTON)
    obj_tracking_btn.Command = object_tracking_btn_action

    obj_recog_btn = display_gui.Menu.Button(text="Object Recognition", rect=BIG_BUTTON)
    obj_recog_btn.Command = object_recog_btn_action

    display_object = collections.namedtuple("display_object",
                                            ["title", "frame_info", "start_btn", "stop_btn", "exit_btn", "forward_btn",
                                             "backward_btn", "face_recog_btn",
                                             "obj_tracking_btn", "obj_recog_btn"])

    disply_obj = display_object(title, frame_info, start_btn, stop_btn, exit_btn, forward_btn, backward_btn,
                                face_recog_btn, obj_tracking_btn, obj_recog_btn)

    return disply_obj


# ------------------------------------------------------------------------------
# """ display_render """
# ------------------------------------------------------------------------------


def display_render(screen, frame, dsply_obj, task_info):
    """
    display_render render all the pygame object on display

    :param screen: object from pygame.display.setmode
    :param frame: opencv video frame
    :param dsply_obj:  namdedtuple of display_menu_init
    :param task_info: string task info

    :return:
    """
    # taking list of all the events form the display gui
    for event in pygame.event.get():
        # check if the pygame window quit button precess or not
        if event.type == pygame.QUIT:
            config.EXIT = True

        # check mouse event on display
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # check for left mouse click
                # handle button click events
                for btn in display_gui.Menu.Button.All:
                    if btn.Rolling:  # mouse is over button
                        # if not btn.Command() != None:  # do button event
                        if btn.Command():  # do button event
                            btn.Command()

                        btn.Rolling = False
                        break

    # 144 is upper y value of the picture frame, SMALL_BUTTON[3] = button height (50)
    dsply_obj.start_btn.Render(screen, pos=(SMALL_BUTTON[3] + 10 + config.HORIZ_PIXELS_SMALL, 144))
    #  length of small button  + 10 pixel (50  + 10) = 60
    dsply_obj.stop_btn.Render(screen,
                              pos=(SMALL_BUTTON[3] + 10 + config.HORIZ_PIXELS_SMALL, 144 + SMALL_BUTTON[3] + 10))

    # SMALL_BUTTON[2] = button weight (100)
    dsply_obj.exit_btn.Render(screen, pos=(display_gui.SCREEN_WIDTH - SMALL_BUTTON[2] + 48, 0))

    # 574 is lower y value of frame
    dsply_obj.forward_btn.Render(screen, pos=(SMALL_BUTTON[3] + 10 + config.HORIZ_PIXELS_SMALL, 574))
    dsply_obj.backward_btn.Render(screen,
                                  pos=(SMALL_BUTTON[3] + 10 + config.HORIZ_PIXELS_SMALL, 574 - SMALL_BUTTON[3] - 10))

    # 280 pixel away form start button
    dsply_obj.face_recog_btn.Render(screen, pos=(280 + config.HORIZ_PIXELS_SMALL, 144))

    dsply_obj.obj_tracking_btn.Render(screen, pos=(280 + config.HORIZ_PIXELS_SMALL, 144 + SMALL_BUTTON[3] + 10))
    dsply_obj.frame_info.add_text(text=task_info)

    dsply_obj.obj_recog_btn.Render(screen,
                                   pos=(280 + config.HORIZ_PIXELS_SMALL, (144 + (2 * SMALL_BUTTON[3] + 10)) + 10))
    dsply_obj.frame_info.add_text(text=task_info)

    frame = np.rot90(frame)

    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, VID_FRAME_POS)

    dsply_obj.title.Render(to=screen, pos=display_gui.TITLE_POSTION)
    # dsply_obj.image_title.Render(to=screen, pos=(config.VID_FRAME_CENTER, 100))
    pygame.display.flip()
    # pygame.display.update()

# ------------------------------------------------------------------------------
# """ test_loop """
# ------------------------------------------------------------------------------


def test_loop():
    """ testing of  all the object for gui """
    global btn_done
    btn_done = False
    img_path = "1.jpg"
    if not os.path.isfile(img_path):
        log.error("image does not exist {}".format(img_path))
    img = cv2.imread(img_path, 1)
    # size = (config.HORIZ_PIXELS_SMALL, config.VERT_LINES_SMALL)
    resize_frame = cv2.resize(img, config.VID_FRAME_SIZE)

    frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    disply = display_gui.Menu()
    screen = disply.display_init()
    disply.display_color()

    # fonts = pygame.font.SysFont("Comic Sans MS", 40)
    # title = fonts.render('Closed Loop Object Tracking based on Image Recognition', False, (0, 0, 255))
    title = display_gui.Menu.Text(text=PROJECT_TITLE, font=display_gui.Font.Medium)

    img_title_str = "Panda"
    image_title = display_gui.Menu.Text(text=img_title_str, font=display_gui.Font.Medium)

    title_info_str = "INFO"
    title_info_str = display_gui.Menu.Text(text=img_title_str, font=display_gui.Font.Medium)

    task_info = "Vivek, John Snow, khalisi"
    frame_info = display_gui.Menu.FrameText(screen)
    frame_info.add_frame()
    # info  = display_gui.Menu.FrameText(text=task_info, font=display_gui.Font.Small)
    # pygame.draw.rect(info, )

    start_btn = display_gui.Menu.Button(text="START", rect=SMALL_BUTTON)
    start_btn.Command = start_btn_action

    stop_btn = display_gui.Menu.Button(text="STOP", rect=SMALL_BUTTON)
    stop_btn.Command = stop_btn_action

    forward_btn = display_gui.Menu.Button(text=">>", rect=SMALL_BUTTON)
    forward_btn.Command = forward_btn_action

    backward_btn = display_gui.Menu.Button(text="<<", rect=SMALL_BUTTON)
    backward_btn.Command = backward_btn_action

    face_recog_btn = display_gui.Menu.Button(text="Face Recognition", rect=BIG_BUTTON)
    face_recog_btn.Command = face_recog_btn_action

    obj_tracking_btn = display_gui.Menu.Button(text="Object Tracking", rect=BIG_BUTTON)
    obj_tracking_btn.Command = object_tracking_btn_action

    # btn_start.Left = display_gui.SCREEN_HEIGHT/2 - btn_start.Left*2
    frame_center = (50 + config.HORIZ_PIXELS_SMALL) / 2
    frame_end = 60 + config.HORIZ_PIXELS_SMALL

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # check for left mouse click
                    # handle button click events
                    for btn in display_gui.Menu.Button.All:
                        if btn.Rolling:  # mouse is over button
                            if btn.Command() != None:  # do button event
                                btn.Command()
                            btn.Rolling = False
                            break

            if btn_done:
                done = True
        # 144 is upper y value of the picture frame
        start_btn.Render(screen, pos=(60 + config.HORIZ_PIXELS_SMALL, 144))
        #  length of small button  + 10 pixel (50  + 10) = 60
        stop_btn.Render(screen, pos=(60 + config.HORIZ_PIXELS_SMALL, 144 + 60))
        # 574 is lower y value of frame
        forward_btn.Render(screen, pos=(60 + config.HORIZ_PIXELS_SMALL, 574))
        backward_btn.Render(screen, pos=(60 + config.HORIZ_PIXELS_SMALL, 574 - 60))

        face_recog_btn.Render(screen, pos=(280 + config.HORIZ_PIXELS_SMALL, 144))

        obj_tracking_btn.Render(screen, pos=(280 + config.HORIZ_PIXELS_SMALL, 144 + 60))
        frame_info.add_text(text=task_info)
        screen.blit(frame, (50, 150))

        title.Render(to=screen, pos=display_gui.TITLE_POSTION)
        image_title.Render(to=screen, pos=(frame_center, 100))
        pygame.display.flip()


# ----------------------------------------------------------------------------------------------------------------------
# """ main """
# ----------------------------------------------------------------------------------------------------------------------


def main():
    fb3 = "/dev/fb0"
    os.putenv("SDL_FBDEV", fb3)
    # set up audio driver to avoid alisa lib erros
    os.environ['SDL_AUDIODRIVER'] = "dsp"

    # os.environ['SDL_VIDEODRIVER'] = fb3
    # os.environ["SDL_FBDEV"] = fb3
    config.platform_init()

    # pygame.init()
    # root = setup_tkinter()
    # fps_clock = pygame.time.Clock()

    # WIDTH =  config.VERTICAL_LINES
    # HEIGHT = config.HORIZONTAL_PIXELS
    # # screen = pygame.display.set_mode((1240, 1010))
    # size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    #
    # print("Framebuffer size set {} x {}".format(size[0],size[1]))
    #
    # screen = pygame.display.set_mode((1265, 1015), pygame.FULLSCREEN)
    # while True:
    #     screen.fill(BLACK)

    # game_loop(screen, fps_clock)
    test_loop()


if __name__ == '__main__':
    main()
