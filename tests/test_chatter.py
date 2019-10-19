# -*- coding: utf-8 -*-

from unittest.mock import Mock

from sol import chatter
from sol.dialog import Dialog


def test_get_dialogs():
    dialogs = list(chatter._get_dialogs())
    assert isinstance(dialogs[0][1], Dialog)


def test_respond_to_default():
    c = chatter.Chatter()
    c.default = Mock(spec=c.default)
    c.respond_to('bla')
    assert c.default.called


def test_respond_to_hello():
    c = chatter.Chatter()
    c.dialogs['hello'] = Mock(spec=c.dialogs['hello'])
    c.respond_to('hello')
    assert c.dialogs['hello'].called
