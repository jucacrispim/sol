# -*- coding: utf-8 -*-

from unittest.mock import Mock

from sol import dialog


def test_execute(mocker):
    mocker.patch.object(dialog, 'print', Mock(spec=print))
    bollocks = dialog.Bollocks()
    bollocks({})

    assert dialog.print.called
