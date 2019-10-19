# -*- coding: utf-8 -*-

import os
from unittest.mock import Mock

import pytest

from sol import parser

HERE = os.path.dirname(__file__)
DIALOGS_DIR = os.path.join(HERE, '..', 'sol', 'dialogs')


def test_line_parser():
    lparser = parser.LineParser()

    with pytest.raises(NotImplementedError):
        lparser('line')


def test_say_parser():
    say = parser.parsers[0]
    parsed = say('diga bom dia, coleguinha')
    expected = ('say', 'bom dia, coleguinha')
    assert parsed == expected


def test_say_parser_var_markup():
    say = parser.parsers[0]
    parsed = say('diga bom dia, {coleguinha}')
    expected = ('say', 'bom dia, {coleguinha}')
    assert parsed == expected


def test_ask_parser():
    ask = parser.parsers[1]
    parsed = ask('nome=pergunte Qual seu nome?')
    expected = ('ask', 'Qual seu nome?', 'nome')
    assert parsed == expected


def test_parse_slang(mocker):
    mocker.patch.object(parser.logger, 'warning', Mock(
        spec=parser.logger.warning))
    fname = os.path.join(DIALOGS_DIR, 'hello.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = parser.parse_slang(fcontents)
    assert parsed[0][0] == 'say'
    assert parsed[1][0] == 'ask'
    assert not parser.logger.warning.called


def test_parse_slang_bad(mocker):
    mocker.patch.object(parser.logger, 'warning', Mock(
        spec=parser.logger.warning))
    fname = os.path.join(DIALOGS_DIR, 'bad.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = parser.parse_slang(fcontents)
    assert parser.logger.warning.called
