# -*- coding: utf-8 -*-
# @Author: vivekpatel99
# @Date:   2018-10-06 15:44:29
# @Last Modified by:   vivekpatel99
# @Last Modified time: 2018-10-06 15:44:29
import logging

def logger_init(log_filepath, project_name = "obj_track_Img_recog"):

    # create logger with arg project name
    logger = logging.getLogger(project_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs for error messages only
    fh = logging.FileHandler(log_filepath, "w+")
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the  handlers
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
