# -*- coding: utf-8 -*-

from unittest.mock import Mock

from sol import dialog


def test_from_parsed():
    parsed = [
        ('say', 'oi, bom dia'),
        ('say', 'tchau'),
        ('ask', 'what?', 'var'),

    ]
    d = dialog.Dialog.from_parsed(parsed)
    assert len(d.actions) == 3


def test_execute(mocker):
    mocker.patch.object(dialog.Say, '__call__', Mock(spec=dialog.Say.__call__))

    parsed = [
        ('say', 'oi, bom dia'),
        ('say', 'tchau'),

    ]
    d = dialog.Dialog.from_parsed(parsed)
    d.execute({})

    assert len(dialog.Say.__call__.call_args_list) == 2
