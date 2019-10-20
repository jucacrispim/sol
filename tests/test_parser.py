# -*- coding: utf-8 -*-

import os
from unittest.mock import Mock

import pytest

from sol import parser

HERE = os.path.dirname(__file__)
DIALOGS_DIR = os.path.join(HERE, '..', 'sol', 'dialogs')


@pytest.fixture
def slang():
    yield parser.SlangParser()


def test_match_parser():
    lparser = parser.MatchParser()

    with pytest.raises(NotImplementedError):
        lparser('line', 0, [])


def test_say_parser(slang):
    parsed = slang._parse_lines(['diga bom dia, coleguinha'])
    expected = ('say', 'bom dia, coleguinha')
    assert parsed[0] == expected


def test_say_parser_var_markup(slang):
    parsed = slang._parse_lines(['diga bom dia, {coleguinha}'])
    expected = ('say', 'bom dia, {coleguinha}')
    assert parsed[0] == expected


def test_ask_parser(slang):
    parsed = slang._parse_lines(['nome = pergunte Qual seu nome?'])
    expected = ('ask', 'Qual seu nome?', 'nome')
    assert parsed[0] == expected


def test_parse_slang(mocker, slang):
    mocker.patch.object(parser.logger, 'warning', Mock(
        spec=parser.logger.warning))
    fname = os.path.join(DIALOGS_DIR, 'hello.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = slang(fcontents)
    assert parsed[0][0] == 'say'
    assert parsed[1][0] == 'ask'
    assert not parser.logger.warning.called


def test_parse_slang_bad(mocker, slang):
    mocker.patch.object(parser.logger, 'warning', Mock(
        spec=parser.logger.warning))
    fname = os.path.join(DIALOGS_DIR, 'bad.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    slang(fcontents)
    assert parser.logger.warning.called
