# -*- coding: utf-8 -*-

from unittest.mock import Mock

import pytest

from sol import actions


def test_action():
    action = actions.Action()
    with pytest.raises(NotImplementedError):
        action({})


def test_say(mocker):
    mocker.patch.object(actions, 'print', Mock(spec=print))
    say = actions.Say('hei')
    say({})

    assert actions.print.called


def test_say_context_var(mocker):
    mocker.patch.object(actions, 'print', Mock(spec=print))
    say = actions.Say('hei {oi}')
    say({'oi': 'ola'})

    assert actions.print.call_args[0][0] == 'hei ola'


def test_ask(mocker):
    mocker.patch.object(actions, 'input', Mock(spec=input,
                                               return_value='oi'))
    ask = actions.Ask('what?', 'oque')
    r = ask({})

    assert r == {'oque': 'oi'}
