# -*- coding: utf-8 -*-

from unittest.mock import Mock

from sol import dialog


def test_from_parsed():
    parsed = {'sayings': ['oi, bom dia', 'tchau!']}
    d = dialog.Dialog.from_parsed(parsed)

    assert len(d.actions) == 2


def test_execute(mocker):
    mocker.patch.object(dialog, 'print', Mock(spec=print))

    parsed = {'sayings': ['oi, bom dia', 'tchau!']}
    d = dialog.Dialog.from_parsed(parsed)

    d.execute()

    assert len(dialog.print.call_args_list) == 2
