# -*- coding: utf-8 -*-

import os

from sol import parser

HERE = os.path.dirname(__file__)
DIALOGS_DIR = os.path.join(HERE, '..', 'sol', 'dialogs')


def test_say():
    parsed = parser.say.parseString('diga bom dia, coleguinha')
    assert ' '.join(parsed.msg) == 'bom dia, coleguinha'


def test_parse_slang():
    fname = os.path.join(DIALOGS_DIR, 'hello.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = parser.parse_slang(fcontents)
    assert parsed.get('sayings')
