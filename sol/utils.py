# -*- coding: utf-8 -*-

import logging


def create_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


logger = create_logger('sol')
