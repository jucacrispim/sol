# -*- coding: utf-8 -*-

import logging
import re


def create_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


logger = create_logger('sol')


def eval_expr(expr, context, use_globals=True):
    expr = _remove_garbage(expr)
    global_context = globals() if use_globals else {}
    r = eval(expr, global_context, context)
    return r


def _remove_garbage(expr):
    p = re.compile(r'{|}')
    return p.sub('', expr)
