# -*- coding: utf-8 -*-

from unittest.mock import Mock

from sol import dialog


def test_execute(mocker):
    mocker.patch.object(dialog.Say, '__call__', Mock(spec=dialog.Say.__call__))
    bollocks = dialog.Bollocks()
    bollocks({})

    assert dialog.Say.__call__.called
