# -*- coding: utf-8 -*-

import os

from .dialog import Dialog, Bollocks
from .parser import parse_slang


HERE = os.path.dirname(__file__)
DIALOGS_DIR = os.path.join(HERE, 'dialogs')


def _get_slangs():
    for fname in os.listdir(DIALOGS_DIR):
        if not fname.endswith('.slang'):
            continue
        fpath = os.path.join(DIALOGS_DIR, fname)
        with open(fpath) as fd:
            slang = fd.read()
        fname = fname.split('.')[0]
        yield fname, slang


def _get_dialogs():
    for fname, slang in _get_slangs():
        d = Dialog.from_parsed(parse_slang(slang))
        yield fname, d


class Chatter:

    DEFAULT_DIALOG_CLS = Bollocks

    def __init__(self):
        self.default = self.DEFAULT_DIALOG_CLS()
        self.dialogs = {fname: dialog for fname, dialog in _get_dialogs()}

    def respond_to(self, text):
        dialog = self.dialogs.get(text, self.default)
        dialog({})
        return True
