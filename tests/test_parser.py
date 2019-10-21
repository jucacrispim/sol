# -*- coding: utf-8 -*-

import os
from unittest.mock import Mock

import pytest

from sol import parser

HERE = os.path.dirname(__file__)
DIALOGS_DIR = os.path.join(HERE, 'dialogs')


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


def test_parse_if(slang):
    fname = os.path.join(DIALOGS_DIR, 'cond.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = slang(fcontents)
    assert parsed[1][0] == 'if'
    assert len(parsed[1][2]) == 2
    assert len(parsed[1][3]) == 1
    assert len(parsed) == 2


def test_parse_if_no_else(slang):
    fname = os.path.join(DIALOGS_DIR, 'cond_no_else.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = slang(fcontents)
    assert parsed[1][0] == 'if'
    assert len(parsed[1][2]) == 2
    assert len(parsed[1][3]) == 0
    assert len(parsed) == 5


def test_parse_call(slang):
    fname = os.path.join(DIALOGS_DIR, 'call.slang')
    with open(fname) as fd:
        fcontents = fd.read()
    parsed = slang(fcontents)
    assert parsed[0][0] == 'call'
    assert parsed[0][1] == 'a_fn(1)'
    assert parsed[0][2] == 'a'


def test_parse_nested_identation_error(slang):
    fname = os.path.join(DIALOGS_DIR, 'cond_indentation_error.slang')
    with open(fname) as fd:
        fcontents = fd.read()

    with pytest.raises(IndentationError):
        slang(fcontents)


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
